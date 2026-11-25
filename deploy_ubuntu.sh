#!/bin/bash
set -e

# Add 2GB Swap if not present (prevents RAM crash on Free Tier)
if [ ! -f /swapfile ]; then
    sudo fallocate -l 2G /swapfile
    sudo chmod 600 /swapfile
    sudo mkswap /swapfile
    sudo swapon /swapfile
    echo '/swapfile none swap sw 0 0' | sudo tee -a /etc/fstab > /dev/null
fi

sudo apt update && sudo DEBIAN_FRONTEND=noninteractive apt install -y python3-pip python3-venv nginx git

sudo iptables -I INPUT 6 -m state --state NEW -p tcp --dport 80 -j ACCEPT
sudo iptables -I INPUT 6 -m state --state NEW -p tcp --dport 443 -j ACCEPT
sudo mkdir -p /etc/iptables && sudo iptables-save | sudo tee /etc/iptables/rules.v4 > /dev/null

cd /home/ubuntu/django_python
sudo DEBIAN_FRONTEND=noninteractive apt install -y software-properties-common
sudo add-apt-repository -y ppa:deadsnakes/ppa
sudo apt update && sudo DEBIAN_FRONTEND=noninteractive apt install -y python3.12 python3.12-venv python3.12-dev
rm -rf venv
python3.12 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt

SECRET_KEY=$(python3 -c "import secrets; print(secrets.token_urlsafe(50))")
cat <<EOF > .env
DEBUG=False
SECRET_KEY=$SECRET_KEY
ALLOWED_HOSTS=130.210.8.93,localhost,127.0.0.1
CSRF_TRUSTED_ORIGINS=http://130.210.8.93
SESSION_COOKIE_SECURE=False
CSRF_COOKIE_SECURE=False
EOF

export DJANGO_SETTINGS_MODULE=settings.production
python manage.py migrate
python manage.py collectstatic --noinput

chmod 755 /home/ubuntu

sudo tee /etc/systemd/system/hybrid_marketplace.service > /dev/null <<EOF
[Unit]
Description=Hybrid Marketplace Gunicorn Service
After=network.target

[Service]
User=ubuntu
Group=www-data
WorkingDirectory=/home/ubuntu/django_python
Environment="DJANGO_SETTINGS_MODULE=settings.production"
ExecStart=/home/ubuntu/django_python/venv/bin/gunicorn --workers 2 --bind 127.0.0.1:8000 core.wsgi:application
Restart=always

[Install]
WantedBy=multi-user.target
EOF

sudo systemctl daemon-reload
sudo systemctl enable hybrid_marketplace
sudo systemctl restart hybrid_marketplace

sudo tee /etc/nginx/sites-available/hybrid_marketplace > /dev/null <<EOF
server {
    listen 80;
    server_name 130.210.8.93;

    client_max_body_size 20M;

    location /static/ {
        alias /home/ubuntu/django_python/staticfiles/;
    }

    location /media/ {
        alias /home/ubuntu/django_python/media/;
    }

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto \$scheme;
    }
}
EOF

sudo ln -sf /etc/nginx/sites-available/hybrid_marketplace /etc/nginx/sites-enabled/
sudo rm -f /etc/nginx/sites-enabled/default
sudo nginx -t && sudo systemctl restart nginx
echo "=========================================="
echo "LIVE READY: http://130.210.8.93"
echo "=========================================="

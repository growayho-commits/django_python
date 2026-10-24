from .base import *

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-local-dev-secret-key-change-in-production'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# Allowed Hosts (Workspace & Localhost support)
ALLOWED_HOSTS = ['*']

# Database Configuration (SQLite for local workspace)
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# Real Email Configuration (SMTP - Gmail)
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'growayho@gmail.com'       # உங்கள் நிறுவனத்தின் மின்னஞ்சல் ஐடி
EMAIL_HOST_PASSWORD = 'Lakshmi@786123'        # Gmail App Password

# Email Sender & Superuser Notification Config
DEFAULT_FROM_EMAIL = 'GROWAY SOLUTIONS <growayho@gmail.com>'
SUPERUSER_EMAIL = 'growayho@gmail.com'          # சூப்பர் யூசரின் உண்மையான மின்னஞ்சல் ஐடி
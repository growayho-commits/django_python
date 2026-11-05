from pathlib import Path
from .base import *

# (local.py ஆனது settings/ ஃபோல்டருக்குள் இருப்பதால் .parent கொடுக்க வேண்டும்)
BASE_DIR = Path(__file__).resolve().parent.parent

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-local-dev-secret-key-change-in-production'

DEBUG = True

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
EMAIL_HOST_USER = 'growayho@gmail.com'
EMAIL_HOST_PASSWORD = 'Lakshmi@786123'

DEFAULT_FROM_EMAIL = 'HYBRID MARKETPLACE <growayho@gmail.com>'
SUPERUSER_EMAIL = 'growayho@gmail.com'

# REST Framework Integration (Missing previously)
INSTALLED_APPS += [
    'rest_framework',
    
]

REST_FRAMEWORK = {
    'DEFAULT_RENDERER_CLASSES': [
        'rest_framework.renderers.JSONRenderer',
        'rest_framework.renderers.BrowsableAPIRenderer',
    ]
}
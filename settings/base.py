import os
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent.parent

SECRET_KEY = os.environ.get('SECRET_KEY', 'django-insecure-default-change-me-in-production')

DEBUG = True

ALLOWED_HOSTS = ['*']

# Application definition
INSTALLED_APPS = [
    # Catalogs Apps
    'apps.catalogs.reviews_ratings',
    'apps.catalogs.search_filters',
    'apps.catalogs.bundles_kits',
    'apps.catalogs.specifications',
    'apps.catalogs.catalog_statuses',
    'apps.catalogs.catalog_medias',
    'apps.catalogs.variants',
    'apps.catalogs.attributes',
    'apps.catalogs.categories',
    'apps.catalogs.inventories',
    'apps.catalogs.pricing_tiers',
    'apps.catalogs.core_catalogs',
    'apps.professional_network',
    'apps.marketing_leads.wishlists.apps.WishlistsConfig',
    'apps.professional_network.service_categries',

    # Django Default Apps
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Custom Domain Apps (Domain-Driven Design Structure - Users Group)
    'apps.users.guests.apps.GuestsConfig',
    'apps.users.members.apps.MembersConfig',
    'apps.users.merchant.apps.MerchantConfig',
    'apps.users.executives.apps.ExecutivesConfig',
    'apps.users.sellers.apps.SellersConfig',
    'apps.users.superusers.apps.SuperusersConfig',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# 👇 Pointing to core.urls since your urls.py is inside the core folder
ROOT_URLCONF = 'core.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'core.wsgi.application'

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'Asia/Kolkata'
USE_I18N = True
USE_TZ = True

STATIC_URL = 'static/'
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

MEDIA_URL = 'media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Custom User Model Configuration for SoC / DDD Architecture
AUTH_USER_MODEL = 'guests.CoreUser'
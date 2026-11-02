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

    # Professional Network Apps
    'apps.professional_network',
    'apps.professional_network.service_categries',

    # Marketing & Leads Apps
    'apps.marketing_leads.ads_campaigns',
    'apps.marketing_leads.carts',
    'apps.marketing_leads.checkout_flows',
    'apps.marketing_leads.coupons_discounts',
    'apps.marketing_leads.customer_leads',
    'apps.marketing_leads.orders',
    'apps.marketing_leads.push_notifications',
    'apps.marketing_leads.wishlists',

    # Finances Apps
    'apps.finances.bank_accounts',
    'apps.finances.commissions',
    'apps.finances.payment_gateways',
    'apps.finances.payouts',
    'apps.finances.taxes',

    # Logistics Apps
    'apps.logistics.logistics_partners',
    'apps.logistics.returns',
    'apps.logistics.shipments',
    'apps.logistics.warehouse_transfers',

    # Systems Apps
    'apps.systems.analytics',
    'apps.systems.audits',
    'apps.systems.integrations',

    # Customer Support Apps
    'apps.customer_supports.faqs',
    'apps.customer_supports.helpdesk_tickets',
    'apps.customer_supports.live_chats',
    'apps.customer_supports.return_refunds',

    # Django Default Apps
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Custom Domain Apps (Domain-Driven Design Structure - Users Group)
    'apps.users.guests',
    'apps.users.members',
    'apps.users.merchant',
    'apps.users.executives',
    'apps.users.sellers',
    'apps.users.superusers',
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
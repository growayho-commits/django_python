import importlib
import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
SECRET_KEY = os.environ.get('SECRET_KEY', 'django-insecure-default-change-me-in-production')
DEBUG = True
ALLOWED_HOSTS = ['*']


def load_app_configs(apps_root: Path):
    """Auto-discover all sub-app conf.py files and collect unique INSTALLED_APPS & context processors."""
    project_apps, context_processors = [], []
    if not apps_root.exists():
        return project_apps, context_processors

    for conf_file in sorted(apps_root.rglob("conf.py")):
        if any(part in {"__pycache__", "migrations"} for part in conf_file.parts):
            continue
        module_path = ".".join(conf_file.relative_to(BASE_DIR).with_suffix("").parts)
        mod = importlib.import_module(module_path)
        cfg = getattr(mod, "APP_CONFIG", None)
        if cfg and cfg.get("enabled", True):
            app_path = cfg.get("app_path")
            ctx_proc = cfg.get("context_processor")
            if app_path and app_path not in project_apps:
                project_apps.append(app_path)
            if ctx_proc and ctx_proc not in context_processors:
                context_processors.append(ctx_proc)
    return project_apps, context_processors


PROJECT_APPS, USER_CONTEXT_PROCESSORS = load_app_configs(BASE_DIR / "apps")

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
] + PROJECT_APPS

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

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
            ] + USER_CONTEXT_PROCESSORS,
        },
    },
]

WSGI_APPLICATION = 'core.wsgi.application'

AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
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
AUTH_USER_MODEL = 'superusers.CoreUser'

# Session & Authentication Settings
SESSION_EXPIRE_AT_BROWSER_CLOSE = True
LOGIN_URL = '/api/v1/users/superusers/login/'
"""
Django settings for inventory_management project.
"""

from pathlib import Path
import os

# -------- Base Directory --------
BASE_DIR = Path(__file__).resolve().parent.parent


# -------- Security Settings --------
SECRET_KEY = 'django-insecure-@mek79a&qbmx2vf!td&3ljum(b2k+f6ib=%(btoyz)slbs3=x)'
DEBUG = True
ALLOWED_HOSTS = []


# -------- Installed Apps --------
INSTALLED_APPS = [

    'jazzmin',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # ====== Local Apps ======
    'app_product',
    'app_supplier',
    'app_customer',
    'app_purchase',
    'app_sales',
    'app_stock',
    'app_account',
    'app_user',
    'app_dashboard',
    'app_asset',
    'app_expense',
]


# -------- Middleware --------
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]


# -------- Root & Templates --------
ROOT_URLCONF = 'inventory_management.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',

        # ✅ Project-level templates folder
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

WSGI_APPLICATION = 'inventory_management.wsgi.application'


# -------- Database --------
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# -------- Password Validators --------
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]


# -------- Internationalization --------
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'Asia/Dhaka'   # ✅ তোমার লোকাল টাইমজোন অনুযায়ী
USE_I18N = True
USE_TZ = True


# -------- Static & Media Files --------
STATIC_URL = '/static/'
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]  # ✅ for development
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')    # ✅ for production

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')


# -------- Custom User Model --------
AUTH_USER_MODEL = 'app_user.User'   # ✅ custom user model active


# -------- Default Auto Field --------
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

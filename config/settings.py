"""
Django settings for ruby project.
Author Ali RajabNezhad 30 Dec 2022
"""
import os
from datetime import timedelta
from pathlib import Path
from dotenv import dotenv_values
from kavenegar import KavenegarAPI

from config.storage import STORAGE_MEDIA_URL

BASE_DIR = Path(__file__).resolve().parent.parent

env = dotenv_values(BASE_DIR / '.env')

QR_DIR = BASE_DIR / 'qr_codes'

SECRET_KEY = env['SECRET_KEY']

STORAGE_ENDPOINT_URL = env['STORAGE_ENDPOINT_URL']
STORAGE_ACCESS_KEY = env['STORAGE_ACCESS_KEY']
STORAGE_SECRET_KEY = env['STORAGE_SECRET_KEY']
BUCKET_NAME = env['BUCKET_NAME']

KAVENEGAR_API_KEY = env['KAVENEGAR_API_KEY']

KAVENEGAR = KavenegarAPI(KAVENEGAR_API_KEY)

DEBUG = True

ALLOWED_HOSTS = ['*']

CSRF_TRUSTED_ORIGINS = [
    'https://api.btcgift.shop',
    'https://api.league23.ir',
]
CORS_ALLOWED_ORIGINS = [
    'https://btcgift.shop',
    'https://btc.league23.ir',
    'http://localhost:3000',
]

INSTALLED_APPS = [
    'simpleui',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'corsheaders',
    'tinymce',
    'faq',
    'user',
    'blog',
    'card',
    'support',
    'payment',
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'home/templates'],
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

LOGS_DIR = BASE_DIR / 'logs'
if not os.path.exists(LOGS_DIR):
    os.makedirs(LOGS_DIR)

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '| {asctime} | {message}',
            'style': '{',
        },
    },
    # TODO: volume LOGS_DIR
    'handlers': {
        'file': {
            'formatter': 'verbose',
            'filename': LOGS_DIR / 'btcgift.log',
            'class': 'logging.handlers.RotatingFileHandler',
            'maxBytes': 1024 * 1024 * 100,  # 100 MB,
            'backupCount': 3
        },
        'console': {
            'class': 'rich.logging.RichHandler',
            'show_time': False,
            'formatter': 'verbose'
        },
    },
    'loggers': {
        'root': {
            'handlers': ['console', 'file'],
            'level': 'INFO',
            'propagate': False
        },
    },
}

WSGI_APPLICATION = 'config.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

REST_FRAMEWORK = {
    'DEFAULT_THROTTLE_RATES': {'anon': '30 /min'},
    'DEFAULT_RENDERER_CLASSES': ['rest_framework.renderers.JSONRenderer'],
    'DEFAULT_THROTTLE_CLASSES': ['rest_framework.throttling.AnonRateThrottle'],
    'DEFAULT_AUTHENTICATION_CLASSES': ['user.authentication.JWTAuthentication'],
}

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

# CACHES = {
#     "default": {
#         "BACKEND": "django_redis.cache.RedisCache",
#         "LOCATION": REDIS_URL,
#         "OPTIONS": {
#             "CLIENT_CLASS": "django_redis.client.DefaultClient"
#         },
#         "KEY_PREFIX": "cache"
#     }
# }


AUTH_USER_MODEL = 'user.User'

OTP_LEN = 4

JWT_EXP = timedelta(days=30).total_seconds()

OTP_EXP = int(timedelta(minutes=1).total_seconds())

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Asia/Tehran'

USE_I18N = True

USE_TZ = True

STATIC_URL = 'static/'
STATIC_ROOT = BASE_DIR / 'static'


LOGIN_REDIRECT_URL = '/'

MEDIA_URL = 'media/'
MEDIA_ROOT = BASE_DIR / 'media'
# MEDIA_URL = STORAGE_MEDIA_URL + '/'
# MEDIA_ROOT = STORAGE_MEDIA_URL

import os
import sys
from datetime import timedelta
import sentry_sdk
import logging

from django.conf import settings
from sentry_sdk.integrations.django import DjangoIntegration
from sentry_sdk.integrations.logging import LoggingIntegration
from decouple import config
from pathlib import Path


# BASE
# --------------------------------------------------------------------------

BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.append(os.path.join(BASE_DIR, "apps"))

# SECURITY
# -----------------------------------------------------------------------------------------

SECRET_KEY = config('SECRET_KEY',default='+jtdiuho*l-0_%97w^%!ctlxq7m&2_=lo4o^u*d4fco*9%')

DEBUG = config('DEBUG',default=False)

ALLOWED_HOSTS = []

# APPS
# -----------------------------------------------------------------------------------------

DJANGO_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
]

EXTERNAL_APPS = [
    "rest_framework",
    "rest_framework_simplejwt",
    "drf_spectacular",
    "django_filters"
]

LOCAL_APPS = [
    'user',
]

INSTALLED_APPS = DJANGO_APPS + EXTERNAL_APPS + LOCAL_APPS


# MIDDLEWARE
# -----------------------------------------------------------------------------------------

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "core.urls"

# TEMPLATES
# -----------------------------------------------------------------------------------------

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

# APPLICATIONS
# -----------------------------------------------------------------------------------------

WSGI_APPLICATION = "core.wsgi.application"

# DATABASES
# -----------------------------------------------------------------------------------------

DATABASES = {
    "default": {
        "ENGINE": config("DB_ENGINE",default="django.db.backends.sqlite3"),
        "NAME": config("DB_NAME",default=BASE_DIR / "db.sqlite3"),
        "USER":config("DB_USER",default=''),
        "PASSWORD":config("DB_PASSWORD",default=''),
        "HOST":config("DB_HOST",default=''),
        "PORT":config("DB_PORT",default='')
    }
}

# PASSWORD VALIDATORS
# -----------------------------------------------------------------------------------------

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]

# INTERNATIONALIZATION
# -----------------------------------------------------------------------------------------

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True

# STATIC & MEDIA FILES
# -----------------------------------------------------------------------------------------

STATIC_URL = "static/"
STATIC_ROOT = BASE_DIR / "static"

MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"

# DEFAULT PRIMARY KEY FIELD
# -----------------------------------------------------------------------------------------

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# AUTH_USER_MODEL
# -----------------------------------------------------------------------------------------
AUTH_USER_MODEL = 'user.User'

# REST_FRAMEWORK
# -----------------------------------------------------------------------------------------
REST_FRAMEWORK = {
    'DEFAULT_SCHEMA_CLASS':'drf_spectacular.openapi.AutoSchema',
    'DEFAULT_AUTHENTICATION_CLASSES':[
        'rest_framework_simplejwt.authentication.JWTAuthentication'
    ],
    'DEFAULT_PERMISSION_CLASSES':[
        'rest_framework.permissions.AllowAny'
    ]
}

# JWT
# -----------------------------------------------------------------------------------------
SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(minutes=60),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=1),
    "ROTATE_REFRESH_TOKENS": False,
    "BLACKLIST_AFTER_ROTATION": False,
    "UPDATE_LAST_LOGIN": False,

    "ALGORITHM": "HS256",
    "SIGNING_KEY": settings.SECRET_KEY,
    "VERIFYING_KEY": "",
    "AUDIENCE": None,
    "ISSUER": None,
    "JSON_ENCODER": None,
    "JWK_URL": None,
    "LEEWAY": 0,

    "AUTH_HEADER_TYPES": ("Bearer",),
    "AUTH_HEADER_NAME": "HTTP_AUTHORIZATION",
    "USER_ID_FIELD": "id",
    "USER_ID_CLAIM": "user_id",
    "USER_AUTHENTICATION_RULE": "rest_framework_simplejwt.authentication.default_user_authentication_rule",

    "AUTH_TOKEN_CLASSES": ("rest_framework_simplejwt.tokens.AccessToken",),
    "TOKEN_TYPE_CLAIM": "token_type",
    "TOKEN_USER_CLASS": "rest_framework_simplejwt.models.TokenUser",

    "JTI_CLAIM": "jti",

    "SLIDING_TOKEN_REFRESH_EXP_CLAIM": "refresh_exp",
    "SLIDING_TOKEN_LIFETIME": timedelta(minutes=5),
    "SLIDING_TOKEN_REFRESH_LIFETIME": timedelta(days=1),

    "TOKEN_OBTAIN_SERIALIZER": "rest_framework_simplejwt.serializers.TokenObtainPairSerializer",
    "TOKEN_REFRESH_SERIALIZER": "rest_framework_simplejwt.serializers.TokenRefreshSerializer",
    "TOKEN_VERIFY_SERIALIZER": "rest_framework_simplejwt.serializers.TokenVerifySerializer",
    "TOKEN_BLACKLIST_SERIALIZER": "rest_framework_simplejwt.serializers.TokenBlacklistSerializer",
    "SLIDING_TOKEN_OBTAIN_SERIALIZER": "rest_framework_simplejwt.serializers.TokenObtainSlidingSerializer",
    "SLIDING_TOKEN_REFRESH_SERIALIZER": "rest_framework_simplejwt.serializers.TokenRefreshSlidingSerializer",
}

# DRF_SPECTACULAR
# -----------------------------------------------------------------------------------------
SPECTACULAR_SETTINGS = {
    'TITLE': 'Telegram Clone Project API',
    'DESCRIPTION': 'This Projects is Telegram app clone api',
    'VERSION': '1.0.0',
    'SERVE_INCLUDE_SCHEMA': False,
    'COMPONENT_SPLIT_REQUEST':False,
    # OTHER SETTINGS
}

# REDIS
# -----------------------------------------------------------------------------------------


# CACHES
# -----------------------------------------------------------------------------------------


# CHANNELS
# -----------------------------------------------------------------------------------------


# CELERY
# -----------------------------------------------------------------------------------------


# SENTRY SDK
# -----------------------------------------------------------------------------------------
SENTRY_DSN = config("SENTRY_DSN")

sentry_logging = LoggingIntegration(
    level=logging.INFO,
    event_level=logging.ERROR
)

integrations = [
    sentry_logging,
    DjangoIntegration()
]

sentry_sdk.init(
    dsn=SENTRY_DSN,
    integrations=integrations,
    traces_sample_rate=1.0,
    profiles_sample_rate=1.0
)

# FIREBASE
# -----------------------------------------------------------------------------------------


# SMS API
# -----------------------------------------------------------------------------------------


# EMAIL
# -----------------------------------------------------------------------------------------


# ELASTICSEARCH
# -----------------------------------------------------------------------------------------


# LOGGING
# -----------------------------------------------------------------------------------------

import os
import sys

from pathlib import Path

# BASE
# --------------------------------------------------------------------------

BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.append(os.path.join(BASE_DIR, "apps"))

# SECURITY
# -----------------------------------------------------------------------------------------

SECRET_KEY = "django-insecure-z#9g^u)aoa1*+i#_mpt8&%&wm$4vg6)k(=h++$ftljnbds^1)m"

DEBUG = True

ALLOWED_HOSTS = []

# APPS
# -----------------------------------------------------------------------------------------

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
]

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
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
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


# REST_FRAMEWORK
# -----------------------------------------------------------------------------------------


# JWT
# -----------------------------------------------------------------------------------------


# DRF_SPECTACULAR
# -----------------------------------------------------------------------------------------


# RIDES
# -----------------------------------------------------------------------------------------


# CACHES
# -----------------------------------------------------------------------------------------


# CHANNELS
# -----------------------------------------------------------------------------------------


# CELERY
# -----------------------------------------------------------------------------------------


# SENTRY SDK
# -----------------------------------------------------------------------------------------


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

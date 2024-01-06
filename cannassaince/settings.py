from pathlib import Path
from datetime import timedelta
import os
from pydantic_settings import BaseSettings
from pydantic import EmailStr, HttpUrl
from typing import Dict, List


class GeneralSettings(BaseSettings):

    CURRENT_HOST: str = 'localhost:8000'
    BASE_FRONTEND_URL: str = 'http://127.0.0.1:8000/api/v1/auth/users'
    DEBUG: bool = False
    ALLOWED_HOSTS: List[str] = ['http://localhost:8000']


GENERAL_SETTINGS = GeneralSettings()


# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "django-insecure-8en_=!11=c4r^1_@9&78ky%#2s(ut*jq3$57q6fhuj&gexdg65"

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.sites",
    "rest_framework",
    "corsheaders",
    "rest_framework_simplejwt",
    "drf_yasg",
    "rest_framework_simplejwt.token_blacklist",
    "djoser",
    "authenticate.apps.AuthenticateConfig",
    "shared.apps.SharedConfig",
    'social_django',
]

MIDDLEWARE = [
    "corsheaders.middleware.CorsMiddleware",
    'social_django.middleware.SocialAuthExceptionMiddleware',
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "cannassaince.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / 'templates'],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                'social_django.context_processors.backends',
                'social_django.context_processors.login_redirect',
            ],
        },
    },
]

WSGI_APPLICATION = "cannassaince.wsgi.application"


# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": "postgres",
        "USER": "postgres",
        "PASSWORD": "password",
        "HOST": "db",
        "PORT": "5432",
    }
}

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_HOST_USER = 'cannametrics24@gmail.com'
EMAIL_HOST_PASSWORD = 'eoqinyumvqcactdc'
EMAIL_USE_TLS = True


# SOCIAL_AUTH_POSTGRES_JSONFIELD = True


# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

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


# Internationalization
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_URL = "static/"
MEDIA_URL = "media/"
MEDIA_ROOT = BASE_DIR / "media"
STATIC_ROOT = BASE_DIR / "static_root"
STATICFILES_DIRS = [
    BASE_DIR / "static",
]

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

AUTH_USER_MODEL = "authenticate.CustomUser"

CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",
    "http://localhost:8000",
]


CORS_ALLOWED_WHITELIST = [
    "http://localhost:3000",
    "http://localhost:8000",
]

SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(minutes=60),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=1),
    "UPDATE_REFRESH_TOKENS": True,
    "BLACKLIST_AFTER_ROTATION": True,

    'AUTH_TOKEN_CLASSES': (
        'rest_framework_simplejwt.tokens.AccessToken',
    ),
}


AUTHENTICATION_BACKENDS = (
    'social_core.backends.google.GoogleOAuth2',
    'social_core.backends.facebook.FacebookOAuth2',
    'django.contrib.auth.backends.ModelBackend',
)

SOCIAL_AUTH_GOOGLE_OAUTH2_KEY = '141047345168-cq5s44gpsj3f1msplu5at9be0l6dg37v.apps.googleusercontent.com'
SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET = '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'
SOCIAL_AUTH_GOOGLE_OAUTH2_EXTRA_DATA = ['firstname', 'lastname']
SOCIAL_AUTH_RAISE_EXCEPTIONS = False


SOCIAL_AUTH_FACEBOOK_KEY = '2640038109488773'
SOCIAL_AUTH_FACEBOOK_SECRET = '61934561a676bc597dc37bc121096cd8'
SOCIAL_AUTH_FACEBOOK_PROFILE_EXTRA_PARAMS = {
    'fields': 'email,first_name,last_name'}


white_list = ['http://localhost:8000/api/v1/auth/accounts/profile/',]

DJOSER = {
    "LOGIN_FIELD": "email",
    "SEND_ACTIVATION_EMAIL": True,
    "SEND_CONFIRMATION_EMAIL": True,
    "ACTIVATION_URL": "api/v1/auth/activation/{uid}/{token}/",
    "SOCIAL_AUTH_TOKEN_STRATEGY": 'djoser.social.token.jwt.TokenStrategy',
    "SOCIAL_AUTH_ALLOWED_REDIRECT_URIS": white_list,
    "PASSWORD_RESET_CONFIRM_URL": "/api/v1/auth/reset-password-confirm/{uid}/{token}",
    "SERIALIZERS": {
        "user_create": "authenticate.serializers.UserCreateSerializer",
        "user": "authenticate.serializers.UsersSerializer"
    },

    # "SOCIAL_AUTH_REDIRECT_IS_HTTPS": True
}


USE_X_FORWARDED_HOST = True
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework_simplejwt.authentication.JWTAuthentication",
        "rest_framework.authentication.SessionAuthentication"
    ],
    "DEFAULT_PERMISSION_CLASSES": ["rest_framework.permissions.IsAuthenticated"]
    # ]
}


SITE_ID = 1


class FacebookSettings(BaseSettings):
    FACEBOOK_SECRET: str = '61934561a676bc597dc37bc121096cd8'
    FACEBOOK_APP_ID: int = 2640038109488773
    FACEBOOK_OAUTH_ACCESS_TOKEN: HttpUrl = (
        "https://graph.facebook.com/oauth/access_token"
    )
    FACEBOOK_ACCESS_TOKEN: HttpUrl = "https://graph.facebook.com/v15.0/me"


class GoogleSettings(BaseSettings):
    OAUTH2_CLIENT_ID: str = '141047345168-cq5s44gpsj3f1msplu5at9be0l6dg37v.apps.googleusercontent.com'
    GOOGLE_OAUTH2_CLIENT_SECRET: str = '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'

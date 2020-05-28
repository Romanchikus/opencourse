"""
Django settings for opencourse project.

Generated by 'django-admin startproject' using Django 3.0.5.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.0/ref/settings/
"""

import os
from email.utils import parseaddr

import environ
from django.utils.translation import ugettext_lazy as _

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = environ.Path(__file__) - 3

env = environ.Env()
env.read_env(os.path.join(BASE_DIR, ".env"))
_ENV = env.str("DJANGO_SETTINGS_MODULE", "config.settings.base")

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env.str("DJANGO_SECRET_KEY", default="!!!SET DJANGO_SECRET_KEY!!!",)
# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = env.bool("DJANGO_DEBUG", False)

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    "modeltranslation",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.sites",
    "allauth",
    "allauth.account",
    "allauth.socialaccount",
    "crispy_forms",
    "django_filters",
    "guardian",
    "django_extensions",
    "opencourse.courses.apps.CoursesConfig",
    "opencourse.profiles.apps.ProfilesConfig",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.locale.LocaleMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "config.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [os.path.join(BASE_DIR, "opencourse/templates")],
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

WSGI_APPLICATION = "config.wsgi.application"


# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases

DATABASES = {"default": env.db("DATABASE_URL")}


# Password validation
# https://docs.djangoproject.com/en/3.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",},
]


# Internationalization
# https://docs.djangoproject.com/en/3.0/topics/i18n/

LANGUAGES = (
    ("en", _("English")),
    ("fr", _("French")),
)
LANGUAGE_CODE = "fr"
MODELTRANSLATION_FALLBACK_LANGUAGES = ["en", "fr"]
LOCALE_PATHS = [os.path.join(BASE_DIR, "locale/")]

TIME_ZONE = "UTC"

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.0/howto/static-files/

STATIC_URL = "/static/"
STATICFILES_DIRS = [str(BASE_DIR("opencourse/static"))]
STATIC_ROOT = str(BASE_DIR("static"))

MEDIA_URL = "/media/"
MEDIA_ROOT = str(BASE_DIR("media"))

# Project adjustments
AUTH_USER_MODEL = "profiles.User"
admins_data = env.tuple(
    "DJANGO_ADMINS", default="Open Course <opencourse2020@mail.com>"
)
ADMINS = tuple(parseaddr(email) for email in admins_data)

# Third-party opencourse settings
AUTHENTICATION_BACKENDS = (
    "django.contrib.auth.backends.ModelBackend",
    "allauth.account.auth_backends.AuthenticationBackend",
    "guardian.backends.ObjectPermissionBackend",
)
SITE_ID = 1
CRISPY_TEMPLATE_PACK = "bootstrap4"

ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_AUTHENTICATION_METHOD = "email"
ACCOUNT_EMAIL_VERIFICATION = "mandatory"
ACCOUNT_FORMS = {"signup": "opencourse.profiles.forms.ProfileCreateForm"}
LOGIN_REDIRECT_URL = "profiles:dispatch_login"

ACCOUNT_LOGOUT_REDIRECT_URL = "account_login"

GUARDIAN_RENDER_403 = True
GUARDIAN_TEMPLATE_403 = "profiles/403.html"
GUARDIAN_MONKEY_PATCH = False

# Security settings
CSRF_COOKIE_HTTPONLY = True
ADMIN_URL = "admin/"

# Delete on production
ACCOUNT_LOGOUT_ON_GET = True

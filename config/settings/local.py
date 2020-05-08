from .base import *  # noqa
from .base import env

DEBUG = True
SECRET_KEY = env("DJANGO_SECRET_KEY", default="!!!SET DJANGO_SECRET_KEY!!!",)
ALLOWED_HOSTS = ["localhost", "0.0.0.0", "127.0.0.1"]

INSTALLED_APPS += [
    # "debug_toolbar",
    "django_extensions",
]
MIDDLEWARE += [
    # "debug_toolbar.middleware.DebugToolbarMiddleware",
]
INTERNAL_IPS = [
    "127.0.0.1",
]
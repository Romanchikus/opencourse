from .base import *  # noqa
from .base import env

DEBUG = True
SECRET_KEY = env("DJANGO_SECRET_KEY", default="!!!SET DJANGO_SECRET_KEY!!!",)

INSTALLED_APPS += [
    "debug_toolbar",
]
MIDDLEWARE += [
    "debug_toolbar.middleware.DebugToolbarMiddleware",
]
INTERNAL_IPS = [
    "127.0.0.1",
]

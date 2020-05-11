from django.contrib import admin
from django.contrib.sites.models import Site
from . import models

admin.site.register(models.Professor)
admin.site.register(models.Student)
admin.site.register(models.Review)

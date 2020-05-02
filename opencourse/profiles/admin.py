from django.contrib import admin
from opencourse.profiles import models

admin.site.register(models.Professor)
admin.site.register(models.Student)
admin.site.register(models.Review)

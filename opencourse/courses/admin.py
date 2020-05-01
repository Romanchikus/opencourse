from django.contrib import admin
from opencourse.courses import models

admin.site.register(models.Course)
admin.site.register(models.CourseLocation)

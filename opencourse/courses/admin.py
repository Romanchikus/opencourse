from django.contrib import admin
from django.contrib.auth.models import Permission

from opencourse.courses import models


class CourseInline(admin.TabularInline):
    model = models.CourseLocation


class CourseAdmin(admin.ModelAdmin):
    inlines = [
        CourseInline,
    ]


admin.site.register(models.Course, CourseAdmin)
admin.site.register(models.Currency)
admin.site.register(Permission)

admin.site.register(models.CourseArea)
admin.site.register(models.City)
admin.site.register(models.CourseLevel)
admin.site.register(models.CourseAge)
admin.site.register(models.CourseLanguage)
admin.site.register(models.CourseLocationType)

from django.contrib import admin
from opencourse.courses import models


class CourseInline(admin.TabularInline):
    model = models.CourseLocation


class CourseAdmin(admin.ModelAdmin):
    inlines = [
        CourseInline,
    ]


admin.site.register(models.Course, CourseAdmin)
admin.site.register(models.CourseLocation)
admin.site.register(models.Currency)

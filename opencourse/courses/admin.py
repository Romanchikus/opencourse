from django.contrib import admin
from modeltranslation.admin import TranslationAdmin
from opencourse.courses import models


class CourseInline(admin.TabularInline):
    model = models.CourseLocation


class CourseAdmin(admin.ModelAdmin):
    inlines = [
        CourseInline,
    ]


admin.site.register(models.Course, CourseAdmin)
admin.site.register(models.Currency)

admin.site.register(models.CourseArea, TranslationAdmin)
admin.site.register(models.City, TranslationAdmin)
admin.site.register(models.CourseLevel, TranslationAdmin)
admin.site.register(models.CourseAge, TranslationAdmin)
admin.site.register(models.CourseLanguage, TranslationAdmin)
admin.site.register(models.CourseLocationType, TranslationAdmin)

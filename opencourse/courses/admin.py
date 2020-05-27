from django.contrib import admin
from guardian.admin import GuardedModelAdmin
from opencourse.courses import models


class CourseInline(admin.TabularInline):
    model = models.CourseLocation


class CourseAdmin(GuardedModelAdmin):
    inlines = [
        CourseInline,
    ]


model_objects = (
    models.Course,
    models.CourseArea,
    models.City,
    models.CourseLevel,
    models.CourseAge,
    models.CourseLanguage,
    models.CourseLocationType,
    models.Currency,
    models.CourseDuration,
    models.Enrollment,
    models.HandoutSection,
    models.Handout,
)

for m in model_objects:
    admin.site.register(m, type(m.__name__ + "Admin", (admin.ModelAdmin,), {}))

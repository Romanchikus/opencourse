from django.contrib import admin
from . import models

model_objects = (
    models.Professor,
    models.Student,
    models.Review,
    models.User,
)

for m in model_objects:
    admin.site.register(m)

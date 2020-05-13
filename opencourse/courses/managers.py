from django.db import models


class CourseManager(models.Manager):
    use_for_related_fields = True

    def created_by(self, professor):
        return self.filter(professor=professor)

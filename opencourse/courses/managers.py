from django.db import models


class CourseManager(models.Manager):
    use_for_related_fields = True

    def created_by(self, professor):
        return self.filter(professor=professor)


class EnrollmentManager(models.Manager):
    use_for_related_fields = True

    def created_by(self, student):
        return self.filter(student=student)


class HandoutManager(models.Manager):
    use_for_related_fields = True

    def created_by(self, professor):
        return self.filter(professor=professor)


class CenterManager(models.Manager):
    use_for_related_fields = True

    def created_by(self, admin):
        return self.filter(admin=admin)


class JoinRequestManager(models.Manager):
    use_for_related_fields = True

    def created_by(self, professor):
        return self.filter(professor=professor)

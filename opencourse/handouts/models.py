from django.db import models
from django.utils.translation import ugettext_lazy as _
from autoslug import AutoSlugField
from opencourse.courses.models import Course
from opencourse.profiles.models import Student
from django.urls import reverse
from .managers import *


class Enrollment(models.Model):

    slug = AutoSlugField(unique=True)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    is_active = models.NullBooleanField(default=None)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)

    objects = EnrollmentManager()

    class Meta:
        verbose_name = _("Enrollment")
        verbose_name_plural = _("Enrollment")
        permissions = (("manage_enrollment", _("Manage enrollment")),)

    def __str__(self):
        return "Enrollment_of_{}".format(self.student)


class HandoutSection(models.Model):
    name = models.CharField(max_length=40)

    def __str__(self):
        return str(self.name)


class Handout(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    name = models.CharField(max_length=40)
    description = models.TextField(max_length=255, blank=True, null=True)
    attachment = models.FileField(upload_to="handouts/%Y-%m-%d/")
    section = models.ForeignKey(HandoutSection, on_delete=models.PROTECT)

    objects = HandoutManager()

    class Meta:
        verbose_name = _("Handout")
        verbose_name_plural = _("Handout")
        permissions = (("manage_handout", _("Manage handout")),)

    def __str__(self):
        return str(self.name)

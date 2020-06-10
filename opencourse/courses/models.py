from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.utils import timezone

from . import managers
from opencourse.profiles.models import Professor, Student


class City(models.Model):
    codepostal = models.CharField(max_length=8, blank=True, null=True)
    name = models.CharField(max_length=60, blank=True, null=True)
    latitude_south = models.DecimalField(
        blank=True, null=True, max_digits=8, decimal_places=4
    )
    latitude_north = models.DecimalField(
        blank=True, null=True, max_digits=8, decimal_places=4
    )
    longitude_west = models.DecimalField(
        blank=True, null=True, max_digits=8, decimal_places=4
    )
    longitude_east = models.DecimalField(
        blank=True, null=True, max_digits=8, decimal_places=4
    )
    latitude_southa = models.DecimalField(
        blank=True, null=True, max_digits=8, decimal_places=4
    )
    latitude_northa = models.DecimalField(
        blank=True, null=True, max_digits=8, decimal_places=4
    )
    longitude_westa = models.DecimalField(
        blank=True, null=True, max_digits=8, decimal_places=4
    )
    longitude_easta = models.DecimalField(
        blank=True, null=True, max_digits=8, decimal_places=4
    )
    category_1 = models.SmallIntegerField(blank=True, null=True)
    category_2 = models.SmallIntegerField(blank=True, null=True)

    class Meta:
        verbose_name = _("City")
        verbose_name_plural = _("Cities")

    def __str__(self):
        return str(self.name)


class CourseLevel(models.Model):
    name = models.CharField(max_length=30, blank=True, null=True)
    description = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        verbose_name = _("Level")
        verbose_name_plural = _("Levels")

    def __str__(self):
        return str(self.name)


class CourseDuration(models.Model):
    duration = models.SmallIntegerField(blank=True, null=True)

    class Meta:
        verbose_name = _("Duration")
        verbose_name_plural = _("Durations")

    def __str__(self):
        return f"{self.duration} {_('minutes')}"


class CourseAge(models.Model):
    max = models.SmallIntegerField(blank=True, null=True)
    name = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        verbose_name = _("Age")
        verbose_name_plural = _("Ages")

    def __str__(self):
        return str(self.name)


class CourseArea(models.Model):
    name = models.CharField(max_length=30, blank=True, null=True)
    description = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        verbose_name = _("Area")
        verbose_name_plural = _("Areas")

    def __str__(self):
        return str(self.name)


class CourseLanguage(models.Model):
    name = models.CharField(max_length=30, blank=True, null=True)
    tag = models.CharField(max_length=2, blank=True, null=True)

    class Meta:
        verbose_name = _("Language")
        verbose_name_plural = _("Languages")

    def __str__(self):
        return str(self.name)


class Center(models.Model):
    admin = models.ForeignKey(Professor, on_delete=models.CASCADE)
    name = models.CharField(max_length=40)
    description = models.TextField(max_length=255, blank=True, null=True)
    picture = models.ImageField(
        upload_to="center_pics/%Y-%m-%d/", null=True, blank=True
    )
    created = models.DateTimeField(auto_now=True, blank=True, null=True)

    objects = managers.CenterManager()

    class Meta:
        verbose_name = _("Center")
        verbose_name_plural = _("Centers")
        permissions = (("manage_center", _("Manage center")),)

    def __str__(self):
        return str(self.name)


class Course(models.Model):
    professor = models.ForeignKey(Professor, on_delete=models.CASCADE)
    city = models.ForeignKey(City, on_delete=models.CASCADE, null=True)
    title = models.CharField(max_length=100)
    descrip = models.TextField(blank=True)
    extrainfo = models.CharField(max_length=250, blank=True, null=True)
    payactive = models.NullBooleanField()
    active = models.NullBooleanField()
    dateexp = models.DateTimeField(blank=True, null=True)
    starthostdate = models.DateTimeField(blank=True, null=True)
    endhostdate = models.DateTimeField(blank=True, null=True)
    hosted = models.NullBooleanField()
    hostactive = models.NullBooleanField()
    level = models.ForeignKey(CourseLevel, on_delete=models.SET_NULL, null=True)
    duration = models.ForeignKey(CourseDuration, on_delete=models.PROTECT, null=True)
    age = models.ManyToManyField(CourseAge)
    area = models.ManyToManyField(CourseArea)
    language = models.ManyToManyField(CourseLanguage)
    center = models.ForeignKey(Center, on_delete=models.SET_NULL, null=True)

    objects = managers.CourseManager()

    class Meta:
        verbose_name = _("Course")
        verbose_name_plural = _("Courses")
        permissions = (("manage_course", _("Manage course")),)

    def __str__(self):
        return self.title or ""


class CourseLocationType(models.Model):
    name = models.CharField(max_length=25)

    class Meta:
        verbose_name = _("Location Type")
        verbose_name_plural = _("Location Types")

    def __str__(self):
        return str(self.name)


class Currency(models.Model):
    name = models.CharField(max_length=20)
    iso_code = models.CharField(max_length=5)
    symbol = models.CharField(max_length=5)

    class Meta:
        verbose_name = _("Currency")
        verbose_name_plural = _("Currencies")

    def __str__(self):
        return self.symbol


class CourseLocation(models.Model):
    location_type = models.ForeignKey(
        CourseLocationType, on_delete=models.PROTECT, null=True
    )
    course = models.ForeignKey(
        Course, on_delete=models.CASCADE, related_name="locations"
    )
    description = models.CharField(max_length=100, blank=True, null=True)
    price = models.SmallIntegerField()
    currency = models.ForeignKey(Currency, on_delete=models.PROTECT)
    number_sessions = models.SmallIntegerField(blank=True, null=True)
    coursestartdate = models.DateTimeField(blank=True, null=True)
    courseenddate = models.DateTimeField(blank=True, null=True)

    class Meta:
        verbose_name = _("Location")
        verbose_name_plural = _("Locations")

    def __str__(self):
        return f"{self.location_type.name}: {self.price}{self.currency}"


class Enrollment(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    accepted = models.NullBooleanField()
    student = models.ForeignKey(Student, on_delete=models.CASCADE)

    objects = managers.EnrollmentManager()

    class Meta:
        verbose_name = _("Enrollment")
        verbose_name_plural = _("Enrollment")
        permissions = (("manage_enrollment", _("Manage enrollment")),)
        unique_together = ("course", "student")

    def __str__(self):
        return "{}: {} ({})".format(self.course, self.student, self.accepted)


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

    objects = managers.HandoutManager()

    class Meta:
        verbose_name = _("Handout")
        verbose_name_plural = _("Handout")
        permissions = (("manage_handout", _("Manage handout")),)

    def __str__(self):
        return str(self.name)


class JoinRequest(models.Model):
    center = models.ForeignKey(Center, on_delete=models.CASCADE)
    professor = models.ForeignKey(Professor, on_delete=models.CASCADE)
    accepted = models.NullBooleanField()

    objects = managers.JoinRequestManager()

    class Meta:
        verbose_name = _("Join request")
        verbose_name_plural = _("Join requests")
        permissions = (("manage_join_request", _("Manage join request")),)
        unique_together = ("center", "professor")

    def __str__(self):
        return "{}: {} ({})".format(self.center, self.professor, self.accepted)

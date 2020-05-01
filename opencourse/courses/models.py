from django.db import models
from opencourse.profiles.models import Professor


class City(models.Model):
    codepostal = models.CharField(max_length=8, blank=True, null=True)
    name = models.CharField(max_length=60, blank=True, null=True)
    name_ar = models.CharField(max_length=70, blank=True, null=True)
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

    def __str__(self):
        return self.name


class CourseLevel(models.Model):
    name = models.CharField(max_length=30, blank=True, null=True)
    name_ar = models.CharField(max_length=45, blank=True, null=True)
    description = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.name


class CourseDuration(models.Model):
    duration = models.SmallIntegerField(blank=True, null=True)

    def __str__(self):
        return f"{self.duration} minutes"


class CourseAge(models.Model):
    max = models.SmallIntegerField(blank=True, null=True)
    name = models.CharField(max_length=20, blank=True, null=True)
    name_ar = models.CharField(max_length=20, blank=True, null=True)

    def __str__(self):
        return self.name


class CourseArea(models.Model):
    name = models.CharField(max_length=30, blank=True, null=True)
    name_ar = models.CharField(max_length=45, blank=True, null=True)
    description = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.name


class CourseLanguage(models.Model):
    origin = models.CharField(max_length=30, blank=True, null=True)
    ar = models.CharField(max_length=30, blank=True, null=True)
    fr = models.CharField(max_length=30, blank=True, null=True)
    tag = models.CharField(max_length=2, blank=True, null=True)

    def __str__(self):
        return self.origin


class Course(models.Model):
    professor = models.ForeignKey(Professor, on_delete=models.CASCADE)
    city = models.ForeignKey(City, on_delete=models.CASCADE, null=True)
    title = models.CharField(max_length=100, blank=True, null=True)
    title_ar = models.CharField(max_length=100, blank=True, null=True)
    descrip = models.TextField(blank=True, null=True)
    extrainfo = models.CharField(max_length=250, blank=True, null=True)
    payactive = models.NullBooleanField()
    active = models.NullBooleanField()
    dateexp = models.DateTimeField(blank=True, null=True)
    starthostdate = models.DateTimeField(blank=True, null=True)
    endhostdate = models.DateTimeField(blank=True, null=True)
    hosted = models.NullBooleanField()
    hostactive = models.NullBooleanField()
    level = models.ForeignKey(CourseLevel, on_delete=models.PROTECT, null=True)
    duration = models.ForeignKey(CourseDuration, on_delete=models.PROTECT, null=True)
    age = models.ManyToManyField(CourseAge)
    area = models.ManyToManyField(CourseArea)
    language = models.ManyToManyField(CourseLanguage)

    def __str__(self):
        return self.title or ""


class CourseLocation(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    name = models.CharField(max_length=25, blank=True, null=True)
    name_ar = models.CharField(max_length=20, blank=True, null=True)
    description = models.CharField(max_length=100, blank=True, null=True)
    price = models.SmallIntegerField(blank=True, null=True)
    currency = models.CharField(max_length=23, blank=True, null=True)
    number_sessions = models.SmallIntegerField(blank=True, null=True)
    coursestartdate = models.DateTimeField(blank=True, null=True)
    courseenddate = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return self.name

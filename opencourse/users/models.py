from django.db import models


class Visitor(models.Model):
    first_name_ar = models.CharField(max_length=10, blank=True, null=True)
    last_name_ar = models.CharField(max_length=100, blank=True, null=True)
    address = models.CharField(max_length=255, blank=True, null=True)
    city = models.CharField(max_length=60, blank=True, null=True)
    dob = models.DateTimeField(blank=True, null=True)
    picture = models.CharField(max_length=20, blank=True, null=True)
    edulevel = models.CharField(max_length=100, blank=True, null=True)
    tel = models.CharField(max_length=20, blank=True, null=True)
    whatsapp = models.CharField(max_length=20, blank=True, null=True)
    email = models.CharField(max_length=60, blank=True, null=True)
    dateadd = models.DateTimeField(blank=True, null=True)

    class Meta:
        abstract = True


class Student(Visitor):
    pass


class Professor(Visitor):
    bio = models.CharField(max_length=255, blank=True, null=True)
    yearsexperience = models.SmallIntegerField(blank=True, null=True)
    act_position = models.CharField(max_length=100, blank=True, null=True)
    dateexpir = models.DateTimeField(blank=True, null=True)
    listed = models.NullBooleanField()
    feespaid = models.NullBooleanField()

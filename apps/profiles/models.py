import uuid
from django.db import models
from django.conf import settings


class Profile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, primary_key=True
    )
    slug = models.UUIDField(default=uuid.uuid4, blank=True, editable=False)
    picture = models.ImageField(
        "Profile picture", upload_to="profile_pics/%Y-%m-%d/", null=True, blank=True
    )
    email_verified = models.BooleanField("Email verified", default=False)

    first_name_ar = models.CharField(max_length=10, blank=True, null=True)
    last_name_ar = models.CharField(max_length=100, blank=True, null=True)
    address = models.CharField(max_length=255, blank=True, null=True)
    city = models.CharField(max_length=60, blank=True, null=True)
    dob = models.DateTimeField(blank=True, null=True)
    edulevel = models.CharField(max_length=100, blank=True, null=True)
    tel = models.CharField(max_length=20, blank=True, null=True)
    whatsapp = models.CharField(max_length=20, blank=True, null=True)
    email = models.CharField(max_length=60, blank=True, null=True)
    dateadd = models.DateTimeField(blank=True, null=True)

    class Meta:
        abstract = True


class Student(Profile):
    pass


class Professor(Profile):
    bio = models.CharField(max_length=255, blank=True, null=True)
    yearsexperience = models.SmallIntegerField(blank=True, null=True)
    act_position = models.CharField(max_length=100, blank=True, null=True)
    dateexpir = models.DateTimeField(blank=True, null=True)
    listed = models.NullBooleanField()
    feespaid = models.NullBooleanField()

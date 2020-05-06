import uuid
from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.utils.translation import ugettext_lazy as _


class User(AbstractUser):
    @property
    def profile(self):
        if hasattr(self, "professor"):
            return self.professor
        elif hasattr(self, "student"):
            return self.student
        else:
            return self

    @property
    def is_professor(self):
        if hasattr(self, "professor"):
            return True
        return False

    @property
    def is_student(self):
        if hasattr(self, "student"):
            return True
        return False


class Profile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE
    )
    slug = models.UUIDField(default=uuid.uuid4, blank=True, editable=False)
    picture = models.ImageField(
        _("Profile picture"), upload_to="profile_pics/%Y-%m-%d/", null=True, blank=True
    )
    email_verified = models.BooleanField(_("Email verified"), default=False)

    first_name_ar = models.CharField(max_length=10, blank=True, null=True)
    last_name_ar = models.CharField(max_length=100, blank=True, null=True)
    address = models.CharField(max_length=255, blank=True, null=True)
    city = models.CharField(max_length=60, blank=True, null=True)
    dob = models.DateField(blank=True, null=True)
    edulevel = models.TextField(max_length=1000, blank=True, null=True)
    tel = models.CharField(max_length=20)
    whatsapp = models.CharField(max_length=20, blank=True, null=True)
    email = models.CharField(max_length=60, blank=True, null=True)
    dateadd = models.DateTimeField(blank=True, null=True)
    contacts_requests = models.PositiveIntegerField(null=True)

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name} ({self.user.email})"

    class Meta:
        abstract = True


class Student(Profile):
    pass


class Professor(Profile):
    bio = models.TextField(max_length=1000, blank=True, null=True)
    yearsexperience = models.SmallIntegerField(blank=True, null=True)
    act_position = models.CharField(max_length=100, blank=True, null=True)
    dateexpir = models.DateTimeField(blank=True, null=True)
    listed = models.NullBooleanField()
    feespaid = models.NullBooleanField()


class Review(models.Model):
    professor = models.ForeignKey(Professor, on_delete=models.CASCADE)
    score = models.PositiveSmallIntegerField()
    text = models.TextField()

    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    author_id = models.PositiveIntegerField()
    author = GenericForeignKey("content_type", "author_id")

    def __str__(self):
        return self.text

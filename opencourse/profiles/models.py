from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.utils.translation import ugettext_lazy as _
from guardian.mixins import GuardianUserMixin


class User(GuardianUserMixin, AbstractUser):
    @property
    def profile(self):
        if hasattr(self, "professor"):
            return self.professor
        elif hasattr(self, "student"):
            return self.student
        else:
            return self

    @property
    def is_student(self):
        return hasattr(self, "student")

    class Meta(AbstractUser.Meta):
        permissions = (
            ("access_professor_pages", _("Access professor pages")),
            ("access_student_pages", _("Access student pages")),
        )


class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    picture = models.ImageField(
        _("Profile picture"), upload_to="profile_pics/%Y-%m-%d/", null=True, blank=True,
    )
    email_verified = models.BooleanField(_("Email verified"), default=False)

    address = models.CharField(max_length=255, blank=True, null=True)
    city = models.CharField(max_length=60, blank=True, null=True)
    dob = models.DateField(blank=True, null=True)
    edulevel = models.TextField(max_length=1000, blank=True, null=True)
    tel = models.CharField(max_length=20)
    whatsapp = models.CharField(max_length=20, blank=True, null=True)
    email = models.CharField(max_length=60, blank=True, null=True)
    dateadd = models.DateTimeField(blank=True, null=True)
    contacts_requests = models.PositiveIntegerField(default=0)

    def __str__(self):
        if self.user.first_name or self.user.last_name:
            return f"{self.user.first_name} {self.user.last_name}"
        return self.user.username

    class Meta:
        abstract = True


class Student(Profile):
    class Meta(Profile.Meta):
        verbose_name = _("Student")
        verbose_name_plural = _("Students")


class Professor(Profile):
    bio = models.TextField(max_length=1000, blank=True, null=True)
    yearsexperience = models.SmallIntegerField(blank=True, null=True)
    act_position = models.CharField(max_length=100, blank=True, null=True)
    dateexpir = models.DateTimeField(blank=True, null=True)
    listed = models.NullBooleanField()
    feespaid = models.NullBooleanField()

    class Meta(Profile.Meta):
        verbose_name = _("Professor")
        verbose_name_plural = _("Professors")

    @property
    def average_score(self):
        reviews = self.review_set.all()
        score = reviews.aggregate(models.Avg("score"))["score__avg"]
        return score


class Review(models.Model):
    professor = models.ForeignKey(Professor, on_delete=models.CASCADE)
    score = models.PositiveSmallIntegerField()
    text = models.TextField()

    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    author_id = models.PositiveIntegerField()
    author = GenericForeignKey("content_type", "author_id")

    class Meta:
        verbose_name = _("Review")
        verbose_name_plural = _("Reviews")

    def __str__(self):
        return self.text

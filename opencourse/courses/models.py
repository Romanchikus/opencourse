from django.db import models
from opencourse.users.models import Professor


class City(models.Model):
    codepostal = models.CharField(max_length=8, blank=True, null=True)
    name = models.CharField(max_length=60, blank=True, null=True)
    name_ar = models.CharField(max_length=70, blank=True, null=True)
    latitude_south = models.DecimalField(blank=True, null=True, max_digits=8, decimal_places=4)
    latitude_north = models.DecimalField(blank=True, null=True, max_digits=8, decimal_places=4)
    longitude_west = models.DecimalField(blank=True, null=True, max_digits=8, decimal_places=4)
    longitude_east = models.DecimalField(blank=True, null=True, max_digits=8, decimal_places=4)
    latitude_southa = models.DecimalField(blank=True, null=True, max_digits=8, decimal_places=4)
    latitude_northa = models.DecimalField(blank=True, null=True, max_digits=8, decimal_places=4)
    longitude_westa = models.DecimalField(blank=True, null=True, max_digits=8, decimal_places=4)
    longitude_easta = models.DecimalField(blank=True, null=True, max_digits=8, decimal_places=4)
    category_1 = models.SmallIntegerField(blank=True, null=True)
    category_2 = models.SmallIntegerField(blank=True, null=True)

    def __str__(self):
        return self.name


class Course(models.Model):
    professor = models.ForeignKey(Professor, on_delete=models.CASCADE)
    city = models.ForeignKey(City, on_delete=models.CASCADE)
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

    def __str__(self):
        return self.title or ""
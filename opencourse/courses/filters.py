from django.utils.translation import ugettext_lazy as _
import django_filters
from . import models


class CourseFilter(django_filters.FilterSet):
    class Meta:
        model = models.Course
        fields = [
            "area",
            "city",
            "center",
            "level",
            "age",
            "language",
            "locations__location_type",
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        labels = {
            "area": _("Area"),
            "city": _("City"),
            "center": _("Center"),
            "level": _("Level"),
            "age": _("Age"),
            "language": _("Language"),
            "locations__location_type": _("Location"),
        }
        for filt in self.filters.values():
            filt.label = labels[filt.field_name]


class CenterFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(lookup_expr="icontains")

    class Meta:
        model = models.Center
        fields = [
            "name",
        ]

from django.utils.translation import ugettext_lazy as _
import django_filters
from . import models


class CenterFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(lookup_expr="icontains")

    class Meta:
        model = models.Center
        fields = [
            "name",
        ]

from django.urls import include, path
from opencourse.users.views import IndexView

urlpatterns = [
    path('', IndexView.as_view(), name="index"),
]
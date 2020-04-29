from django.urls import path
from apps.profiles import views

app_name = "profiles"
urlpatterns = [
    path("", views.ProfileView.as_view(), name="profile"),
    path("professor/", views.ProfessorUpdateView.as_view(), name="professor"),
]

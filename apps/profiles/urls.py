from django.urls import path
from apps.profiles import views

app_name = "profiles"
urlpatterns = [
    path("profile/professor/", views.ProfessorUpdateView.as_view(), name="professor_update"),
]

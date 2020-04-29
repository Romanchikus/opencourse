from django.urls import path
from apps.users import views

app_name = "users"
urlpatterns = [
    path("profile/professor/", views.ProfessorUpdateView.as_view(), name="professor_update"),
]

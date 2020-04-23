from django.urls import path
from opencourse.users import views

app_name = "users"
urlpatterns = [
    path("signup/", views.SignUpView.as_view(), name="signup"),
    path("login/", views.LoginView.as_view(), name="login"),
    path("logout/", views.LogoutView.as_view(), name="logout"),
    path("profile/professor/", views.ProfessorUpdateView.as_view(), name="professor_update"),
]

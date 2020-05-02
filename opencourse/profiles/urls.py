from django.urls import path
from opencourse.profiles import views

app_name = "profiles"
urlpatterns = [
    path("", views.ProfileView.as_view(), name="profile"),
    path("dispatch-login/", views.DispatchLoginView.as_view(), name="dispatch_login"),
    path("professor/", views.ProfessorUpdateView.as_view(), name="professor"),
    path(
        "professor/<int:professor_pk>/",
        views.ProfessorDetailView.as_view(),
        name="professor_detail",
    ),
    path(
        "professor/<int:professor_pk>/add-review",
        views.ReviewCreateView.as_view(),
        name="review_create",
    ),
    path("student/", views.StudentUpdateView.as_view(), name="student"),
]

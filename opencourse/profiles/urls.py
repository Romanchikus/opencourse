from django.urls import path
from . import views

app_name = "profiles"
urlpatterns = [
    path("", views.ProfileView.as_view(), name="profile"),
    path("dispatch-login/", views.DispatchLoginView.as_view(), name="dispatch_login",),
    path("professor/", views.ProfessorUpdateView.as_view(), name="professor"),
    path(
        "professor/<int:pk>/add-review",
        views.ReviewCreateView.as_view(),
        name="review_create",
    ),
    path(
        "professor/<int:pk>/contact-request/",
        views.ContactRequestView.as_view(),
        name="contact_request",
    ),
    path("student/", views.StudentUpdateView.as_view(), name="student"),
    path("403/", views.ForbiddenView.as_view(), name="403"),
]

from django.urls import path, include
from . import views

app_name = "profiles"
profile_patterns = [
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

center_patterns = [
    path("list/", views.CenterListView.as_view(), name="list"),
    path("create/", views.CenterCreateView.as_view(), name="create"),
    path("edit/<int:pk>/", views.CenterEditView.as_view(), name="edit"),
    path("delete/<int:pk>/", views.CenterDeleteView.as_view(), name="delete"),
    path("detail/<int:pk>/", views.CenterDetailView.as_view(), name="detail"),
    path(
        "search-results/",
        views.CenterSearchResultsView.as_view(),
        name="search_results",
    ),
]

join_request_patterns = [
    path("admin/", views.JoinRequestrListView.as_view(), name="admin_list"),
    path("create/", views.JoinRequestCreateView.as_view(), name="create"),
    path("edit/<int:pk>/", views.JoinRequestUpdateView.as_view(), name="edit"),
]

urlpatterns = [
    path("", include(profile_patterns)),
    path(
        "centers/",
        include((center_patterns, "opencourse.courses"), namespace="centers"),
    ),
    path(
        "join_requests/",
        include(
            (join_request_patterns, "opencourse.courses"), namespace="join_requests"
        ),
    ),
]

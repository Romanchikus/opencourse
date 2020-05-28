from django.urls import path, include
from django.views.generic import RedirectView

from . import views

app_name = "courses"

course_patterns = [
    path("list/", views.CourseListView.as_view(), name="list"),
    path("create/", views.CourseCreateView.as_view(), name="create"),
    path("detail/<int:pk>/", views.CourseDetailView.as_view(), name="detail"),
    path("edit/<int:pk>/", views.CourseEditView.as_view(), name="edit"),
    path("delete/<int:pk>/", views.CourseDeleteView.as_view(), name="delete"),
    path("search/", views.CourseSearchView.as_view(), name="search"),
    path(
        "search-results/",
        views.CourseSearchResultsView.as_view(),
        name="search_results",
    ),
]

enrollment_patterns = [
    path(
        "professor/", views.EnrollmentProfessorListView.as_view(), name="professor_list"
    ),
    path("student/", views.EnrollmentStudentListView.as_view(), name="student_list"),
    path("create", views.EnrollmentCreateView.as_view(), name="create"),
    path("edit/<int:pk>/", views.EnrollmentUpdateStatusView.as_view(), name="edit"),
]

handout_patterns = [
    path(
        "handouts/list/<int:course_pk>/", views.HandoutListView.as_view(), name="list"
    ),
    path(
        "handouts/create/<int:course_pk>/",
        views.HandoutCreateView.as_view(),
        name="create",
    ),
    path("handouts/edit/<int:pk>/", views.HandoutUpdateView.as_view(), name="edit"),
    path("handouts/delete/<int:pk>/", views.HandoutDeleteView.as_view(), name="delete"),
]

urlpatterns = [
    path("", RedirectView.as_view(pattern_name="courses:search")),
    path("", include(course_patterns)),
    path(
        "enrollments/",
        include((enrollment_patterns, "opencourse.courses"), namespace="enrollments"),
    ),
    path(
        "handouts/",
        include((handout_patterns, "opencourse.courses"), namespace="handouts"),
    ),
]

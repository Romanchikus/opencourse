from django.urls import path, include
from . import views

app_name = "courses"

course_patterns = [
    path("create/", views.CourseCreateView.as_view(), name="create"),
    path("list/", views.CourseListView.as_view(), name="list"),
    path("<int:pk>/detail/", views.CourseDetailView.as_view(), name="detail"),
    path("<int:pk>/edit/", views.CourseEditView.as_view(), name="edit"),
    path("<int:pk>/delete/", views.CourseDeleteView.as_view(), name="delete"),
    path("search/", views.CourseSearchView.as_view(), name="search"),
    path(
        "search-results/",
        views.CourseSearchResultsView.as_view(),
        name="search_results",
    ),
]

enrollment_patterns = [
    path(
        "enrollments/professor/",
        views.EnrollmentProfessorListView.as_view(),
        name="enrollment_professor_list",
    ),
    path(
        "enrollments/student/",
        views.EnrollmentStudentListView.as_view(),
        name="enrollment_student_list",
    ),
    path(
        "enrollments/<int:pk>/",
        views.EnrollmentUpdateStatusView.as_view(),
        name="update_enrollment",
    ),
    path(
        "enrollments/create",
        views.EnrollmentCreateView.as_view(),
        name="enrollment_create",
    ),
]

handout_patterns = [
    path("<int:pk>/handouts/", views.HandoutListView.as_view(), name="handout_list",),
    path(
        "<int:pk>/handouts/create/",
        views.HandoutCreateView.as_view(),
        name="handout_create",
    ),
    path(
        "handouts/<int:pk>/update/",
        views.HandoutUpdateView.as_view(),
        name="handout_update",
    ),
    path(
        "handouts/<int:pk>/delete/",
        views.HandoutDeleteView.as_view(),
        name="handout_delete",
    ),
]

urlpatterns = course_patterns + enrollment_patterns + handout_patterns

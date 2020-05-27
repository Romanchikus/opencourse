from django.urls import path, include
from . import views

app_name = "courses"

course_patterns = [
    path("create/", views.CourseCreateView.as_view(), name="create"),
    path("list/", views.CourseListView.as_view(), name="list"),
    path("<slug:slug>/detail/", views.CourseDetailView.as_view(), name="detail"),
    path("<slug:slug>/edit/", views.CourseEditView.as_view(), name="edit"),
    path("<slug:slug>/delete/", views.CourseDeleteView.as_view(), name="delete"),
    path("search/", views.CourseSearchView.as_view(), name="search"),
    path("search-results/", views.CourseSearchResultsView.as_view(), name="search_results",),
]

enrollment_patterns = [
    path("enrollment-list/", views.ProfessorEnrollmentsListView.as_view(), name="enrollment_list"),
    path(
        "enrollments/<slug:slug>/", views.EnrollmentUpdateView.as_view(), name="update_enrollment",
    ),
    path("student_list/", views.StudentEnrollmentsListView.as_view(), name="student_list"),
    path("post/", views.EnrollmentCreateView.as_view(), name="post"),
]

handout_patterns = [
    path("<slug:slug>/handouts/", views.HandoutListView.as_view(), name="list_handouts",),
    path(
        "<slug:slug>/create_handouts/", views.HandoutCreateView.as_view(), name="create_handouts",
    ),
    path(
        "<slug:slug>/create_handouts/", views.HandoutCreateView.as_view(), name="create_handouts",
    ),
    path("<int:pk>/detail_handouts/", views.ShowHandoutView.as_view(), name="detail_handouts",),
    path("<int:pk>/update_handout/", views.HandoutUpdateView.as_view(), name="update_handout",),
    path("<int:pk>/delete_handout/", views.HandoutDeleteView.as_view(), name="delete_handout",),
    path("<int:pk>/download_handout/", views.FileDownloadView.as_view(), name="download_handout",),
]

urlpatterns = course_patterns + enrollment_patterns + handout_patterns

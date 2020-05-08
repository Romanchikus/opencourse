from django.urls import path
from . import views

app_name = "courses"
urlpatterns = [
    path("create/", views.CourseCreateView.as_view(), name="create"),
    path("<slug:slug>/update/", views.CourseUpdateView.as_view(), name="update"),
    path("list/", views.CourseListView.as_view(), name="list"),
    path("search/", views.CourseSearchView.as_view(), name="search"),
    path(
        "search-results/",
        views.CourseSearchResultsView.as_view(),
        name="search_results",
    ),
]

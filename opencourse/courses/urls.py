from django.urls import path
from opencourse.courses import views

app_name = "courses"
urlpatterns = [
    path('create/', views.CourseCreateView.as_view(), name="create"),
    path('list/', views.CourseListView.as_view(), name='list'),
]

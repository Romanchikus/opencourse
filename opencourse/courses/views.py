from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, FormView, UpdateView
from django_filters.views import FilterView

from opencourse.courses import forms, models
from opencourse.courses.mixins import FormsetMixin
from opencourse.profiles.mixins import ProfessorRequiredMixin


class CourseUpdateView(ProfessorRequiredMixin, FormsetMixin, UpdateView):
    model = models.Course
    form_class = forms.CourseForm
    formset_class = forms.CourseLocationFormset
    template_name = "courses/edit.html"
    exclude = ["professor"]
    success_url = reverse_lazy("courses:list")


class CourseCreateView(ProfessorRequiredMixin, FormsetMixin, CreateView):
    form_class = forms.CourseForm
    formset_class = forms.CourseLocationFormset
    template_name = "courses/edit.html"
    exclude = ["professor"]
    success_url = reverse_lazy("courses:list")

    def form_valid(self, form):
        form.instance.professor = self.request.user.professor
        return super().form_valid(form)


class CourseListView(ProfessorRequiredMixin, ListView):
    model = models.Course
    template_name = "courses/list.html"
    paginate_by = 100  # if pagination is desired


class CourseSearchView(FormView):
    template_name = "courses/search.html"
    form_class = forms.CourseSearchForm
    success_url = reverse_lazy("courses:search")


class CourseSearchResultsView(FilterView):
    model = models.Course
    filterset_fields = [
        "area",
        "city",
        "level",
        "age",
        "language",
        "locations__location_type",
    ]
    template_name = "courses/search_results.html"
    paginate_by = 10

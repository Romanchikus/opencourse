from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, FormView
from django_filters.views import FilterView

from opencourse.courses import forms, models


class CourseCreateView(CreateView):
    form_class = forms.CourseForm
    template_name = "courses/create.html"
    exclude = ["professor"]
    success_url = reverse_lazy("courses:list")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.POST:
            context['formset'] = forms.CourseLocationFormset(self.request.POST)
        else:
            context['formset'] = forms.CourseLocationFormset()
        return context

    def form_valid(self, form):
        form.instance.professor = self.request.user.professor
        context = self.get_context_data()
        formset = context['formset']
        if formset.is_valid():
            response = super().form_valid(form)
            formset.instance = self.object
            formset.save()
            return response
        else:
            return super().form_invalid(form)


class CourseListView(ListView):
    model = models.Course
    template_name = "courses/list.html"
    paginate_by = 100  # if pagination is desired


class CourseSearchView(FormView):
    template_name = "courses/search.html"
    form_class = forms.CourseSearchForm
    success_url = reverse_lazy("courses:search")


class CourseSearchResultsView(FilterView):
    model = models.Course
    filterset_fields = ['area', 'city', 'level', 'age', 'language']
    template_name = "courses/search_results.html"
    paginate_by = 10

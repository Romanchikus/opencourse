from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import transaction
from django.http import HttpResponse, HttpResponseForbidden
from django.shortcuts import get_object_or_404
from django.urls import reverse, reverse_lazy
from django.views.generic import (
    CreateView,
    ListView,
    FormView,
    UpdateView,
    DetailView,
    DeleteView,
    View,
)

from django_filters.views import FilterView
from guardian.mixins import PermissionRequiredMixin
from guardian.shortcuts import assign_perm

from . import forms, models, filters
from .mixins import FormsetMixin, JsonFormMixin
from opencourse.profiles.forms import ReviewForm
from opencourse.profiles.mixins import ProfessorRequiredMixin, StudentRequiredMixin

REVIEW_COUNT = 10


class CoursePermissionRequiredMixin(PermissionRequiredMixin):
    permission_required = "courses.manage_course"
    return_403 = True


class CourseEditView(CoursePermissionRequiredMixin, FormsetMixin, UpdateView):
    model = models.Course
    form_class = forms.CourseForm
    formset_class = forms.CourseLocationFormset
    template_name = "courses/course_edit.html"
    exclude = ["professor"]
    success_url = reverse_lazy("courses:list")
    permission_required = "courses.manage_course"
    return_403 = True


class CourseCreateView(ProfessorRequiredMixin, FormsetMixin, CreateView):
    model = models.Course
    form_class = forms.CourseForm
    formset_class = forms.CourseLocationFormset
    template_name = "courses/course_edit.html"
    exclude = ["professor"]
    success_url = reverse_lazy("courses:list")

    def form_valid(self, form):
        with transaction.atomic():
            form.instance.professor = self.request.user.professor
            response = super().form_valid(form)
            course = self.object
            assign_perm("manage_course", course.professor.user, course)
            return response


class CourseListView(ProfessorRequiredMixin, ListView):
    template_name = "courses/course_list.html"
    paginate_by = 100  # if pagination is desired

    def get_queryset(self):
        professor = self.request.user.professor
        return models.Course.objects.created_by(professor=professor)


class CourseDetailView(DetailView):
    model = models.Course
    template_name = "courses/course_detail.html"
    paginate_by = 10

    def get_context_data(self, **kwargs):
        kwargs["review_form"] = ReviewForm()
        kwargs["professor"] = self.object.professor
        kwargs["reviews"] = self.object.professor.review_set.order_by("-id")[
            :REVIEW_COUNT
        ]
        kwargs["enrollment_form"] = forms.EnrollmentCreateForm(
            initial={"course": self.object, "student": self.request.user.student},
        )
        enrollment = models.Enrollment.objects.filter(
            course=self.object, student=self.request.user.student
        ).first()
        kwargs["enrollment_accepted"] = getattr(enrollment, "accepted", "not_existing")

        return super().get_context_data(**kwargs)


class CourseDeleteView(CoursePermissionRequiredMixin, DeleteView):
    model = models.Course
    success_url = reverse_lazy("courses:list")
    template_name = "confirm_delete.html"


class CourseSearchView(FormView):
    template_name = "courses/course_search.html"
    form_class = forms.CourseSearchForm
    success_url = reverse_lazy("courses:search")


class CourseSearchResultsView(FilterView):
    filterset_class = filters.CourseFilter
    template_name = "courses/course_search_results.html"
    paginate_by = 10


class HandoutListView(LoginRequiredMixin, ListView):
    model = models.Handout
    template_name = "courses/handout_list.html"

    def get_queryset(self):
        pk = self.kwargs.get("pk")
        course = get_object_or_404(models.Course, pk=pk)
        object_list = self.model.objects.filter(course=course).order_by("section")
        return object_list

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        pk = self.kwargs.get("pk")
        context["course"] = get_object_or_404(models.Course, pk=pk)
        return context


class HandoutUpdateView(ProfessorRequiredMixin, UpdateView):
    model = models.Handout
    form_class = forms.HandoutForm
    template_name = "courses/handout_edit.html"

    def get_success_url(self):
        handout_pk = self.kwargs.get("pk")
        course = get_object_or_404(models.Course, handout=handout_pk)
        return reverse("courses:handout_list", kwargs={"pk": course.pk})


class HandoutDeleteView(ProfessorRequiredMixin, DeleteView):
    model = models.Handout
    template_name = "confirm_delete.html"

    def get_success_url(self):
        handout_pk = self.kwargs.get("pk")
        course = get_object_or_404(models.Course, handout=handout_pk)
        return reverse("courses:handout_list", kwargs={"pk": course.pk})


class HandoutCreateView(ProfessorRequiredMixin, CreateView):
    model = models.Handout
    form_class = forms.HandoutForm
    template_name = "courses/handout_edit.html"

    def form_valid(self, form):
        pk = self.kwargs.get("pk")
        form.course = get_object_or_404(models.Course, pk=pk)
        form.save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse("courses:handout_list", kwargs={"slug": self.kwargs.get("slug")})


class EnrollmentUpdateStatusView(ProfessorRequiredMixin, JsonFormMixin, UpdateView):
    model = models.Enrollment
    fields = ["accepted"]


class EnrollmentCreateView(LoginRequiredMixin, JsonFormMixin, CreateView):
    model = models.Enrollment
    form_class = forms.EnrollmentCreateForm


class EnrollmentStudentListView(StudentRequiredMixin, ListView):
    model = models.Enrollment
    template_name = "courses/enrollment_list.html"

    def get_queryset(self):
        object_list = self.model.objects.filter(
            student=self.request.user.student, accepted=True
        )
        return object_list


class EnrollmentProfessorListView(ProfessorRequiredMixin, ListView):
    model = models.Enrollment
    template_name = "courses/enrollment_list.html"

    def get_queryset(self):
        object_list = self.model.objects.filter(
            course__professor=self.request.user.professor
        ).order_by("accepted")
        return object_list

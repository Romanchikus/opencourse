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
from opencourse.profiles.models import Student
from .mixins import FormsetMixin, JsonFormMixin
from opencourse.profiles.forms import ReviewForm
from opencourse.profiles.mixins import ProfessorRequiredMixin, StudentRequiredMixin
from django.views.generic.list import MultipleObjectMixin


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

    def get_form_kwargs(self):
        kwargs = super(CourseEditView, self).get_form_kwargs()
        kwargs.update({"professor": self.request.user.professor})
        return kwargs


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

    def get_initial(self):
        initial = {
            "area": 1,
            "level": 1,
            "language": 1,
            "duration": 1,
            "age": 1,
            "city": 1,
            "center": 1,
        }
        return initial

    def get_form_kwargs(self):
        kwargs = super(CourseCreateView, self).get_form_kwargs()
        kwargs.update({"professor": self.request.user.professor})
        return kwargs


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
        kwargs["reviews_count"] = kwargs["reviews"].count()
        student = getattr(self.request.user, "student", None)
        kwargs["enrollment_form"] = forms.EnrollmentCreateForm(
            initial={"course": self.object, "student": student},
        )
        enrollment = models.Enrollment.objects.filter(
            course=self.object, student=student
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
        course_pk = self.kwargs.get("course_pk")
        course = get_object_or_404(models.Course, pk=course_pk)
        object_list = self.model.objects.filter(course=course).order_by("section")
        return object_list

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        course_pk = self.kwargs.get("course_pk")
        context["course"] = get_object_or_404(models.Course, pk=course_pk)
        return context

    def dispatch(self, request, *args, **kwargs):
        if self.request.user.is_student:
            course_pk = self.kwargs.get("course_pk")
            course = get_object_or_404(models.Course, pk=course_pk)
            student = self.request.user.student
            enrollment = models.Enrollment.objects.filter(
                course=course, student=student
            ).first()
            has_access = getattr(enrollment, "accepted", False)
            if not has_access:
                return self.handle_no_permission()
        return super().dispatch(request, *args, **kwargs)


class HandoutUpdateView(ProfessorRequiredMixin, UpdateView):
    model = models.Handout
    form_class = forms.HandoutForm
    template_name = "courses/handout_edit.html"

    def get_success_url(self):
        handout_pk = self.kwargs.get("pk")
        course = get_object_or_404(models.Course, handout=handout_pk)
        return reverse("courses:handouts:list", kwargs={"course_pk": course.pk})


class HandoutDeleteView(ProfessorRequiredMixin, DeleteView):
    model = models.Handout
    template_name = "confirm_delete.html"

    def get_success_url(self):
        handout_pk = self.kwargs.get("pk")
        course = get_object_or_404(models.Course, handout=handout_pk)
        return reverse("courses:handouts:list", kwargs={"course_pk": course.pk})


class HandoutCreateView(ProfessorRequiredMixin, CreateView):
    model = models.Handout
    form_class = forms.HandoutForm
    template_name = "courses/handout_edit.html"

    def form_valid(self, form):
        course_pk = self.kwargs.get("course_pk")
        form.instance.course = get_object_or_404(models.Course, pk=course_pk)
        form.save()
        return super().form_valid(form)

    def get_success_url(self):
        course_pk = self.kwargs.get("course_pk")
        return reverse("courses:handouts:list", kwargs={"course_pk": course_pk})


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


class CourseStudentsListView(ProfessorRequiredMixin, ListView):
    model = models.Course
    template_name = "courses/course_students_list.html"
    paginate_by = 100  # if pagination is desired

    def get_queryset(self):
        course = get_object_or_404(models.Course, pk=self.kwargs.get("pk"))
        students = Student.objects.filter(
            enrollment__course=course, enrollment__accepted=True
        )
        return students


class CenterCreateView(ProfessorRequiredMixin, CreateView):
    model = models.Center
    template_name = "courses/center_edit.html"
    form_class = forms.CenterForm
    success_url = reverse_lazy("courses:centers:list")

    def form_valid(self, form):
        form.instance.admin = self.request.user.professor
        form.save()
        return super().form_valid(form)


class CenterEditView(ProfessorRequiredMixin, UpdateView):
    model = models.Center
    template_name = "courses/center_edit.html"
    form_class = forms.CenterForm
    success_url = reverse_lazy("courses:centers:list")

    def form_valid(self, form):
        form.instance.admin = self.request.user.professor
        form.save()
        return super().form_valid(form)


class CenterListView(ProfessorRequiredMixin, ListView):
    template_name = "courses/centers_list.html"

    def get_queryset(self, *args, **kwargs):
        professor = self.request.user.professor
        return models.Center.objects.created_by(admin=professor)

    def get_context_data(self, **kwargs):
        professor = getattr(self.request.user, "professor", None)
        kwargs["join_centers"] = models.JoinRequest.objects.filter(
            professor=professor, accepted=True
        )

        return super().get_context_data(**kwargs)


class CenterDetailView(DetailView, MultipleObjectMixin):
    model = models.Center
    template_name = "courses/center_detail.html"
    paginate_by = 3

    def get_context_data(self, **kwargs):
        professor = getattr(self.request.user, "professor", None)
        kwargs["join_request_form"] = forms.JoinRequestCreateForm(
            initial={"center": self.object, "professor": professor},
        )
        join_request = models.JoinRequest.objects.filter(
            center=self.object, professor=professor
        ).first()
        kwargs["join_request_accepted"] = getattr(
            join_request, "accepted", "not_existing"
        )
        object_list = models.Course.objects.filter(center=self.get_object())
        return super(CenterDetailView, self).get_context_data(
            object_list=object_list, **kwargs
        )


class CenterDeleteView(ProfessorRequiredMixin, DeleteView):
    model = models.Center
    success_url = reverse_lazy("courses:centers:list")
    template_name = "confirm_delete.html"


class CenterSearchResultsView(FilterView):
    filterset_class = filters.CenterFilter
    template_name = "courses/center_search_results.html"
    paginate_by = 10


class JoinRequestCreateView(ProfessorRequiredMixin, JsonFormMixin, CreateView):
    model = models.JoinRequest
    form_class = forms.JoinRequestCreateForm


class JoinRequestUpdateView(ProfessorRequiredMixin, JsonFormMixin, UpdateView):
    model = models.JoinRequest
    fields = ["accepted"]


class JoinRequestrListView(ProfessorRequiredMixin, ListView):
    model = models.JoinRequest
    template_name = "courses/join_request_list.html"
    paginate_by = 15

    def get_queryset(self):
        object_list = self.model.objects.filter(
            center__admin=self.request.user.professor
        ).order_by("accepted")
        return object_list

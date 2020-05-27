from django.db import transaction
from django.http import HttpResponse, QueryDict, HttpResponseForbidden, JsonResponse
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
from .mixins import FormsetMixin
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
    template_name = "courses/edit.html"
    exclude = ["professor"]
    success_url = reverse_lazy("courses:list")
    permission_required = "courses.manage_course"
    return_403 = True


class CourseCreateView(ProfessorRequiredMixin, FormsetMixin, CreateView):
    model = models.Course
    form_class = forms.CourseForm
    formset_class = forms.CourseLocationFormset
    template_name = "courses/edit.html"
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
    template_name = "courses/list.html"
    paginate_by = 100  # if pagination is desired

    def get_queryset(self):
        professor = self.request.user.professor
        return models.Course.objects.created_by(professor=professor)


class CourseDetailView(DetailView):
    model = models.Course
    template_name = "courses/detail.html"
    paginate_by = 10

    def get_context_data(self, **kwargs):
        kwargs["review_form"] = ReviewForm()
        kwargs["professor"] = self.object.professor
        kwargs["reviews"] = self.object.professor.review_set.order_by("-id")[
            :REVIEW_COUNT
        ]
        try:
            kwargs["has_enroll"] = models.Enrollment.objects.filter(
                student=self.request.user.student, course=self.object
            ).exists()
            if kwargs["has_enroll"]:
                kwargs["active_enroll"] = models.Enrollment.objects.get(
                    student=self.request.user.student, course=self.object
                ).accepted
        except:
            pass
        return super().get_context_data(**kwargs)


class CourseDeleteView(CoursePermissionRequiredMixin, DeleteView):
    model = models.Course
    success_url = reverse_lazy("courses:list")
    template_name = "confirm_delete.html"


class CourseSearchView(FormView):
    template_name = "courses/search.html"
    form_class = forms.CourseSearchForm
    success_url = reverse_lazy("courses:search")


class CourseSearchResultsView(FilterView):
    filterset_class = filters.CourseFilter
    template_name = "courses/search_results.html"
    paginate_by = 10


class ShowHandoutView(DetailView):
    model = models.Handout
    template_name = "courses/handout.html"


class HandoutsListView(ListView):
    model = models.Handout
    template_name = "courses/list_handouts.html"

    def get_queryset(self):
        slug = self.kwargs.get("slug")
        course = get_object_or_404(models.Course, slug=slug)
        object_list = self.model.objects.filter(course=course).order_by("section")
        return object_list

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        slug = self.kwargs.get("slug")
        context["course"] = get_object_or_404(models.Course, slug=slug)
        try:
            context["accepted"] = models.Enrollment.objects.get(
                course=context["course"], student=self.request.user.student
            ).accepted
        except:
            pass
        return context


class HandoutUpdateView(ProfessorRequiredMixin, UpdateView):
    model = models.Handout
    form_class = forms.HandoutForm
    template_name = "courses/handout.html"

    def get_success_url(self):
        handout_pk = self.kwargs.get("pk")
        course = get_object_or_404(models.Course, handout=handout_pk)
        return reverse("courses:list_handouts", kwargs={"slug": course.slug})


class HandoutDeleteView(ProfessorRequiredMixin, DeleteView):
    model = models.Handout
    template_name = "confirm_delete.html"

    def get_success_url(self):
        handout_pk = self.kwargs.get("pk")
        course = get_object_or_404(models.Course, handout=handout_pk)
        return reverse("courses:list_handouts", kwargs={"slug": course.slug})


class HandoutCreateView(ProfessorRequiredMixin, CreateView):
    model = models.Handout
    form_class = forms.HandoutForm
    template_name = "courses/handout.html"

    def form_valid(self, form):
        form = form.save(commit=False)
        slug = self.kwargs.get("slug")
        form.course = get_object_or_404(models.Course, slug=slug)
        form.save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse(
            "courses:list_handouts", kwargs={"slug": self.kwargs.get("slug")}
        )


import os
from django.conf import settings
from urllib.parse import quote


class FileDownloadView(View):
    # Set FILE_STORAGE_PATH value in settings.py
    folder_path = settings.MEDIA_ROOT
    # Here set the name of the file with extension
    file_name = ""
    # Set the content type value
    content_type_value = "text/plain"

    def get(self, request, pk):
        handout = get_object_or_404(models.Handout, pk=pk)
        file_path = os.path.join(self.folder_path, str(handout.attachment))
        filename = os.path.basename(file_path)
        if os.path.exists(file_path):
            with open(file_path, "rb") as fh:
                print(os.path.basename(file_path))
                response = HttpResponse(
                    fh.read(), content_type="application/force-download"
                )
                try:
                    filename.encode("ascii")
                    file_expr = 'filename="{}"'.format(filename)
                except UnicodeEncodeError:
                    file_expr = "filename*=utf-8''{}".format(quote(filename))
                response["Content-Disposition"] = "attachment; {}".format(file_expr)
                return response


class EnrollmentUpdateView(UpdateView):
    model = models.Enrollment
    fields = ["accepted"]

    def post(self, request, *args, **kwargs):
        # breakpoint()
        return super().post(request, *args, **kwargs)

    def form_valid(self, form):
        """If the form is valid, save the associated model."""
        self.object = form.save()
        # breakpoint()
        return JsonResponse(form.cleaned_data)

    def form_invalid(self, form):
        data = {
            "success": False,
            "errors": {k: v[0] for k, v in form.errors.items()},
        }
        return JsonResponse(data, status=400)


class EnrollmentCreateView(UpdateView):
    def post(self, request):
        post = QueryDict(request.body)
        student = self.request.user.profile
        course = post.get("course")
        course = get_object_or_404(models.Course, slug=course)
        if not models.Enrollment.objects.filter(
            student=student, course=course
        ).exists():
            model = models.Enrollment.objects.get_or_create(
                student=student, course=course, accepted=None
            )
        return HttpResponse()

    def put(self, request):

        put = QueryDict(request.body)
        enrollment = get_object_or_404(models.Enrollment, slug=put.get("enrol_slug"))
        action = put.get("action")
        if action == "True":
            enrollment.accepted = True
        else:
            enrollment.accepted = False
        enrollment.save()

        return HttpResponse([1, 2, 3])


class StudentEnrollmentsListView(StudentRequiredMixin, ListView):
    model = models.Enrollment
    template_name = "courses/professor_list_enrollments.html"

    def get_queryset(self):
        try:
            object_list = self.model.objects.filter(
                student=self.request.user.student
            ).order_by("accepted")
            return object_list
        except:
            return HttpResponseForbidden()


class ProfessorEnrollmentsListView(ProfessorRequiredMixin, ListView):
    model = models.Enrollment
    template_name = "courses/professor_list_enrollments.html"

    def get_queryset(self):
        object_list = self.model.objects.filter(
            course__professor=self.request.user.professor
        ).order_by("accepted")
        return object_list

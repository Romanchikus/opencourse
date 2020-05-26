from . import models, forms
from django.shortcuts import get_object_or_404
from opencourse.profiles.mixins import ProfessorRequiredMixin, StudentRequiredMixin
from django.views.generic import (
    UpdateView,
    DetailView,
    CreateView,
    View,
    DeleteView,
    ListView,
)
from django.urls import reverse, reverse_lazy
from django.http import HttpResponse, QueryDict, HttpResponseForbidden


class ShowHandoutView(DetailView):
    model = models.Handout
    template_name = "handouts/handout.html"


class HandoutsListView(ListView):
    model = models.Handout
    template_name = "handouts/list_handouts.html"

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
    template_name = "handouts/handout.html"

    def get_success_url(self):
        handout_pk = self.kwargs.get("pk")
        course = get_object_or_404(models.Course, handout=handout_pk)
        return reverse("handouts:list_handouts", kwargs={"slug": course.slug})


class HandoutDeleteView(ProfessorRequiredMixin, DeleteView):
    model = models.Handout
    template_name = "confirm_delete.html"

    def get_success_url(self):
        handout_pk = self.kwargs.get("pk")
        course = get_object_or_404(models.Course, handout=handout_pk)
        return reverse("handouts:list_handouts", kwargs={"slug": course.slug})


class HandoutCreateView(ProfessorRequiredMixin, CreateView):
    model = models.Handout
    form_class = forms.HandoutForm
    template_name = "handouts/handout.html"

    def form_valid(self, form):
        form = form.save(commit=False)
        slug = self.kwargs.get("slug")
        form.course = get_object_or_404(models.Course, slug=slug)
        form.save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse(
            "handouts:list_handouts", kwargs={"slug": self.kwargs.get("slug")}
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
    template_name = "handouts/list_enrollments.html"

    def get_queryset(self):
        try:
            object_list = self.model.objects.filter(
                student=self.request.user.student
            ).order_by("accepted")
            return object_list
        except:
            return HttpResponseForbidden()


class EnrollmentListView(ProfessorRequiredMixin, ListView):
    model = models.Enrollment
    template_name = "handouts/list_enrollments.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        new_context_entry = self.kwargs.get("slug")
        context["course_slug"] = new_context_entry
        return context

    def get_queryset(self):
        try:
            object_list = self.model.objects.filter(
                course__professor=self.request.user.profile
            ).order_by("accepted")
            return object_list
        except:
            return HttpResponseForbidden()

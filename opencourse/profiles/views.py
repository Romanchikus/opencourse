from django.http import HttpResponse
from django.urls import reverse_lazy
from django.views.generic import (
    UpdateView,
    RedirectView,
    CreateView,
    View,
    TemplateView,
    ListView,
    DetailView,
    DeleteView,
)
from django.contrib.auth import get_user_model
from django.views.generic.detail import SingleObjectMixin
from django.contrib.auth.mixins import LoginRequiredMixin

from . import forms, models
from .mixins import (
    ProfessorRequiredMixin,
    StudentRequiredMixin,
)
from opencourse.courses.models import Course
from django.db import transaction
from guardian.shortcuts import assign_perm
from . import forms, models, filters
from opencourse.courses.models import Course
from guardian.mixins import PermissionRequiredMixin
from django.views.generic.list import MultipleObjectMixin
from .mixins import JsonFormMixin
from django_filters.views import FilterView

User = get_user_model()


class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    model = User
    fields = ["first_name", "last_name"]
    formset_class = None

    def get_object(self, queryset=None):
        return self.request.user

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.POST:
            context["formset"] = self.formset_class(
                self.request.POST, self.request.FILES, instance=self.object
            )
        else:
            context["formset"] = self.formset_class(instance=self.object)
        return context

    def form_valid(self, form):
        context = self.get_context_data(form=form)
        formset = context["formset"]
        if formset.is_valid():
            response = super().form_valid(form)
            formset.instance = self.object
            formset.save()
            return response
        else:
            return super().form_invalid(form)


class ProfessorUpdateView(ProfessorRequiredMixin, ProfileUpdateView):
    template_name = "profiles/profile.html"
    success_url = reverse_lazy("courses:list")
    formset_class = forms.ProfessorFormSet


class StudentUpdateView(StudentRequiredMixin, ProfileUpdateView):
    template_name = "profiles/profile.html"
    success_url = reverse_lazy("courses:search")
    formset_class = forms.StudentFormSet


class ProfileView(LoginRequiredMixin, RedirectView):
    def get_redirect_url(self, *args, **kwargs):
        if hasattr(self.request.user, "professor"):
            return reverse_lazy("profiles:professor")
        elif hasattr(self.request.user, "student"):
            return reverse_lazy("profiles:student")
        return super().get_redirect_url(*args, **kwargs)


class DispatchLoginView(LoginRequiredMixin, RedirectView):
    def get_redirect_url(self, *args, **kwargs):
        if hasattr(self.request.user, "professor"):
            if self.request.user.professor.course_set.exists():
                return reverse_lazy("courses:list")
            else:
                return reverse_lazy("courses:create")
        return reverse_lazy("courses:search")


class ReviewCreateView(LoginRequiredMixin, StudentRequiredMixin, CreateView):
    form_class = forms.ReviewForm

    def get_success_url(self):
        pk = self.kwargs["pk"]
        return reverse_lazy("courses:detail", args=[pk])

    def form_valid(self, form):
        form.instance.author = self.request.user.profile
        pk = self.kwargs["pk"]
        course = Course.objects.filter(pk=pk).first()
        form.instance.professor = course.professor
        return super().form_valid(form)


class ContactRequestView(SingleObjectMixin, View):
    model = models.Professor

    def post(self, *args, **kwargs):
        professor = self.get_object()
        professor.contacts_requests += 1
        professor.save()
        return HttpResponse()


class ForbiddenView(TemplateView):
    template_name = "profiles/../templates/403.html"


class CenterCreateView(ProfessorRequiredMixin, CreateView):
    model = models.Center
    template_name = "courses/center_edit.html"
    form_class = forms.CenterForm
    success_url = reverse_lazy("courses:centers:list")

    def form_valid(self, form):
        with transaction.atomic():
            form.instance.admin = self.request.user.professor
            response = super().form_valid(form)
            center = self.object
            assign_perm("manage_center", center.admin.user, center)
            return response


class CenterEditView(PermissionRequiredMixin, UpdateView):
    model = models.Center
    template_name = "courses/center_edit.html"
    form_class = forms.CenterForm
    permission_required = "courses.manage_center"
    return_403 = True
    success_url = reverse_lazy("courses:centers:list")


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
        object_list = Course.objects.filter(center=self.get_object())
        return super(CenterDetailView, self).get_context_data(
            object_list=object_list, **kwargs
        )


class CenterDeleteView(PermissionRequiredMixin, DeleteView):
    model = models.Center
    success_url = reverse_lazy("courses:centers:list")
    template_name = "confirm_delete.html"
    permission_required = "courses.manage_center"
    return_403 = True


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

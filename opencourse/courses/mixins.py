from django.http import JsonResponse
from django.views.generic.edit import ModelFormMixin
from . import forms


class FormsetMixin(ModelFormMixin):
    formset_class = forms.CourseLocationFormset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        instance = getattr(self, "object", None)
        if self.request.POST:
            context["formset"] = self.formset_class(
                self.request.POST, instance=instance
            )
        else:
            context["formset"] = self.formset_class(instance=instance)
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        formset = context["formset"]
        if formset.is_valid():
            response = super().form_valid(form)
            formset.instance = self.object
            formset.save()
            return response
        else:
            return super().form_invalid(form)


class JsonFormMixin:
    def form_valid(self, form):
        self.object = form.save()
        return JsonResponse(form.data)

    def form_invalid(self, form):
        data = {
            "success": False,
            "errors": {k: v[0] for k, v in form.errors.items()},
        }
        return JsonResponse(data, status=400)

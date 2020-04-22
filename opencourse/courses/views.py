from django.views.generic import TemplateView


class IndexView(TemplateView):
    template_name = "courses/index.html"

from django.shortcuts import render
from django.template import TemplateDoesNotExist
from django.template.loader import get_template
from django.views.generic import TemplateView


class IndexView(TemplateView):
    template_name = "index.html"

    def get(self, request, *args, **kwargs):
        try:
            get_template(self.template_name)
        except TemplateDoesNotExist:
            return render(request, "custom_template.html", status=404)

        return super().get(request, *args, **kwargs)

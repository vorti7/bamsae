from django.views.generic import TemplateView

# CBV 기초
class HomePage(TemplateView):
    template_name = 'index.html'
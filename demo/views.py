from django.views.generic import TemplateView
from .forms import DemoForm
from django.shortcuts import render


class HelloWorld(TemplateView):
    template_name = 'demo/hello-world.html'


class NotFound(TemplateView):
    template_name = 'demo/404.html'


def demo_form(request):
    form = DemoForm()
    return render(request, 'demo/widgets.html', {'form': form})

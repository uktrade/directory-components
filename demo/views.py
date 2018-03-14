from django.views.generic import TemplateView
from demo.forms import DemoForm
from django.views.generic.edit import FormView


class HelloWorld(TemplateView):
    template_name = 'demo/hello-world.html'


class NotFound(TemplateView):
    template_name = 'demo/404.html'


class DemoFormView(FormView):
    template_name = 'demo/widgets.html'
    form_class = DemoForm

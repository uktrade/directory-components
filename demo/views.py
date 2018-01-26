from django.views.generic import TemplateView
import yaml
import pathlib

__here__ = pathlib.Path(__file__).parent

with open(__here__/"header_footer_urls.yml") as f:
    header_footer_urls = yaml.load(f)

class HelloWorld(TemplateView):
    template_name = 'demo/hello-world.html'

    def get_context_data(self, *args, **kwargs):
        return super().get_context_data(
            *args, **kwargs,
            header_footer_urls=header_footer_urls
        )

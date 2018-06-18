from django.views.generic import TemplateView
from demo import forms


class HelloWorld(TemplateView):
    template_name = 'demo/hello-world.html'


class NotFound(TemplateView):
    template_name = 'demo/404.html'


class DemoFormView(TemplateView):
    template_name = 'demo/form-elements.html'

    def get_context_data(self, *args, **kwargs):
        return super().get_context_data(
            text_form=forms.TextBoxForm(),
            checkbox_form=forms.CheckboxForm(),
            multiple_choice_form=forms.MultipleChoiceForm(),
            radio_form=forms.RadioForm(),
            *args, **kwargs
        )


class ComponentsView(TemplateView):
    template_name = 'demo/components.html'


class InvestHeaderFooterView(TemplateView):
    template_name = 'demo/invest_header_footer.html'

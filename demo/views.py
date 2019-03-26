from django.views.generic import TemplateView
from demo import forms
from django.urls import reverse_lazy
from django.views.generic.edit import FormView

from directory_components.mixins import CountryDisplayMixin


class BasePageView(TemplateView):

    @property
    def template_name(self):
        return self.kwargs.get('template_name')


class GreatDomesticHeader(BasePageView):
    def get_context_data(self, *args, **kwargs):
        return super().get_context_data(
            features={'HEADER_SEARCH_ON': False},
            page_heading='Great.gov.uk domestic header and footer',
            *args, **kwargs)


class GreatDomesticHeaderSearch(BasePageView):
    def get_context_data(self, *args, **kwargs):
        return super().get_context_data(
            features={'HEADER_SEARCH_ON': True},
            page_heading=(
                'Great.gov.uk domestic header and footer with search box'),
            *args, **kwargs)


class InternationalHeaderView(CountryDisplayMixin, BasePageView):
    pass


class DemoFormErrorsView(FormView):
    template_name = 'demo/form-errors.html'
    form_class = forms.DemoFormErrors
    success_url = reverse_lazy('form-errors')


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

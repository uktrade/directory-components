from django.views.generic import TemplateView
from demo import forms
from django.urls import reverse_lazy
from django.views.generic.edit import FormView

from directory_components.mixins import (
    CountryDisplayMixin, EnableTranslationsMixin
)


class BasePageView(TemplateView):

    @property
    def template_name(self):
        return self.kwargs.get('template_name')


class GreatDomesticHeaderView(BasePageView):
    def get_context_data(self, *args, **kwargs):
        return super().get_context_data(
            features={'HEADER_SEARCH_ON': False},
            page_heading='Great.gov.uk domestic header and footer',
            *args, **kwargs)


class GreatDomesticHeaderSearchView(BasePageView):
    def get_context_data(self, *args, **kwargs):
        return super().get_context_data(
            features={'HEADER_SEARCH_ON': True},
            page_heading=(
                'Great.gov.uk domestic header and footer with search box'),
            *args, **kwargs)


class InternationalHeaderView(
    CountryDisplayMixin, EnableTranslationsMixin, BasePageView
):
    pass


class DemoCardsView(BasePageView):
    statistics = [
        {
            'heading': 'Ease of doing business',
            'number': '36',
            'smallprint': 'World Bank Ease of Doing Business ranking'
        },
        {
            'heading': 'Currency',
            'number': 'Euro',
            'smallprint': ''
        },
        {
            'heading': 'Business languages',
            'number': 'Dutch, English',
            'smallprint': ''
        },
        {
            'heading': 'GDP per capita',
            'number': '48,223.16 USD',
            'smallprint': 'UK GDP per capita is 39,800.3 USD'
        },
        {
            'heading': 'Economic growth',
            'number': '2.9%',
            'smallprint': 'in 2017'
        },
        {
            'heading': 'Time zone',
            'number': 'GMT+1',
            'smallprint': ''
        },
    ]
    num_of_statistics = 6


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

import ast
import re
from unittest.mock import Mock

from django.core.paginator import Paginator
from django.shortcuts import Http404
from django.views.generic import TemplateView, View
from django.views.generic.edit import FormView
from django.urls import reverse_lazy

from directory_components.mixins import (
    CountryDisplayMixin, EnableTranslationsMixin,
    InternationalHeaderMixin
)

from demo import forms


class BasePageView(TemplateView):

    @property
    def template_name(self):
        return self.kwargs.get('template_name')


class IndexPageView(BasePageView):
    def get_version(self):
        pattern = re.compile(r'version=(.*),')

        with open('setup.py', 'rb') as src:
            return str(ast.literal_eval(
                pattern.search(src.read().decode('utf-8')).group(1)
            ))

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['version'] = self.get_version()
        return context


class InternationalHeaderView(
    InternationalHeaderMixin,
    CountryDisplayMixin,
    EnableTranslationsMixin,
    BasePageView
):
    header_section = "invest"


class InvestHeaderView(InternationalHeaderView):
    pass


class BreadcrumbsDemoPageView(BasePageView):
    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['page'] = {
            'title': 'Breadcrumbs demo page',
            'url': '',
        }
        context['home_link'] = '/'
        context['home_label'] = 'Home'
        return context


class SearchPageComponentsDemoPageView(BasePageView):

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(
            filters=['Energy', 'Real Estate', 'Automotive', 'Aerospace'],
            form=forms.MultipleChoiceForm(),
            *args, **kwargs
        )
        context['home_link'] = '/'
        context['home_label'] = 'Home'
        return context


class DemoStatsView(BasePageView):
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


class Trigger404View(View):
    def dispatch(self, request):
        raise Http404()


class Trigger500ErrorView(View):
    def dispatch(self, request):
        raise Exception('triggering a server error')


class DemoPaginationView(TemplateView):
    template_name = 'demo/pagination.html'

    objects = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15]

    @property
    def pagination_few_pages(self):
        paginator = Paginator(self.objects, 10)
        return [paginator.page(index) for index in range(1, 3)]

    @property
    def pagination_some_pages(self):
        paginator = Paginator(self.objects, 3)
        return [paginator.page(index) for index in range(1, 6)]

    @property
    def pagination_many_pages(self):
        paginator = Paginator(self.objects, 1)
        return [paginator.page(index) for index in range(1, 16)]

    def get_context_data(self, *args, **kwargs):
        return super().get_context_data(
            pagination_page_few_pages=self.pagination_few_pages,
            pagination_page_some_pages=self.pagination_some_pages,
            pagination_page_many_pages=self.pagination_many_pages,
        )


class DomesticHeaderFooterView(TemplateView):
    template_name = 'demo/great-domestic-header-footer.html'

    def dispatch(self, request, *args, **kwargs):
        if 'authenticated' in request.GET:
            request.user = Mock(is_authenticated=True)
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        return super().get_context_data(
            **kwargs,
            sso_login_url='?authenticated',
            sso_logout_url='?unauthenticated',
        )

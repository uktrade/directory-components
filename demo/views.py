from django.core.paginator import Paginator
from django.shortcuts import Http404
from django.views.generic import TemplateView, View
from django.views.generic.edit import FormView
from django.urls import reverse_lazy

from directory_components.mixins import (
    CountryDisplayMixin, EnableTranslationsMixin, InternationalHeaderMixin
)

from demo import forms


class BasePageView(TemplateView):

    @property
    def template_name(self):
        return self.kwargs.get('template_name')


class InternationalHeaderView(
    InternationalHeaderMixin,
    CountryDisplayMixin,
    EnableTranslationsMixin,
    BasePageView
):
    header_section = "invest"


class InvestHeaderView(
    CountryDisplayMixin, EnableTranslationsMixin, BasePageView
):
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
    def pagination_few_pages_1(self):
        paginator = Paginator(self.objects, 10)
        return paginator.page(1 or 1)

    @property
    def pagination_few_pages_2(self):
        paginator = Paginator(self.objects, 10)
        return paginator.page(2 or 1)

    @property
    def pagination_some_pages_1(self):
        paginator = Paginator(self.objects, 3)
        return paginator.page(1 or 1)

    @property
    def pagination_some_pages_3(self):
        paginator = Paginator(self.objects, 3)
        return paginator.page(3 or 1)

    @property
    def pagination_some_pages_5(self):
        paginator = Paginator(self.objects, 3)
        return paginator.page(5 or 1)

    @property
    def pagination_many_pages_1(self):
        paginator = Paginator(self.objects, 1)
        return paginator.page(1 or 1)

    @property
    def pagination_many_pages_10(self):
        paginator = Paginator(self.objects, 1)
        return paginator.page(10 or 1)

    @property
    def pagination_many_pages_15(self):
        paginator = Paginator(self.objects, 1)
        return paginator.page(15 or 1)

    def get_context_data(self, *args, **kwargs):
        return super().get_context_data(
            pagination_page_few_1=self.pagination_few_pages_1,
            pagination_page_few_2=self.pagination_few_pages_2,
            pagination_page_some_1=self.pagination_some_pages_1,
            pagination_page_some_3=self.pagination_some_pages_3,
            pagination_page_some_5=self.pagination_some_pages_5,
            pagination_page_many_1=self.pagination_many_pages_1,
            pagination_page_many_10=self.pagination_many_pages_10,
            pagination_page_many_15=self.pagination_many_pages_15
        )

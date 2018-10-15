from django.views.generic import TemplateView
from demo import forms
from django.urls import reverse_lazy, reverse
from django.contrib.staticfiles.templatetags.staticfiles import static
from django.views.generic.edit import FormView

from directory_components.helpers import SocialLinkBuilder


class HelloWorld(TemplateView):
    template_name = 'demo/hello-world.html'


class GreatHeaderFooter(TemplateView):
    template_name = 'demo/great-header-footer.html'


class Elements(TemplateView):
    template_name = 'demo/elements.html'


class NotFound(TemplateView):
    template_name = 'demo/404.html'


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


class ComponentsView(TemplateView):
    template_name = 'demo/components.html'


class ResponsiveGridView(TemplateView):
    template_name = 'demo/responsive_grid.html'


class InvestHeaderFooterView(TemplateView):
    template_name = 'demo/invest_header_footer.html'


class TemplateTagsView(TemplateView):
    template_name = 'demo/template_tags.html'


class PrototypeArticlePageView(TemplateView):
    template_name = 'demo/prototype_article.html'
    parent_sections = [
        {
            'url': '#',
            'title': 'Guidance'
        },
        {
            'url': '#',
            'title': 'Market research'
        },
    ]
    current_page = {
        'url': '#',
        'title': 'Research your market'
    }
    parent_site = {
        'url': reverse_lazy('hello-world'),
        'title': 'Great.gov.uk'
    }

    def get_context_data(self, *args, **kwargs):
        social_links_builder = SocialLinkBuilder(
            self.request.build_absolute_uri(reverse('prototype-article')),
            self.current_page['title'],
            self.parent_site['title'])

        return super().get_context_data(
            social_links=social_links_builder.links,
            parent_sections=self.parent_sections,
            current_page=self.current_page,
            parent_site=self.parent_site,
            *args, **kwargs
        )


class PrototypeGuidanceListView(TemplateView):
    template_name = 'demo/prototype_guidance_list.html'
    # create dummy content for the page that would be returned by the cms api
    page = {
        'parent_sections': [],
        'current_page': {
            'url': reverse_lazy('prototype-guidance-list'),
            'title': 'Guidance'
        },
        'parent_site': {
            'url': reverse_lazy('hello-world'),
            'title': 'Great.gov.uk'
        },
        'guidance_sections': [
            {
                'title': 'Market research',
                'id': 'market research',
                'description': (
                    'Research is an essential first step to selling in a new '
                    'market. Making decisions based on market data will help '
                    'you maximise profits and avoid costly mistakes.'),
                'icon_url': static('images/sections/market-research.svg'),
                'article_url': reverse_lazy('prototype-article'),
            },
            {
                'title': 'Customer insight',
                'id': 'customer-insight',
                'description': (
                    'Find out about potential customers to target them '
                    'effectively. Once you have overseas customers, nurture '
                    'the customer relationship with regular face-to-face '
                    'meetings.'),
                'icon_url': static('images/sections/customer-insight.svg'),
                'article_url': '#',
            },
            {
                'title': 'Finance',
                'id': 'finance',
                'description': (
                    'Finding the right financial products for your business '
                    'can give you a competitive edge in overseas markets and '
                    'bridge the gap between invoicing and payment.'),
                'icon_url': static('images/sections/finance.svg'),
                'article_url': '#',
            },
            {
                'title': 'Business planning',
                'id': 'business-planning',
                'description': (
                    'Having a well thought out export plan will make it '
                    'easier to get financial support and make informed '
                    'decisions on which markets to enter and which routes '
                    'to take.'),
                'icon_url': static('images/sections/business-planning.svg'),
                'article_url': '#',
            },
            {
                'title': 'Getting paid',
                'id': 'getting-paid',
                'description': (
                    'Think about what currency to invoice in, what to include '
                    'on a commercial invoice and if you need to insure '
                    'against non-payment.'),
                'icon_url': static('images/sections/getting-paid.svg'),
                'article_url': '#',
            },
            {
                'title': 'Operations and compliance',
                'id': 'operations-and-compliance',
                'description': (
                    'How you market your website, deliver your products and '
                    'protect your brand all need consideration when your '
                    'customers are overseas.'),
                'icon_url': static(
                    'images/sections/operations-and-compliance.svg'),
                'article_url': '#',
            },
        ]
    }

    def get_context_data(self, *args, **kwargs):
        return super().get_context_data(
            page=self.page,
            *args, **kwargs
        )

from directory_constants.constants.choices import COUNTRY_CHOICES

from directory_components import helpers, forms


class CountryDisplayMixin:
    country_form_class = forms.CountryForm

    def get_context_data(self, *args, **kwargs):
        country_code = helpers.get_user_country(self.request)

        # if there is a country already detected we can hide the selector
        hide_country_selector = bool(country_code)
        country_name = dict(COUNTRY_CHOICES).get(country_code, '')

        country = {
            # used for flag icon css class. must be lowercase
            'code': country_code.lower(),
            'name': country_name,
        }

        country_form_kwargs = self.get_country_form_kwargs()

        return super().get_context_data(
            hide_country_selector=hide_country_selector,
            country=country,
            country_selector_form=self.country_form_class(
                **country_form_kwargs),
            *args, **kwargs
        )

    def get_country_form_kwargs(self, **kwargs):
        return {
            'initial': forms.get_country_form_initial_data(self.request),
            **kwargs,
        }

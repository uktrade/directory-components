dit.tagging = dit.tagging || {};
dit.tagging.internationalHeader = new function() {

    this.init = function() {
        $(document).ready(function() {
            $("[data-ga-class='banner-choose-country-form']").on("submit", function() {
                window.dataLayer.push({
                    'event': 'gaEvent',
                    'action': 'SelectCountry',
                    'type': 'InternationalHeader',
                    'element': 'Form',
                    'value': $("#great-header-country-select").val()
                });
            });

            $("[data-ga-class='change-country-form']").on("submit", function() {
                window.dataLayer.push({
                    'event': 'gaEvent',
                    'action': 'ChangeCountry',
                    'type': 'InternationalHeader',
                    'element': 'Form',
                    'value': $("#great-header-country-select").val()
                });
            });

            $("[data-ga-class='change-language-form']").on("submit", function() {
                window.dataLayer.push({
                    'event': 'gaEvent',
                    'action': 'ChangeLanguage',
                    'type': 'InternationalHeader',
                    'element': 'Form',
                    'value': $("#great-header-language-select").val()
                });
            });

            $("[data-ga-class='header-navigation']").on("click", function() {
                window.dataLayer.push({
                    'event': 'gaEvent',
                    'action': 'Navigation',
                    'type': 'InternationalHeader',
                    'element': 'Link',
                    'value': $(this).text()
                });
            })
        });
    };
};
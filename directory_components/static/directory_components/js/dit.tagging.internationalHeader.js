dit.tagging = dit.tagging || {};
dit.tagging.internationalHeader = new function() {

    this.init = function() {
        $(document).ready(function() {
            $("[data-ga-class='banner-choose-country-form']").on("submit", function() {
                window.dataLayer.push({
                    'eventAction': 'Select Country',
                    'eventLabel': 'International Header',
                    'eventValue': $("#great-header-country-select").val()
                });
            });

            $("[data-ga-class='change-country-form']").on("submit", function() {
                window.dataLayer.push({
                    'eventAction': 'Change Country',
                    'eventLabel': 'International Header',
                    'eventValue': $("#great-header-country-select").val()
                });
            });

            $("[data-ga-class='change-language-form']").on("submit", function() {
                window.dataLayer.push({
                    'eventAction': 'Change Language',
                    'eventLabel': 'International Header',
                    'eventValue': $("#great-header-language-select").val()
                });
            });

            $("[data-ga-class='header-navigation']").on("click", function() {
                window.dataLayer.push({
                    'eventAction': 'Navigation',
                    'eventCategory': 'Header Link',
                    'eventLabel': 'International Header',
                    'eventValue': $(this).text()
                });
            })
        });
    };
};
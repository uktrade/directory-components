dit.tagging.internationalHeader = function() {

    this.init = function() {
        $("[data-ga-id='choose-country-form']").on("submit", function() {
            window.dataLayer.push({
                'eventAction': 'Submit',
                'eventCategory': 'Select Country',
                'eventLabel': 'International Header',
                'eventValue': $("#great-header-country-select").val()
            });
        });

        $("[data-ga-id='change-country-form']").on("submit", function() {
            window.dataLayer.push({
                'eventAction': 'Submit',
                'eventCategory': 'Change Country',
                'eventLabel': 'International Header',
                'eventValue': $("#great-header-country-select").val()
            });
        });

        $("[data-ga-id='change-language-form']").on("submit", function() {
            window.dataLayer.push({
                'eventAction': 'Submit',
                'eventCategory': 'Change Language',
                'eventLabel': 'International Header',
                'eventValue': $("#great-header-language-select").val()
            });
        });

        $("[data-ga-id='invest-header-navigation']").on("click", function() {
            window.dataLayer.push(navLinkClickedEvent("Invest"));
        });

        $("[data-ga-id='fas-header-navigation']").on("click", function() {
            window.dataLayer.push(navLinkClickedEvent("Find a UK supplier"));
        });

        $("[data-ga-id='industries-header-navigation']").on("click", function() {
            window.dataLayer.push(navLinkClickedEvent("Industries"));
        });

        $("[data-ga-id='how-to-do-business-header-navigation']").on("click", function() {
            window.dataLayer.push(navLinkClickedEvent("How to do business with the UK"));
        });

        $("[data-ga-id='news-header-navigation']").on("click", function() {
            window.dataLayer.push(navLinkClickedEvent("News"));
        });

        $("[data-ga-id='domestic-header-navigation']").on("click", function() {
            window.dataLayer.push(navLinkClickedEvent("For UK businesses"));
        });
    };

    function navLinkClickedEvent(linkName) {
        return {
                'eventAction': 'Navigation',
                'eventCategory': 'Header Link',
                'eventLabel': 'International Header',
                'eventValue': linkName
        }
    }
};
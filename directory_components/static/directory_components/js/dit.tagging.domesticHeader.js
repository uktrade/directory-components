dit.tagging = dit.tagging || {};
dit.tagging.domesticHeader = new function() {

    this.init = function() {
        $(document).ready(function() {

            $('#great-header-search-form').on('submit', function() {
                window.dataLayer.push({
                    'event': 'gaEvent',
                    'action': 'Search',
                    'type': 'General',
                    'element': 'HeaderSearchBar',
                    'value': $('#great-header-search-box').text()
                });
            });

            $('[data-ga-class="great-header-menu-link"]').on('click', function() {
                window.dataLayer.push({
                    'event': 'gaEvent',
                    'action': 'Navigation',
                    'element': 'HeaderMenuLink',
                    'value': $(this).text()
                });
            });

            // for following link by pressing enter
            $('[data-ga-class="great-header-menu-link"]').on('keypress', function(e) {
                  if (e.which == 13) {
                      window.dataLayer.push({
                          'event': 'gaEvent',
                          'action': 'Navigation',
                          'element': 'HeaderMenuLink',
                          'value': $(this).text()
                      });
                  }
            });

            $('#header-sign-in-link').on('click', function() {
                  window.dataLayer.push({
                      'event': 'gaEvent',
                      'action': 'SignIn',
                      'type': 'Account',
                      'element': 'HeaderSignInLink'
                });
            });

            // for following link by pressing enter
            $('#header-sign-in-link').on('keypress', function(e) {
                  if (e.which == 13) {
                      window.dataLayer.push({
                          'event': 'gaEvent',
                          'action': 'SignIn',
                          'type': 'Account',
                          'element': 'HeaderSignInLink'
                      });
                  }
            });

        });
    };
};

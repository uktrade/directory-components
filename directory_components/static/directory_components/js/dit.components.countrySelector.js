
var dit = dit || {};
dit.components = dit.components || {};

dit.components.countrySelector = (new function() {
  var self = this;

  var BANNER = '#country-selector-dialog';
  var BANNER_ID = 'country-selector-dialog';
  var BANNER_CLOSE_BUTTON_ID = 'close-country-selector-dialog';
  var BANNER_ACTIVATOR = '#country-selector-activator';
  var BANNER_ACTIVATOR_ID = 'country-selector-activator';
  var COUNTRY_SELECT = '#js-country-select';
  var FLAG = '#flag-container';

  self.createBannerCloseButton = function() {
    var $container = $(BANNER + ' .countries');
    var $button = $('<button></button>', {
      'text': 'Close',
      'class': 'close-button',
      'aria-controls': BANNER_ID,
      id: BANNER_CLOSE_BUTTON_ID
    });
    $container.append($button);
    return $button;
  }

  self.bannerCloseButtonEventHandler = function() {
    var $button = self.createBannerCloseButton();

    $button.on('keydown', function(e) {
      // Close on enter, space or esc
      if(e.which === 13 || e.which === 32 || e.which == 27) {
        e.preventDefault();
        self.closeBanner();
      }
    });

    $button.on('click', function(e) {
      e.preventDefault();
      self.closeBanner();
    });
  }

  self.createBannerOpenButton = function() {
    var $element = $('#country-text');
    var $button = $('<button></button>', {
      'text': 'Change country',
      'aria-controls': BANNER_ID,
      'class': 'country-selector-activator',
      id: BANNER_ACTIVATOR_ID
    });
    $element.replaceWith($button);
    return $button;
  }

  self.bannerOpenButtonEventHandler = function() {
    var $button = self.createBannerOpenButton();

    $button.on('keydown', function(e) {
      // Close on enter or space
      if(e.which === 13 || e.which === 32) {
        e.preventDefault();
        self.openBanner();
      }
    });

    $button.on('click', function(e) {
      e.preventDefault();
      $(BANNER).show();
    });
  }

  self.closeBanner = function() {
    $(BANNER).hide();
    $(BANNER_ACTIVATOR).focus();
  }

  self.openBanner = function() {
    $(BANNER).show();
    $(COUNTRY_SELECT).focus();
  }

  self.bannerContentsEventHandler = function() {
    var $items = $(BANNER).find('form').find('select, a, button, input');

    $items.each(function() {
      $(this).on('keydown', function(e) {
        if (e.which === 27) { // esc
          self.closeBanner();
        }
      })
    })
  }

  self.selectEventHandler = function() {
    $(COUNTRY_SELECT).on('change', function() {
      var country = '';

      $("select option:selected").each(function() {
        country = $(this).attr('value');
      });

      $(FLAG).attr('class', 'flag-icon flag-icon-' + country.toLowerCase())
    });
  }

  self.viewInhibitor = function(activate) {
    var rule = BANNER + " { display: none; }";
    var style;
    if (arguments.length && activate) {
      style = document.createElement("style");
      style.setAttribute("type", "text/css");
      style.setAttribute("id", "country-dialog-view-inhibitor");
      style.appendChild(document.createTextNode(rule));
      document.head.appendChild(style);
    }
    else {
      document.head.removeChild(document.getElementById("country-dialog-view-inhibitor"));
    }
  }
  self.viewInhibitor(true);

  self.bannerEventHandler = function() {
    self.bannerCloseButtonEventHandler();
    self.bannerOpenButtonEventHandler();
    self.bannerContentsEventHandler();
    self.selectEventHandler();
  }

  self.init = function() {
    self.bannerEventHandler();
  }

});


var dit = dit || {};
dit.components = dit.components || {};

dit.components.countrySelector = (new function() {

  var BANNER = '#country-selector-dialog';
  var BANNER_ID = 'country-selector-dialog';
  var BANNER_CLOSE_BUTTON_ID = 'close-country-selector-dialog';
  var BANNER_ACTIVATOR = '#country-selector-activator';
  var BANNER_ACTIVATOR_ID = 'country-selector-activator';
  var COUNTRY_SELECT = '#js-country-select';
  var FLAG = '#flag-container';

  this.createBannerCloseButton = function() {
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

  this.bannerCloseButtonEventHandler = function() {
    var $button = this.createBannerCloseButton();
    console.log('close button events');

    $button.on('keydown', function(e) {
      // Close on enter, space or esc
      if(e.which === 13 || e.which === 32 || e.which == 27) {
        e.preventDefault();
        this.closeBanner();
      }
    });

    $button.on('click', function(e) {
      e.preventDefault();
      this.closeBanner();
    });
  }

  this.createBannerOpenButton = function() {
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

  this.bannerOpenButtonEventHandler = function() {
    var $button = this.createBannerOpenButton();

    $button.on('keydown', function(e) {
      // Close on enter or space
      if(e.which === 13 || e.which === 32) {
        e.preventDefault();
        this.openBanner();
      }
    });

    $button.on('click', function(e) {
      e.preventDefault();
      $(BANNER).show();
    });
  }

  this.closeBanner = function() {
    $(BANNER).hide();
    $(BANNER_ACTIVATOR).focus();
  }

  this.openBanner = function() {
    $(BANNER).show();
    $(COUNTRY_SELECT).focus();
  }

  this.bannerContentsEventHandler = function() {
    var $items = $(BANNER).find('form').find('select, a, button, input');

    $items.each(function() {
      $(this).on('keydown', function(e) {
        if (e.which === 27) { // esc
          this.closeBanner();
        }
      })
    })
  }

  this.selectEventHandler = function() {
    $(COUNTRY_SELECT).on('change', function() {
      var country = '';

      $("select option:selected").each(function() {
        country = $(this).attr('value');
      });

      $(FLAG).attr('class', 'flag-icon flag-icon-' + country.toLowerCase())
    });
  }

  this.viewInhibitor = function(activate) {
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
  this.viewInhibitor(true);

  this.bannerEventHandler = function() {
    console.log('events 1');
    this.bannerCloseButtonEventHandler();
    console.log('events 2');
    this.bannerOpenButtonEventHandler();
    console.log('events 3');
    this.bannerContentsEventHandler();
    this.selectEventHandler();
  }

  this.init = function() {
    console.log('init');
    this.bannerEventHandler();
  }

});
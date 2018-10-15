
var dit = dit || {};
dit.components = dit.components || {};

dit.components.dismissableBanner = (new function() {

  var BANNER_ID = 'information-banner';
  var BANNER_CLOSE_BUTTON_ID = 'dismiss-banner';

  hideBanner = function() {
    $('#information-banner').hide();
  }

  createBannerCloseButton = function() {
    var $container = $('#information-banner .banner-content');
    var $buttonContainer = $('<div></div>');
    var $closeButton = $('<a>', {
      'text': 'Close',
      'href': '#',
      'class': 'banner-close-button link',
      'aria-controls': BANNER_ID,
      id: BANNER_CLOSE_BUTTON_ID
    });
    $buttonContainer.append($closeButton);
    $container.append($buttonContainer);
    return $closeButton;
  }

  bannerCloseButtonEventHandler = function() {
    var $button = createBannerCloseButton();

    $button.on('keydown', function(e) {
      // Close on enter or space
      if(e.which === 13 || e.which === 32) {
        hideBanner();
      }
    });

    $button.on('click', function(e) {
      hideBanner();
      e.preventDefault();
    });
  }

  this.init = function() {
    bannerCloseButtonEventHandler();
  }

});

$(document).ready(function() {
  dit.components.dismissableBanner.init();
});

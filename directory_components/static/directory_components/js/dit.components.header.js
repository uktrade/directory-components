
var dit = dit || {};

dit.classes = dit.classes || {};
dit.components = dit.components || {};
dit.constants = dit.constants || {};

dit.components.header = (new function() {
  var self = this;

  self.showButton = function() {
    $('#mobile-menu-button').addClass('ready');
  };

  self.toggleMenu = function() {
    var nav = $('#great-header-mobile-nav');
    var isCurrentlyExpanded = nav.attr('aria-expanded');

    if (isCurrentlyExpanded === 'true') {
      self.closeMenu();
    } else {
      self.openMenu();
    }
  };

  self.openMenu = function() {
    $('#mobile-menu-button').addClass('expanded').attr('aria-expanded', 'true');
    $('#great-header-mobile-nav').addClass('expanded').attr('aria-expanded', 'true');
    $('#great-header-search-wrapper').hide();
  };

  self.closeMenu = function() {
    $('#mobile-menu-button').removeClass('expanded').attr('aria-expanded', 'false');
    $('#great-header-mobile-nav').removeClass('expanded').attr('aria-expanded', 'false');
    $('#great-header-search-wrapper').show();
  };

  self.init = function() {
    var mobileMenuButton = document.getElementById("mobile-menu-button");
    var header = document.getElementById("great-header-menu");

    mobileMenuButton.addEventListener("click", function () {
      self.toggleMenu();
    });

    header.addEventListener("keyup", function(event) {
      if (event.key === "Escape") {
        self.closeMenu();
      }
    });

    // menu should start closed
    self.closeMenu();
    self.showButton();
  }
});

$(document).ready(function() {
  dit.components.header.init();
});

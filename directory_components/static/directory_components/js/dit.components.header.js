
var dit = dit || {};

dit.classes = dit.classes || {};
dit.components = dit.components || {};
dit.constants = dit.constants || {};

dit.components.header = (new function() {
  var self = this;

  self.init = function() {
    var mobileMenuButtons = document.getElementsByClassName("mobile-menu-button");
    for (var i = 0; i < mobileMenuButtons.length; i++) {
      var mobileMenuButton = mobileMenuButtons[i];
      mobileMenuButton.addEventListener("click", function(event) {
        $(this).toggleClass('expanded');
        $('#great-header-menu-mobile').toggleClass('expanded');
        event.preventDefault();
      });
    }
  };
});

$(document).ready(function() {
  dit.components.header.init();
});

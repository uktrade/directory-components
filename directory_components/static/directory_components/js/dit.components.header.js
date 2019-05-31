
var dit = dit || {};

dit.classes = dit.classes || {};
dit.components = dit.components || {};
dit.constants = dit.constants || {};

dit.components.header = (new function() {
  const self = this;

  self.init = function() {
    const mobileMenuButtons = document.getElementsByClassName("mobile-menu-button");
    for (let i = 0; i < mobileMenuButtons.length; i++) {
      const mobileMenuButton = mobileMenuButtons[i];
      mobileMenuButton.addEventListener("click", function(event) {
        const href = mobileMenuButton.getAttribute("href");
        window.location.replace(href);
        event.preventDefault();
      });
    }
  };
});

$(document).ready(function() {
  dit.components.header.init();
});

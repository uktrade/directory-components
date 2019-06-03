
var dit = dit || {};

dit.classes = dit.classes || {};
dit.components = dit.components || {};
dit.constants = dit.constants || {};

dit.components.internationalHeader = (new function() {
  const self = this;

  function toggleSubNavMobile(subNavElementId) {
    const subNavId = subNavElementId.split("-").pop();
    const subNavList = document.getElementById("sub-nav-mobile-list-" + subNavId);
    subNavList.hidden = !subNavList.hidden;
  }

  self.init = function() {
    const subNavMobileToggles = document.getElementsByClassName("sub-nav-mobile-toggle");
    for (let i = 0; i < subNavMobileToggles.length; i++) {
      const subNavMobileToggle = subNavMobileToggles[i];
      subNavMobileToggle.onclick = function() { toggleSubNavMobile(subNavMobileToggle.id); };
    }
  };
});

$(document).ready(function() {
  dit.components.countrySelector.init();
  dit.components.languageSelectorDropdown.init();
  dit.components.internationalHeader.init();
});

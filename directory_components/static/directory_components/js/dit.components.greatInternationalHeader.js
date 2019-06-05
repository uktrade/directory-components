
var dit = dit || {};

dit.classes = dit.classes || {};
dit.components = dit.components || {};
dit.constants = dit.constants || {};

dit.components.internationalHeader = (new function() {
  const self = this;
  let openSubNavId = "";
  let subNavBackground;

  function toggleSubNav(subNavElementId) {
    const subNavId = subNavElementId.split("-").pop();

    if (openSubNavId) {
      document.getElementById("sub-nav-list-" + openSubNavId).hidden = true;
    }
    subNavBackground.style.height = "0";

    if (subNavId && openSubNavId !== subNavId) {
      const subNav = document.getElementById("sub-nav-list-" + subNavId);
      subNav.hidden = false;
      subNavBackground.style.height = subNav.offsetHeight + "px";
    }

    openSubNavId = openSubNavId === subNavId ? "" : subNavId;
  }

  function toggleSubNavMobile(subNavElementId) {
    const subNavId = subNavElementId.split("-").pop();
    const subNavList = document.getElementById("sub-nav-mobile-list-" + subNavId);
    subNavList.hidden = !subNavList.hidden;
  }

  self.init = function() {
    subNavBackground = document.getElementById("international-header-sub-nav-background");

    const subNavToggles = document.getElementsByClassName("sub-nav-toggle");
    for (let i = 0; i < subNavToggles.length; i++) {
      const subNavToggle = subNavToggles[i];
      subNavToggle.onclick = function() { toggleSubNav(subNavToggle.id); };
    }

    const subNavMobileToggles = document.getElementsByClassName("sub-nav-mobile-toggle");
    for (let i = 0; i < subNavMobileToggles.length; i++) {
      const subNavMobileToggle = subNavMobileToggles[i];
      subNavMobileToggle.onclick = function() { toggleSubNavMobile(subNavMobileToggle.id); };
    }
  }
});

$(document).ready(function() {
  dit.components.countrySelector.init();
  dit.components.languageSelectorDropdown.init();
  dit.components.internationalHeader.init();
});


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
    subNavBackground.hidden = true;

    if (subNavId && openSubNavId !== subNavId) {
      const subNav = document.getElementById("sub-nav-list-" + subNavId);
      subNav.hidden = false;
      subNavBackground.style.height = subNav.offsetHeight + "px";
      subNavBackground.hidden = false;
    }

    openSubNavId = openSubNavId === subNavId ? "" : subNavId;
  }

  self.init = function() {
    subNavBackground = document.getElementById("international-header-sub-nav-background");

    const subNavToggles = document.getElementsByClassName("sub-nav-toggle");
    for (let i = 0; i < subNavToggles.length; i++) {
      const subNavToggle = subNavToggles[i];
      subNavToggle.onclick = function() { toggleSubNav(subNavToggle.id); };
    }
  }
});

$(document).ready(function() {
  dit.components.countrySelector.init();
  dit.components.languageSelectorDropdown.init();
  dit.components.internationalHeader.init();
});

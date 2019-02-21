// Country Selector Component Functionality.
//
// Requires...
// dit.js
// dit.utils.js
// dit.class.modal.js

// Usage
// --------------------------------------------------------------------
// To find all Country Selector components and enhance using
// the default settings.
//
// dit.components.countrySelector.init()
//
// For greater control, use either of the individual enhance functions
// for Country Selector Control or Country Selector Dialog components.
// This also allow passing options to customise the output.
//
// dit.components.countrySelector.enhanceControl()
// dit.components.countrySelector.enhanceDialog()

dit.components = dit.components || {};

dit.components.countrySelector = (new function() {

  var COUNTRY_SELECT_CLOSE_BUTTON_ID = "great-header-country-selector-close";

  dit.classes.CountrySelectorControl = CountrySelectorControl;
    function CountrySelectorControl($select) {
      var SELECT_TRACKER = this;
      var button, code, lang;

      if (arguments.length && $select.length) {
        this.$node = $(document.createElement("p"));
        this.$node.attr("aria-hidden", "true");
        this.$node.addClass("SelectTracker");
        this.$select = $select;
        this.$select.addClass("SelectTracker-Select");
        this.$select.after(this.$node);
        this.$select.on("change.SelectTracker", function() {
          SELECT_TRACKER.update();
        });

        // Initial value
        this.update();
      }
    }

  CountrySelectorControl.prototype = {};
  CountrySelectorControl.prototype.update = function() {
    var $code = $(document.createElement("span"));
    var $lang = $(document.createElement("span"));
    SelectTracker.prototype.update.call(this);
    $lang.addClass("lang");
    $code.addClass("code");
    $lang.text(this.$node.text());
    $code.text(this.$select.val());
    this.$node.empty();
    this.$node.append($code);
    this.$node.append($lang);
  }

  /* Contructor
   * Displays control and dialog enhancement for language-selector-dialog element.
   * @$dialog (jQuery node) Element displaying list of selective links
   * @options (Object) Configurable options
   **/
  function CountrySelectorDialog($dialog, options) {
    var COUNTRY_SELECTOR_DISPLAY = this;
    var id = dit.utils.generateUniqueStr("CountrySelectorDialog_");
    var $control = CountrySelectorDialog.createControl($dialog, id);
    dit.classes.Modal.call(COUNTRY_SELECTOR_DISPLAY, $dialog, {
      $activators: $control,
      closeButtonId: COUNTRY_SELECT_CLOSE_BUTTON_ID
    });
    this.config = $.extend({
      $controlContainer: $dialog.parent() // Where to append the generated control
    }, options);


    if (arguments.length > 0 && $dialog.length) {
      this.$container.attr("id", id);
      this.$container.addClass("CountrySelectorDialog-Modal");
      this.setContent($dialog.children());
    }
  }

  CountrySelectorDialog.createControl = function($node, id) {
    var $control = $('#header-country-selector-activator');
    $control.attr("href", ("#" + id));
    $control.attr("aria-controls", id);
    return $control;
  }

  CountrySelectorDialog.prototype = new dit.classes.Modal;

  // Just finds all available Country Selector components
  // and enhances using the any default settings.
  this.init = function() {
    $("[data-component='country-selector-dialog']").each(function() {
      new CountrySelectorDialog($(this));
    });
  }

  // Selective enhancement for individual Country Selector Control views
  // Allows passing of custom options.
  // @$control (jQuery object) Something like this: $("[data-component='language-selector-control'] select")
  // @options (Object) Configurable options for class used.
  this.enhanceControl = function($control, options) {
    if ($control.length) {
      new CountrySelectorControl($control, options);
    }
    else {
      console.error("Country Selector Control missing or not passed")
    }
  }

  // Selective enhancement for individual Country Selector Dialog views
  // Allows passing of custom options.
  // @$control (jQuery object) Something like this: $("[data-component='language-selector-dialog']")
  // @options (Object) Configurable options for class used.
  this.enhanceDialog = function($dialog , options) {
    if ($dialog.length) {
      new CountrySelectorDialog($dialog, options);
    }
  }

});

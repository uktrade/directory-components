
dit.components.searchPageExpandableOptions = new function(){
    var self = this;

    self.init = function () {
        function handleExpandableOptions(event) {
            var element = event.target;
            element.classList.toggle('checked');
            var aria_label = element.getAttribute('aria-label');
            if (aria_label.includes("Hide")) {
                element.setAttribute('aria-label', aria_label.replace("Hide", "Show"));
            }
            else if (aria_label.includes("Show")) {
                element.setAttribute('aria-label', aria_label.replace("Show", "Hide"));
            }
            var formGroup = document.getElementById(element.getAttribute('aria-controls'));
            formGroup.setAttribute('aria-expanded', !(formGroup.getAttribute('aria-expanded') == 'true'));
        }
        var elements = document.getElementsByClassName('filter-collapse');
        for (var i = 0; i < elements.length; i++) {
            elements[i].addEventListener('click', handleExpandableOptions);
        }
    }
};

$(document).ready(function() {
  dit.components.searchPageExpandableOptions.init();
});

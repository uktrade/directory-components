dit.tagging = dit.tagging || {};
dit.tagging.base = new function() {
    this.init = function() {
        $(document).ready(function() {
            addTaggingForLinks();
            addTaggingForVideos();
            addTaggingForForms();
        });

        function addTaggingForLinks() {
            var enterKeyValue = 13;
            $('a')
                .on('click', function() { sendLinkEvent($(this)); })
                .on('keypress', function(event) {
                    if (event.code === enterKeyValue) {
                        sendLinkEvent($(this));
                    }
                });
        }

        function addTaggingForVideos() {
            $('video')
                .on('play', function() { sendVideoEvent($(this), 'play') })
                .on('pause', function() { sendVideoEvent($(this), 'pause') })
                .on('ended', function() { sendVideoEvent($(this), 'ended') })
        }

        function addTaggingForForms() {
            $('form').on('submit', function() { sendFormEvent($(this)) })
        }

        function sendLinkEvent(link) {
            var action = link.data('ga-action') || 'clickLink';
            var type = link.data('ga-type') || inferLinkType(link);
            var element = link.data('ga-element') || inferElement(link);
            var value = link.data('ga-value') || inferLinkValue(link);
            var destination = link.attr('href');

            sendEvent(action, type, element, value, destination);
        }

        function sendVideoEvent(video, action) {
            var type = video.data('ga-type') || 'video';
            var element = video.data('ga-element') || inferElement(video);
            var value = video.data('ga-value') || inferVideoValue(video);

            sendEvent(action, type, element, value);
        }

        function sendFormEvent(form) {
            var action = form.data('ga-action') || 'submit';
            var type = form.data('ga-type') || 'form';
            var element = form.data('ga-element') || inferElement(form);
            var value = form.data('ga-value') || inferFormValue(form);

            sendEvent(action, type, element, value);
        }

        function inferLinkType(link) {
            if (isCta(link)) {
                return 'CTA';
            }

            if (isCard(link)) {
                return 'Card';
            }

            return 'PageLink';
        }

        function inferElement(domObject) {
            var parentSection = domObject.closest('[data-ga-section]');
            return parentSection ? parentSection.data('ga-section') : '';
        }

        function inferLinkValue(link) {
            if (link.text()) {
                return link.text();
            }
            return guessTitleFromLinkContents(link);
        }

        function inferVideoValue(video) {
            return video.find('source').attr('src');
        }

        function inferFormValue(form) {
            return form.attr('action');
        }

        function isCta(link) {
            var ctaClasses = ['button', 'cta'];
            var linkClasses = link.css();
            for (var index=0; index < ctaClasses.length; index++) {
                if (linkClasses.includes(ctaClasses[index])) {
                    return true;
                }
            }
            return false;
        }

        function isCard(link) {
            if (link.text()) {
                return false;
            }

            var cardClasses = ['card'];
            var linkClasses = link.css();
            for (var index=0; index < cardClasses.length; index++) {
                if (linkClasses.includes(cardClasses[index])) {
                    return true;
                }
            }
            return false;
        }

        function guessTitleFromLinkContents(link) {
            var titleElements = [
                'h1',
                'h2',
                'h3',
                'h4',
                'h5',
                'span',
                'p',
                'div'
            ];

            for (var index=0; index < titleElements.length; index++) {
                if (link.find(titleElements[index])) {
                    return titleElements[index].text();
                }
            }
            return '';
        }

        function sendEvent(action, type, element, value, linkDestination = null) {
            var event = {
                'event': 'gaEvent',
                'action': action,
                'type': type,
                'element': element,
                'value': value,
            };

            if (linkDestination) {
                event['destination'] = linkDestination;
            }

            window.dataLayer.push(event);
        }
    }

};

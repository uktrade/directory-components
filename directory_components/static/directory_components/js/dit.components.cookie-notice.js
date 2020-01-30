var dit = dit || {};
dit.components = dit.components || {};

dit.components.cookieNotice = function() {
  var COOKIE_NOTICE_ID = 'header-cookie-notice';
  var COOKIE_CLOSE_BUTTON_ID = 'dismiss-cookie-notice';
  var cookiePreferencesName = 'cookie_preferences_set';
  var cookiePreferencesDurationDays = 365;
  var cookiesPolicyName = 'cookies_policy';
  var cookiesPolicyDurationDays = 365;

  function setCookie (name, value, options) {
    if (typeof options === 'undefined') {
      options = {};
    }
    var cookieString = name + '=' + value + '; path=/';
    if (options.days) {
      var date = new Date();
      date.setTime(date.getTime() + options.days * 24 * 60 * 60 * 1000);
      cookieString = cookieString + '; expires=' + date.toGMTString();
    }
    if (document.location.protocol === 'https:') {
      cookieString = cookieString + '; Secure';
    }
    document.cookie = cookieString;
  }

  function getCookie (name) {
    var nameEQ = name + '=';
    var cookies = document.cookie.split(';');
    for (var i = 0, len = cookies.length; i < len; i++) {
      var cookie = cookies[i];
      while (cookie.charAt(0) === ' ') {
        cookie = cookie.substring(1, cookie.length);
      }
      if (cookie.indexOf(nameEQ) === 0) {
        return decodeURIComponent(cookie.substring(nameEQ.length));
      }
    }
    return null;
  }

  function getDefaultPolicy () {
    return {
      essential: true,
      settings: false,
      usage: false,
      campaigns: false
    };
  }

  function getPolicyOrDefault () {
    var cookie = getCookie(cookiesPolicyName);
    var policy = getDefaultPolicy();
    if (!cookie) return policy;

    try {
      var parsed = JSON.parse(cookie);

      policy.campaigns = parsed.campaigns || false;
      policy.usage = parsed.usage || false;
      policy.settings = parsed.settings || false;

    } catch (e) {
      return policy;
    }

    return policy;

  }

  function createPoliciesCookie (settings, usage, campaigns) {
    var policy = getDefaultPolicy();
    policy.settings = settings || false;
    policy.usage = usage || false;
    policy.campaigns = campaigns || false;
    var json = JSON.stringify(policy);
    setCookie(cookiesPolicyName, json, { days: cookiesPolicyDurationDays });
    return policy;
  }

  function hideCookieBanner (className) {
    var banner = document.querySelectorAll(className)[0];
    banner.classList.remove('block', 'confirmation-message');
  }

  function displayCookieBannerAcceptAll (cookieBannerClassName) {
    var banner = document.querySelectorAll(cookieBannerClassName)[0];
    banner.classList.add('confirmation-message');

    var hideButton = document.querySelectorAll('.cookie-close')[0];

      hideButton.addEventListener('click', function (e) {
        e.preventDefault();
        hideCookieBanner(cookieBannerClassName);
        }, false);

      hideButton.addEventListener('keydown', function(e) {
        if(e.which === 13 || e.which === 32) {
          hideCookieBanner(cookieBannerClassName);
        }
      });
  }

  function displayCookieBanner (className) {
    var banner = document.querySelectorAll(className)[0];
    banner.classList.add('block');
  }

  function bindAcceptAllCookiesButton (className, callBack) {
    var button = document.querySelectorAll(className)[0];
    button.addEventListener('click', callBack, false);
  }

  function setPreferencesCookie () {
    setCookie(cookiePreferencesName, 'true', { days: cookiePreferencesDurationDays });
  }

  function enableCookieBanner (bannerClassName, acceptButtonClassName) {
    displayCookieBanner(bannerClassName);
    bindAcceptAllCookiesButton(acceptButtonClassName, function (e) {
      e.preventDefault();
      createPoliciesCookie(true, true, true);
      setPreferencesCookie();
      displayCookieBannerAcceptAll(bannerClassName);

      window.dataLayer.push({
        'event': 'allowCookiePreferences',
        'value': [
          {
          'usage': true,
          },
        {
          'settings': true
        }
      ]
      });

      return false;
    });

  }

  function createCloseButton () {
    var $container = $('.cookie-notice-container');
    var $closeButton = $('<button>', {
      'class': 'cookie-close',
      'aria-controls': COOKIE_NOTICE_ID,
      'aria-label': 'Close this message',
      id: COOKIE_CLOSE_BUTTON_ID
    });
    $container.prepend($closeButton);
    return $closeButton;
  }

  function init (bannerClassName, acceptButtonClassName, cookiesPolicyUrl) {
    if (!bannerClassName) {
      throw 'Expected bannerClassName';
    }

    var preferenceCookie = getCookie(cookiePreferencesName);
    var isCookiesPage = document.URL.indexOf(cookiesPolicyUrl) !== -1;

    if ((!preferenceCookie) && !isCookiesPage) {
      enableCookieBanner(bannerClassName, acceptButtonClassName);
      createCloseButton();
    }
  }

  return {
    init: init,
    getPolicyOrDefault: getPolicyOrDefault,
    createPoliciesCookie: createPoliciesCookie,
    setPreferencesCookie: setPreferencesCookie
  };
}();

window.onload = function() {
  dit.components.cookieNotice.init('.cookie-notice', '.button-accept', 'cookies');
}

// dit.components.cookieNotice = (new function() {

//   var COOKIE_NOTICE_ID = 'header-cookie-notice';
//   var COOKIE_CLOSE_BUTTON_ID = 'dismiss-cookie-notice';
//   var COOKIE_DOMAIN = $('#privacyCookieDomain').attr('value');

//   function viewInhibitor(activate) {
//     var rule = '#header-cookie-notice { display: none; }';
//     var style;
//     if (arguments.length && activate) {
//       style = document.createElement('style');
//       style.setAttribute('type', 'text/css');
//       style.setAttribute('id', 'cookie-notice-view-inhibitor');
//       style.appendChild(document.createTextNode(rule));
//       document.head.appendChild(style);
//     }
//     else {
//       document.head.removeChild(document.getElementById('cookie-notice-view-inhibitor'));
//     }
//   };

//   // Hide on load
//   viewInhibitor(true);

//   setCookie = function(name, value, days) {
//     if (days) {
//       var date = new Date();
//       date.setTime(date.getTime() + (days * 24 * 60 * 60 * 1000));
//       value += '; expires=' + date.toGMTString();
//     }
//     document.cookie = name + '=' + value + '; domain=' + COOKIE_DOMAIN + ';path=/;';
//   }

//   getCookie = function(name) {
//     if (document.cookie.length > 0) {
//       var start = document.cookie.indexOf(name + '=');
//       if (start !== -1) {
//         start = start + name.length + 1;
//         var end = document.cookie.indexOf(';', start);
//         if (end == -1) {
//           end = document.cookie.length;
//         }
//         return unescape(document.cookie.substring(start, end));
//       }
//     }
//     return '';
//   }

//   hideNoticeAndSetCookie = function() {
//     $('#header-cookie-notice').hide();
//     setCookie('hide_cookie_notice', true, 30);
//   }

//   createCloseButton = function() {
//     var $container = $('.cookie-notice-container');
//     var $closeButton = $('<button>', {
//       'class': 'cookie-close',
//       'aria-controls': COOKIE_NOTICE_ID,
//       'aria-label': 'Close this message',
//       id: COOKIE_CLOSE_BUTTON_ID
//     });
//     $container.append($closeButton);
//     return $closeButton;
//   }

//   closeButtonEventHandler = function() {
//     var $button = createCloseButton();

//     $button.on('keydown', function(e) {
//       // Close on enter or space
//       if(e.which === 13 || e.which === 32) {
//         hideNoticeAndSetCookie();
//       }
//     });

//     $button.on('click', function(e) {
//       hideNoticeAndSetCookie();
//       e.preventDefault();
//     });
//   }

//   this.init = function() {
//     closeButtonEventHandler();
//     var showCookieNotice = !getCookie('hide_cookie_notice');
//     if (showCookieNotice) {
//       $('#header-cookie-notice').show();
//     } else {
//       $('#header-cookie-notice').hide();
//     }
//     viewInhibitor(false);
//   }

// });

// dit.components.cookieNotice = cookieNotice;



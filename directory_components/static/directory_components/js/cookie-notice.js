
function setCookie(name, value, days) {
  if (days) {
    var date = new Date();
    date.setTime(date.getTime() + (days * 24 * 60 * 60 * 1000));
    value += "; expires=" + date.toGMTString();
  }
  document.cookie = name + "=" + value + "; path=/";
}

function getCookie(name) {
  if (document.cookie.length > 0) {
    var start = document.cookie.indexOf(name + "=");
    if (start !== -1) {
      start = start + name.length + 1;
      var end = document.cookie.indexOf(";", start);
      if (end == -1) {
        end = document.cookie.length;
      }
      return unescape(document.cookie.substring(start, end));
    }
  }
  return "";
}

function hideNoticeAndSetCookie() {
  $('#header-cookie-notice').hide();
  setCookie('hide_cookie_notice', true, 30);
}

var showCookieNotice = !getCookie('hide_cookie_notice');

$(function() {
  if (showCookieNotice) {
    // Cookie notice is hidden by default to avoid it flashing as page loads
    // Show it again here if no cookie was found
    $('#header-cookie-notice').show();
  }
});

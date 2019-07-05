# Changelog


## 20.2.0
[Full Changelog](https://github.com/uktrade/directory-components/pull/227/files)

### Implemented enhancements
- Added `pagination` template tag


## 20.1.0
[Full Changelog](https://github.com/uktrade/directory-components/pull/226/files)

### Implemented enhancements
- Added `error_box` and `success_box` template tags
- Removed MANIFEST.in

## 20.0.1
[Full Changelog](https://github.com/uktrade/directory-components/pull/225/files)
### Bug fixes
- Fixed build on gov uk PaaS


## 20.0.0
[Full Changelog](https://github.com/uktrade/directory-components/pull/224/files)

### Breaking Changes
- Updated to version 18.x.x of directory-constants.

## 19.0.1
[Full Changelog](https://github.com/uktrade/directory-components/pull/223/files)

### Bug fixes
- Fixed too tall line height in header domestic/international links

## 19.0.0
[Full Changelog](https://github.com/uktrade/directory-components/pull/217/files)

### Implemented enhancements
- Added new tagging.js file to automatically tag links forms and videos.
- Added new ga360_data tag for customising data sent to GA360.
- Removed old methods for GA360 interaction tagging.
- Added GTM page to the demo app to explain how it all works

### Breaking Changes
- `ga360_tracker` has been removed.
- You can now (probably) just delete any existing `tagging.js` files. Most user interaction tagging will now be
performed automatically via the `tagging.js` file within directory components.
See the [google tag manager demo page](https://directory-components-dev.herokuapp.com/google-tag-manager/) for details of what's covered in the new system.
- `dit.components.greatDomesticHeader.js` has been removed from the base template. Each service will now need to explicitly load the JS file for the version of the header they are using e.g.

```
{% block header_js %}
    {{ block.super }}
    <script src="{% static 'directory_components/js/dit.components.greatDomesticHeader.js' %}"></script>
{% endblock %}
```

Or for international-facing services:

```
{% block header_js %}
    {{ block.super }}
    <script src="{% static 'directory_components/js/dit.components.greatInternationalHeader.js' %}"></script>
{% endblock %}
```


## 18.1.0

### Implemented enhancements
- Breadcrumbs template tag now supports context variables as first argument.

## 18.0.0

### Implemented enhancements
- Breadcrumbs template tag now is more flexible: supports any number of levels simplifies most usecases.

### Breaking changes
- Remove support for python 3.5
- breadcrumbs template tag interface has changed:

#### before
1. `{% breadcrumbs left_url='/' left_label='Home' right_label='Statistics' %}`
2. `{% breadcrumbs left_url='/' left_label='Home' middle_url='/middle/' middle_label='middle' right_label='Statistics' %}`

#### after
1. `{% breadcrumbs 'Statistics' %}<a href="/">Home</a>{% endbreadcrumbs %}`
2. `{% breadcrumbs 'Statistics' %}<a href="/">Home</a><a href="/middle/">middle</a>{% endbreadcrumbs %}`


## 17.0.0

### Implemented enhancements
- Removed Overpass semibold (600) weight from font imports
- Add CSS sourcemaps to aid style debugging in local dev

### Bug fixes
- Fixed margins on .underline class when used in the stats component

### Breaking changes
- `card-grid` CSS class has been removed in favour of the more descriptive `flex-grid`
- Images used in card components (excluding `labelled_image_card`) now use the image's original aspect ratio. If the aspect ratios of multiple images used in a grid of cards do not match, their heights will no longer be aligned. In this case, please update your images to all be the same aspect ratio

## 16.5.0
[Full Changelog](https://github.com/uktrade/directory-components/pull/218/files)

### Implemented enhancements
 - Added `handler404` so 404 pages render urls correctly.
 - Added `handler500` so 500 pages render urls correctly.

## 16.4.0
[Full Changelog](https://github.com/uktrade/directory-components/pull/216/files)

### Implemented enhancements
- Added message box with icon component
- Improved mobile style of message box
- Updated documentation
- Added 500 error page template based on [gov.uk design system](https://design-system.service.gov.uk/patterns/problem-with-the-service-pages/)

### Bug fixes
- Fixed invalid property values

## 16.3.0
[Full Changelog](https://github.com/uktrade/directory-components/pull/215/files)

### Implemented enhancements
- Added support for Django 2 -> 2.2

## 16.2.0
[Full Changelog](https://github.com/uktrade/directory-components/pull/213/files)

### Implemented enhancements
- Gave `hero_with_cta` a min-height of 350px

## 16.1.0
[Full Changelog](https://github.com/uktrade/directory-components/pull/210/files)

### Implemented enhancements
- Added ga360_tracker tag for adding GA360 attributes to components.

## 16.0.1
[Full Changelog](https://github.com/uktrade/directory-components/pull/211/files)

### Breaking changes
- Fixed leaking of information between ga360_payload in different requests

## 16.0.0
[Full Changelog](https://github.com/uktrade/directory-components/pull/209/files)
### Implemented enhancements
- Added separate isd url via directory-constants context processor

### Breaking changes
- Added separate isd url please set DIRECTORY_CONSTANTS_URL_INVESTMENT_SUPPORT_DIRECTORY in all dev environments

## [15.2.0](https://pypi.org/project/directory-constants/15.2.0/) (2019-06-03)
[Full Changelog](https://github.com/uktrade/directory-components/pull/208/files)

### Implemented enhancements
- Added contact form office finder url to urls_processor

## 15.1.1
[Full Changelog](https://github.com/uktrade/directory-components/pull/205/files)

### Implemented enhancements
- CI-108: Improve error handling to be simpler and give more informative error messages.

## 15.1.0
[Full Changelog](https://github.com/uktrade/directory-components/pull/200/files)

### Implemented enhancements

- Added `header_footer/invest_header` using invest logo specifically for invest pages

## 15.0.1
[Full Changelog](https://github.com/uktrade/directory-components/pull/204/files)

### Bug Fixes
- CI-108: Fix GA360 Mixin failing when request.sso_user is unset.

## 15.0.0
[Full Changelog](https://github.com/uktrade/directory-components/pull/197/files)

### Implemented enhancements
- CI-108: Added middleware to check that all views have appropriate GA tags have been set or marked as 'skip_ga360'
- CI-108: Updated International Header GA tagging to match the new specification

### Breaking changes
- Changed the ga_payload format for the GA360Mixin. (see mixins.GA360Payload for details).

## 14.1.0
[Full Changelog](https://github.com/uktrade/directory-components/pull/202/files)

**Implemented enhancements:**

- Added GA360 tagging for the domestic header
- Cleaned up unused templates and js

## 14.0.0
[Full Changelog](https://github.com/uktrade/directory-components/pull/199/files)

### Breaking Changes

- Rename all instances of `directory_components_tags` to `directory_components`

The best way to do the rest of the upgrade is to switch to using the latest header/footer.

- CSS to do with the old header/footer have been removed.
- Feature flag no longer used:
    - `NEW_HEADER_FOOTER_ON`
- Six templates have been removed:
    - `header_footer/invest_footer.html`
    - `header_footer/invest_header.html`
    - `header_footer_old/footer.html`
    - `header_footer_old/header.html`
    - `header_footer_old/header_international_link_js_disabled.html`
    - `header_footer_old/header_static.html`
- Images removed:
    - `IIG_Invest_in_GREAT_White_WITH_Flag.png`
    - `UK-Gov_STACK_WHITE_AW.png`
- JavaScript files removed:
    - `invest-header.js`
- Templates renamed/moved:
    - `header_footer/header_static.html` changed to `header_footer/domestic_header_static.html`
    - `header_footer/footer.html` changed to `header_footer/domestic_footer.html`
    - `header_footer/header.html` changed to `header_footer/domestic_header.html`


## 13.2.0
[Full Changelog](https://github.com/uktrade/directory-components/pull/201/files)

**Implemented enhancements:**

- Added if statements to 'informative banner' so label or content can be used without the other


## 13.1.0
[Full Changelog](https://github.com/uktrade/directory-components/pull/200/files)

**Implemented enhancements:**

- Added Investment Support Directory URL


## 13.0.0
[Full Changelog](https://github.com/uktrade/directory-components/pull/198/files)

### Implemented enhancements
- CMS-1528: Add a feature flag for the country selector in the international header.

### Breaking Changes
- All apps using this library must now provide the 'COUNTRY_SELECTOR_ON' feature flag in their settings file.

## 12.1.1
[Full Changelog](https://github.com/uktrade/directory-components/pull/196/files)

### Bug fixes:
- Set text direction in country selector so English text displays correctly on pages in Arabic

## 12.1.0
[Full changelog](https://github.com/uktrade/directory-components/pull/187)

### Bug fixes:

- CMS-1245 Changed default country selector text to "Select a country"

## 12.0.0
[Full Changelog](https://github.com/uktrade/directory-components/pull/193/files)

### Implemented enhancements:
- Improved mobile/tablet styling of full width banner/case study component, added examples to docs
- Added non-responsive classes for widths
- Added responsive display classes

### Breaking changes:
- `full_width_banner_with_cta` inclusion tag has been renamed to `case_study`
- `full-width-banner-with-cta` CSS class has been renamed to `case-study`

## 11.0.4
[Full Changelog](https://github.com/uktrade/directory-components/pull/195/files)

### Bug fixes:
- [[CI-108]](https://uktrade.atlassian.net/browse/CI-108) Fix potential bug where `dit.tagging` is undefined.

## 11.0.3
[Full Changelog](https://github.com/uktrade/directory-components/pull/194/files)

### Bug fixes:
- [[CMS-1460]](https://uktrade.atlassian.net/browse/CMS-1460) Fix spacing issues of language/country selector on some browsers.

## 11.0.2
[Full Changelog](https://github.com/uktrade/directory-components/pull/192/files)

### Bug fixes:
- [[CI-108]](https://uktrade.atlassian.net/browse/CI-108) Fix applying tags to international header.

## 11.0.1
[Full Changelog](https://github.com/uktrade/directory-components/pull/190/files)

### Bug fixes:

- [[CI-120]](https://uktrade.atlassian.net/browse/CI-120) Fixed language selector cutting off the language text on firefox

## 11.0.0
[Full Changelog](https://github.com/uktrade/directory-components/pull/189/files)

### Upgrade instructions
- Rename references to `dit.tagging.internatinalHeader.js` to `dit.tagging.internationalHeader.js`

### Fixed Bugs
- Fix typo in filename of `dit.tagging.internationalHeader.js`

## 10.9.2

[Full Changelog](https://github.com/uktrade/directory-components/pull/188/files)

### Implemented Enhancements:

- Added 'UK setup guide' to the international header.

## 10.9.1
[Full Changelog](https://github.com/uktrade/directory-components/pull/182/files)

**Implemented Enhancements**

- Add GA tagging script for the international header.

## 10.9.0

[Full Changelog](https://github.com/uktrade/directory-components/pull/184/files)

- [[CMS-1395]](https://uktrade.atlassian.net/browse/CMS-1395) PersistLocaleMiddleware deletes deprecated cookie names


## 10.8.3

[Full Changelog](https://github.com/uktrade/directory-components/pull/186/files)

### Bug fixes:

- Improved accessibility of breadcrumbs components based on [WAI-ARIA guidelines](https://www.w3.org/TR/wai-aria-practices/examples/breadcrumb/index.html)

## 10.8.2

[Full Changelog](https://github.com/uktrade/directory-components/pull/183/files)

### Bug fixes:

- Improved contrast on international header language dropdown for better accessibility

## 10.8.1

[Full Changelog](https://github.com/uktrade/directory-components/pull/181/files)

### Bug fixes:

- Specified support for python 3.6 in setup.py

## 10.8.0

[Full Changelog](https://github.com/uktrade/directory-components/pull/178/files)

### Implemented Enhancements:

- Add breadcrumbs template tag that supports two and three levels.

## 10.7.0

[Full Changelog](https://github.com/uktrade/directory-components/pull/180/files)

### Implemented Enhancements:

- [[CMS-1258]](https://uktrade.atlassian.net/browse/CMS-1258) Add background-tint and section-id capability to full_width_banner_with_cta her banner

## 10.6.0

[Full Changelog](https://github.com/uktrade/directory-components/pull/179/files)

### Implemented Enhancements:

- [[CI-108]](https://uktrade.atlassian.net/browse/CI-108) Add mixin for Google Analytics Tags.

## 10.5.0

[Full Changelog](https://github.com/uktrade/directory-components/pull/177/files)

### Implemented Enhancements:

- [[CMS-1386]](https://uktrade.atlassian.net/browse/CMS-1386) Add block to base template for adding content after error-reporting banner

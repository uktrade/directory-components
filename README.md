# directory-components

[![circle-ci-image]][circle-ci]
[![codecov-image]][codecov]
[![pypi-image]][pypi]

**Reusable components used across the directory applications for the Department for International Trade.**

---

## Installation

```shell
pip install directory-components
```

## Development

    $ git clone https://github.com/uktrade/directory-components
    $ cd directory-components


## Demo

Install the demo requirements:

    $ make demo_requirements

To view the components in the browser run the following command:

    $ make run_demo

and go to `0.0.0.0:9013` in your browser

To test cookies locally add this to your /etc/hosts:

```
127.0.0.1       components.trade.great
```

Then visit the demo at `components.trade.great:9013`

## Features

### Environment variables

| Environment variable | Notes |
|-------------------------------------------- |-----------------------------------------------|
| `FEATURE_SEARCH_ENGINE_INDEXING_DISABLED`   | Controls `RobotsIndexControlHeaderMiddlware`. |
| `FEATURE_MAINTENANCE_MODE_ENABLED`          | Controls `MaintenanceModeMiddleware`.         |
| `FEATURE_FLAGS`                             | Place to store the service's feature flags.   |
| `IP_RESTRICTOR_REMOTE_IP_ADDRESS_RETRIEVER` | Method for determining client IP address: 'govuk-paas' or 'ipware'
| `IP_RESTRICTOR_SKIP_CHECK_ENABLED`          | Flag to enable skipping IP check if cookie is valid |
| `IP_RESTRICTOR_SKIP_CHECK_SENDER_ID`        | The shared sender id for skipping IP check     |
| `IP_RESTRICTOR_SKIP_CHECK_SECRET`           | The shared secret for skipping IP check        |


### Middleware

Middleware can be found in `directory_components.middleware.FooBar`.

| Middleware | Notes |
|------------|-------|
| `RobotsIndexControlHeaderMiddlware` | Informs the webcrawlers to not index the service if `FEATURE_SEARCH_ENGINE_INDEXING_DISABLED` is `true`. |
| `MaintenanceModeMiddleware`         | Redirects to http://sorry.great.gov.uk if `FEATURE_MAINTENANCE_MODE_ENABLED` is `true`.|
| `NoCacheMiddlware`                  | Prevents any page in the service from caching pages of logged in users. |
| `PrefixUrlMiddleware`               | Redirects use from unprefixed url to prefixed url if `FEATURE_URL_PREFIX_ENABLED` is `true`. |
| `IPRestrictorMiddleware`            | Convinience wrapper around (django-admin-ip-restrictor)[pypi.org/project/django-admin-ip-restrictor/]. |


### Context processors

Middleware can be found in `directory_components.context_processors.foo_bar`.

| Processor | Context variable name | Notes |
|-----------|-----------------------|-------|
| `sso_processor` | | Exposes the state of the SSO user. |
| `analytics` | `directory_components_analytics` | GA details. Used by base template. |
| `header_footer_processor` | `header_footer_urls` | Urls used by base template's header and footer. |
| `urls_processor` | `directory_components_urls` | More urls used by base template's header and footer. |
| `feature_flags` | `feature_flags` | Exposes the service's feature flags. |

## Auto update services dependency

To automatically update the dependences of services that use this library call the following command:

    $ make update

## Publish to PyPI

The package should be published to PyPI on merge to master. If you need to do it locally then get the credentials from rattic and add the environment variables to your host machine:

| Setting                      |
| ----------------------------- |
| `DIRECTORY_PYPI_USERNAME`     |
| `DIRECTORY_PYPI_PASSWORD`     |


Then run the following command:

    make publish


[code-climate-image]: https://codeclimate.com/github/uktrade/directory-components/badges/issue_count.svg
[code-climate]: https://codeclimate.com/github/uktrade/directory-components

[circle-ci-image]: https://circleci.com/gh/uktrade/directory-components/tree/master.svg?style=svg
[circle-ci]: https://circleci.com/gh/uktrade/directory-components/tree/master

[codecov-image]: https://codecov.io/gh/uktrade/directory-components/branch/master/graph/badge.svg
[codecov]: https://codecov.io/gh/uktrade/directory-components

[pypi-image]: https://badge.fury.io/py/directory-components.svg
[pypi]: https://badge.fury.io/py/directory-components

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
|--------------------------------------------------- |------------------------------------------------|
| `FEATURE_MAINTENANCE_MODE_ENABLED`                 | Controls `MaintenanceModeMiddleware`.          |
| `FEATURE_FLAGS`                                    | Place to store the service's feature flags.    |
| `DIRECTORY_COMPONENTS_VAULT_DOMAIN`                | Hashicorp vault domain. For diffing vaults.    |
| `DIRECTORY_COMPONENTS_VAULT_ROOT_PATH`             | Hashicorp vault root path. For diffing vaults. |
| `DIRECTORY_COMPONENTS_VAULT_PROJECT`               | Hashicorp vault project. For diffing vaults.   |
| `DIRECTORY_COMPONENTS_VAULT_IGNORE_SETTINGS_REGEX` | Settings to ignore when diffing vaults.        |

### Middleware

Middleware can be found in `directory_components.middleware.FooBar`.

| Middleware | Notes |
|------------|-------|
| `MaintenanceModeMiddleware`         | Redirects to http://sorry.great.gov.uk if `FEATURE_MAINTENANCE_MODE_ENABLED` is `true`.|
| `NoCacheMiddlware`                  | Prevents any page in the service from caching pages of logged in users. |
| `PrefixUrlMiddleware`               | Redirects use from unprefixed url to prefixed url. |


### Context processors

Middleware can be found in `directory_components.context_processors.foo_bar`.

| Processor | Context variable name | Notes |
|-----------|-----------------------|-------|
| `sso_processor` | | Exposes the state of the SSO user. |
| `analytics` | `directory_components_analytics` | GA details. Used by base template. |
| `header_footer_processor` | `header_footer_urls` | Urls used by base template's header and footer. |
| `urls_processor` | `directory_components_urls` | More urls used by base template's header and footer. |
| `feature_flags` | `feature_flags` | Exposes the service's feature flags. |

### Exception handlers

Add the following to your urls.py for directory components templates to be used on 404 and 500

```
handler404 = 'directory_components.views.handler404'

handler500 = 'directory_components.views.handler500'
```

Without doing this the 500 and 400 pages would not receive context data provided by context processors

## Auto update services dependency

To automatically update the dependences of services that use this library call the following command:

    $ make update

## Settings janitor

Management commands are provided to assist in the maintenance of settings. Install by `pip install directory-components[janitor]` and then add the following to `settings.py`:

    if some_predicate_is_met:  # feature flagged so it's not used in prod
        INSTALLED_APPS.append('directory_components.janitor')


### Diff environments

You can diff the vaults of two environments by running the following.

    manage.py environment_diff \
        --token=<token> \
        --domain=<domain> \
        --root=<root> \
        --project=<project> \
        --environment_a=<environment_a> \
        --environment_b=<environment_b>

For simplicity once you set the `DIRECTORY_COMPONENTS_VAULT_DOMAIN`, `DIRECTORY_COMPONENTS_VAULT_PROJECT`, and `DIRECTORY_COMPONENTS_VAULT_ROOT_PATH` that simplifies to

    manage.py environment_diff \
        --token=<token> \
        --environment_a=<environment_a> \
        --environment_b=<environment_b>


### Detect settings orphans

You can detect settings that are either unused in the codebase, redundant because they're explicitly set to the default django value, or obsolete because they're set in the vault but not used anywhere:

    manage.py settings_shake \
        --token=<token> \
        --root=<root> \
        --domain=<domain> \
        --project=<project> \
        --environment=<environment>

For simplicity once you set the `DIRECTORY_COMPONENTS_VAULT_DOMAIN`, `DIRECTORY_COMPONENTS_VAULT_PROJECT`, and `DIRECTORY_COMPONENTS_VAULT_ROOT_PATH` that simplifies to

    manage.py settings_shake \
        --token=<token> \
        --environment=<environment>


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

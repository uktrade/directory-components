# directory-components

[![code-climate-image]][code-climate]
[![circle-ci-image]][circle-ci]
[![codecov-image]][codecov]
[![gemnasium-image]][gemnasium]

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

To view the components in the browser run the following command:

    $ ./manage.py runserver --settings=demo.settings 0.0.0.0:9000

and go to `localhost:9000` in your browser


## Publish to PyPI

The package should be published to PyPI on merge to master. If you need to do it locally then get the credentials from rattic and add the environment variables to your host machine:

| Setting                     |
| --------------------------- |
| DIRECTORY_PYPI_USERNAME     |
| DIRECTORY_PYPI_PASSWORD     |


Then run the following command:

    make publish


[code-climate-image]: https://codeclimate.com/github/uktrade/directory-components/badges/issue_count.svg
[code-climate]: https://codeclimate.com/github/uktrade/directory-components

[circle-ci-image]: https://circleci.com/gh/uktrade/directory-components/tree/master.svg?style=svg
[circle-ci]: https://circleci.com/gh/uktrade/directory-components/tree/master

[codecov-image]: https://codecov.io/gh/uktrade/directory-components/branch/master/graph/badge.svg
[codecov]: https://codecov.io/gh/uktrade/directory-components

[gemnasium-image]: https://gemnasium.com/badges/github.com/uktrade/directory-components.svg
[gemnasium]: https://gemnasium.com/github.com/uktrade/directory-components

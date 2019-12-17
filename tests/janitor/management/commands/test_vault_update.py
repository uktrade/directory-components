from unittest import mock
import io

import pytest
from colors import red, green

from django.core.management import call_command

from directory_components.janitor.management.commands import helpers


@pytest.fixture(autouse=True)
def mock_client():
    patched = mock.patch('hvac.Client', mock.Mock(is_authenticated=True))
    yield patched.start()
    patched.stop()


@pytest.fixture(autouse=True)
def mock_get_secrets():
    patched = mock.patch.object(
        helpers,
        'get_secrets',
        return_value={'EXAMPLE_A': 'foo.uktrade.io'}
    )
    yield patched.start()
    patched.stop()


@pytest.fixture(autouse=True)
def mock_list_vault_paths():
    patched = mock.patch.object(
        helpers,
        'list_vault_paths',
        return_value=['foo/bar/baz']
    )
    yield patched.start()
    patched.stop()


def mutator(secrets, path):
    for key, value in secrets.items():
        secrets[key] = value.replace('uktrade.io', 'uktrade.digital')
    return secrets


@mock.patch('builtins.input', return_value=0)  # index of `Yes'
def test_vault_update(mock_input, mock_get_secrets):
    out = io.StringIO()

    call_command(
        'vault_update',
        token='secret-token',
        domain='example.com',
        mutator=mutator,
        stdout=out
    )

    assert red("- {'EXAMPLE_A': 'foo.uktrade.io'}") in mock_input.call_args[0][0]
    assert green("+ {'EXAMPLE_A': 'foo.uktrade.digital'}") in mock_input.call_args[0][0]

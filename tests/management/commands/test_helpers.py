from unittest import mock

from directory_components.management.commands import helpers


def test_prompt_user_choice(monkeypatch):
    mock_input = mock.Mock(return_value='0')

    monkeypatch.setitem(__builtins__, 'input', mock_input)

    helpers.prompt_user_choice(
        message='Choose a thing',
        options=['Option A', 'Option B']
    )
    assert mock_input.call_count == 1
    assert mock_input.call_args == mock.call(
        'Choose a thing:\n\n[0] Option A\n[1] Option B\n\n'
    )


def test_clean_secrets_default():
    secrets = {
        'SECRET_KEY': '123',
        'PASSWORD': '123',
        'MAGIC_TOKEN': '123',
        'API_KEY': '123',
        'BENIGN': True,
    }
    assert helpers.clean_secrets(secrets) == {'BENIGN': True}


def test_clean_secrets_explicit(settings):
    settings.DIRECTORY_COMPONENTS_VAULT_IGNORE_SETTINGS_REGEX = []

    secrets = {
        'SECRET_KEY': '123',
        'PASSWORD': '123',
        'MAGIC_TOKEN': '123',
        'API_KEY': '123',
        'BENIGN': True,
    }
    assert helpers.clean_secrets(secrets) == secrets


def test_get_secrets():
    mock_client = mock.Mock()
    mock_client.read.return_value = {
        'data': {
            'API_KEY': '123',
            'BENIGN': True,
        }
    }

    result = helpers.get_secrets(client=mock_client, path='/root/foo')

    assert result == {'BENIGN': True}
    assert mock_client.read.call_count == 1
    assert mock_client.read.call_args == mock.call(path='/root/foo')


def test_get_secrets_wizard(monkeypatch):
    mock_input = mock.Mock()
    mock_client = mock.Mock()

    monkeypatch.setitem(__builtins__, 'input', mock_input)
    mock_client.read.return_value = {
        'data': {
            'API_KEY': '123',
            'BENIGN': True,
        }
    }
    mock_client.list.side_effect = [
        {'data': {'keys': ['project-one', 'project-two', 'project-three']}},
        {'data': {'keys': ['environment-one', 'environment-two']}}
    ]
    mock_input.side_effect = ['0', '1']

    helpers.get_secrets_wizard(client=mock_client, root='/root/')

    assert mock_input.call_count == 2
    assert mock_input.call_args == mock.call(
        '(/root/project-one) Choose an environment::\n\n[0] environment-one\n[1] environment-two\n\n'
    )


@mock.patch.object(helpers.Vulture, 'get_unused_code')
def test_vulture_filters_non_settings(mock_get_unused_code):
    one = mock.Mock(**{'get_report.return_value': 'conf/settings.py'})
    one.name = 'FOO'
    two = mock.Mock(**{'get_report.return_value': 'conf/settings.py'})
    two.name = 'BAR'
    three = mock.Mock(**{'get_report.return_value': 'views/view.py'})

    mock_get_unused_code.return_value = [one, two, three]

    vulture = helpers.Vulture(
        verbose=False,
        ignore_names=[],
        ignore_decorators=False
    )
    assert list(vulture.report()) == ['FOO', 'BAR']

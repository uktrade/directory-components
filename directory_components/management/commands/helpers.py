import difflib
from pprint import pformat
import re
from urllib.parse import urljoin

from django.conf import settings


DEFAULT_UNSAFE_SETTINGS = [
    re.compile('.*?SECRET.*?'),
    re.compile('.*?PASSWORD.*?'),
    re.compile('.*?TOKEN.*?'),
    re.compile('.*?KEY.*?'),
]
VAULT_ROOT_PATH = '/dit/directory/'


def get_secrets_wizard(client):
    response = client.list(path=VAULT_ROOT_PATH)
    project = prompt_user_choice(
        message='{VAULT_ROOT_PATH} Choose a projects:',
        options=response['data']['keys'],
    )

    response = client.list(path=f'{VAULT_ROOT_PATH}/{project}')
    environment = prompt_user_choice(
        message='({VAULT_ROOT_PATH}/{project}) Choose an environment:',
        options=response['data']['keys'],
    )

    return get_secrets(
        client=client,
        path=urljoin(project, environment),
    )


def prompt_user_choice(message, options):
    display = '\n'.join([f'{[i]} {option}' for i, option in enumerate(options)])
    index = int(input(f'{message}:\n\n{display}\n\n'))
    return options[index]


def clean_secrets(secrets):
    ignore_settings = getattr(
        settings,
        'DIRECTORY_COMPONENTS_VAULT_IGNORE_SETTINGS_REGEX',
        DEFAULT_UNSAFE_SETTINGS
    )
    for key in secrets.copy():
        for entry in ignore_settings:
            if entry.match(key):
                del secrets[key]
                break
    return secrets


def get_secrets(client, path):
    print(path)
    print(urljoin(VAULT_ROOT_PATH, path))
    response = client.read(path=urljoin(VAULT_ROOT_PATH, path))
    return clean_secrets(response['data'])


def diff_dicts(dict_a, dict_b):
    differ = difflib.Differ()
    return '\n'.join(difflib.ndiff(
       pformat(secrets_a).splitlines(),
       pformat(secrets_b).splitlines()
    ))

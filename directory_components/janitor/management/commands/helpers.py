import difflib
from pprint import pformat
import re
from urllib.parse import urljoin

from vulture import Vulture

from django.conf import settings


DEFAULT_UNSAFE_SETTINGS = [
    re.compile('.*?PASSWORD.*?'),
    re.compile('.*?SECRET.*?'),
    re.compile('.*?AUTHORIZATION.*?'),
    re.compile('.*?KEY.*?'),
    re.compile('.*?TOKEN.*?'),
    re.compile('.*?DSN.*?'),
]


def get_secrets_wizard(client, root):
    response = client.list(path=root)
    project = prompt_user_choice(
        message=f'{root} Choose a projects:',
        options=response['data']['keys'],
    )

    response = client.list(path=f'{root}/{project}')
    environment = prompt_user_choice(
        message=f'({root}{project}) Choose an environment:',
        options=response['data']['keys'],
    )

    return get_secrets(
        client=client,
        path=f'{root}{project}{environment}',
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
                secrets[key] = '💀' * 5
                break
    return secrets


def get_secrets(client, path):
    response = client.read(path=path)
    return clean_secrets(response['data'])


def diff_dicts(dict_a, dict_b):
    return '\n'.join(difflib.ndiff(
       pformat(dict_a).splitlines(),
       pformat(dict_b).splitlines()
    ))


class Vulture(Vulture):
    def report(self, min_confidence=0):
        for unused_code in self.get_unused_code(min_confidence=min_confidence):
            report = unused_code.get_report()
            if 'conf/settings.py' in report:
                yield unused_code.name

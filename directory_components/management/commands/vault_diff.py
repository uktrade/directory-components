import difflib
import json
from pprint import pformat
import re

import hvac

from django.conf import settings
from django.core.management.base import BaseCommand, CommandError


DEFAULT_UNSAFE_SETTINGS = [
    re.compile('.*?SECRET.*?'),
    re.compile('.*?PASSWORD.*?'),
    re.compile('.*?TOKEN.*?'),
    re.compile('.*?KEY.*?'),
]


class Command(BaseCommand):

    help = 'Diff the vault of two environments.'
    root_path = '/dit/directory'

    def add_arguments(self, parser):
        parser.add_argument(
            '--token',
            help='Vault token. Retrieve by clicking "copy token" on Vault UI.'
        )
        parser.add_argument(
            '--domain',
            default=getattr(settings, 'DIRECTORY_COMPONENTS_VAULT_URL', None),
            help='Vault domain. The domain you uses to access the UI.'
        )
        parser.add_argument(
            '--wizard',
            action='store_true',
            help='Select the projects and environments from a list.'
        )
        parser.add_argument(
            '--project',
            default=getattr(settings, 'DIRECTORY_COMPONENTS_VAULT_PROJECT', None),
            help='The name of the project you want to diff.'
        )
        parser.add_argument(
            '--environment_a',
            required=False,
            help='The first environment to compare (against environment_a).'
        )
        parser.add_argument(
            '--environment_b',
            required=False,
            help='The second environment to compare (against environment_b).'
        )

    def handle(self, *args, **options):
        self.client = hvac.Client(
            url=f"https://{options['domain']}", token=options['token']
        )
        assert self.client.is_authenticated()

        if options['wizard']:
            secrets_a = self.get_secrets_wizard()
            secrets_b = self.get_secrets_wizard()
        else:
            secrets_a = self.get_secrets(
                project=options['project'],
                environment=options['environment_a'],
            )
            secrets_b = self.get_secrets(
                project=options['project'],
                environment=options['environment_b'],
            )
        differ = difflib.Differ()
        diff = '\n'.join(difflib.ndiff(
           pformat(secrets_a).splitlines(),
           pformat(secrets_b).splitlines()
        ))
        self.stdout.write(f'\n{diff}')

    def get_secrets(self, project, environment):
        response = self.client.read(path=f'{self.root_path}/{project}/{environment}')
        return self.clean_secrets(response['data'])

    def get_secrets_wizard(self):
        response = self.client.list(path=self.root_path)
        project = self.prompt_user_choice(
            message='{root_path} Choose a projects:',
            options=response['data']['keys'],
        )

        response = self.client.list(path=f'{self.root_path}/{project}')
        environment = self.prompt_user_choice(
            message='({root_path}/{project}) Choose an environment:',
            options=response['data']['keys'],
        )

        response = self.get_secrets(project=project, environment=environment)
        return self.clean_secrets(response['data'])

    def prompt_user_choice(self, message, options):
        display = '\n'.join([f'{[i]} {option}' for i, option in enumerate(options)])
        index = int(input(
            self.style.SUCCESS(f'{message}:\n\n{display}\n\n')
        ))
        return options[index]

    def clean_secrets(self, secrets):
        ignore_settings = getattr(
            settings,
            'DIRECTORY_COMPONENTS_VAULT_IGNORE_SETTINGS_REGEX',
            DEFAULT_IGNORE_SETTINGS
        )
        for key in secrets.copy():
            for entry in ignore_settings:
                if entry.match(key):
                    del secrets[key]
                    break
        return secrets

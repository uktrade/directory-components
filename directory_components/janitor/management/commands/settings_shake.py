import hvac

from django.conf import global_settings, settings

from django.core.management.base import BaseCommand, CommandError
from django.core.management.commands.diffsettings import module_to_dict

from directory_components.janitor.management.commands import helpers



class Command(BaseCommand):
    help_text = 'Shake the settings and see what falls off. Like tree-shaking.'

    def add_arguments(self, parser):
        parser.add_argument(
            '--token',
            help='Vault token. Retrieve by clicking "copy token" on Vault UI.'
        )
        parser.add_argument(
            '--domain',
            default=getattr(settings, 'DIRECTORY_COMPONENTS_VAULT_DOMAIN', None),
            help='Vault domain. The domain you uses to access the UI.'
        )
        parser.add_argument(
            '--wizard',
            action='store_true',
            help='Select the projects and environments from a list.'
        )
        parser.add_argument(
            '--root',
            default=getattr(settings, 'DIRECTORY_COMPONENTS_VAULT_ROOT_PATH', None),
            help='The vault root path your projects are within.'
        )
        parser.add_argument(
            '--project',
            default=getattr(settings, 'DIRECTORY_COMPONENTS_VAULT_PROJECT', None),
            help='The name of the project you want to check orphans of.'
        )
        parser.add_argument(
            '--environment',
            required=False,
            help='The environment to check for orphans.'
        )

    def handle(self, *args, **options):
        obsolete = self.report_obsolete_vault_entries(options)
        unused = self.report_unused_settings()
        redundant = self.report_redundant_settings()
        self.report_results(
            success_message='No obsolete vault entries found.',
            warning_message='These vault entries seem obsolete. Consider deleting them:',
            warnings=obsolete,
        )
        self.report_results(
            success_message='No unused settings found.',
            warning_message='These settings seem unused. Consider deleting them:',
            warnings=unused,
        )
        self.report_results(
            success_message='No redundant settings found.',
            warning_message='These settings seem redundant. Consider deleting them:',
            warnings=redundant,
        )

    def report_obsolete_vault_entries(self, options):
        url = f"https://{options['domain']}"
        client = hvac.Client(url=url, token=options['token'])
        assert client.is_authenticated()

        label = self.style.MIGRATE_LABEL('Looking for obsolete vault entries.')
        self.stdout.write(label)

        if options['wizard']:
            secrets = helpers.get_secrets_wizard(client=client, root=options['root'])
        else:
            secrets = helpers.get_secrets(
                client=client,
                path=f"{options['root']}/{options['project']}/{options['environment']}",
            )
        return [key for key in secrets if not hasattr(settings, key)]

    def report_redundant_settings(self):
        self.stdout.write(
            self.style.MIGRATE_LABEL('Looking for redundant settings')
        )

        settings_dict = module_to_dict(settings)
        default_settings = module_to_dict(global_settings)

        warnings = []
        for key, value in settings_dict.items():
            if key in default_settings and settings.is_overridden(key):
                if value == default_settings[key]:
                    warnings.append(key)
        return warnings

    def report_unused_settings(self):
        self.stdout.write(
            self.style.MIGRATE_LABEL('Looking for unused settings')
        )
        vulture = helpers.Vulture(
            verbose=False,
            ignore_names=[],
            ignore_decorators=False
        )
        vulture.scavenge(['.'])
        return vulture.report()

    def report_results(self, warning_message, success_message, warnings):
        if warnings:            
            warnings = '\n'.join(warnings)
            self.stdout.write(
                self.style.WARNING(f'{warning_message}\n{warnings}\n\n')
            )
        else:
            self.stdout.write(self.style.SUCCESS(success_message))

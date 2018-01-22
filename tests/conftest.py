def pytest_configure():
    from django.conf import settings
    settings.configure(
        INSTALLED_APPS=[
            'django.contrib.staticfiles',
            'directory_components',
        ],
        STATIC_URL='/static/',
        TEMPLATES=[
            {
                'BACKEND': 'django.template.backends.django.DjangoTemplates',
                'OPTIONS': {
                    'loaders': [
                        'django.template.loaders.app_directories.Loader',
                    ],
                },
            },
        ]
    )

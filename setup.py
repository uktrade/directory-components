from setuptools import setup, find_packages


setup(
    name='directory_components',
    version='3.4.0',
    url='https://github.com/uktrade/directory-components',
    license='MIT',
    author='Department for International Trade',
    description='Shared components library for Export Directory.',
    packages=find_packages(exclude=["tests.*", "tests", "scripts", "demo.*"]),
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    include_package_data=True,
    install_requires=[
        'django>=1.9,<2.0a1',
        'export_elements>=0.22.0<=1.0.0',
        'beautifulsoup4>=4.6.0<5.0.0',
        'django-admin-ip-restrictor>=1.0.0,<2.0.0',
        'mohawk>=0.3.4,<1.0.0',
        'directory-constants>=11.1.0,<12.0.0',
    ],
    extras_require={
        "test": [
            "ansicolors==1.1.8",
            "codecov==2.0.9",
            "flake8==3.0.4",
            "pytest-cov==2.3.1",
            "pytest-django==3.0.0",
            "pytest-sugar",
            "pytest==3.0.3",
            "requests-toolbelt==0.8.0",
            "requests==2.18.1",
            "twine>=1.11.0,<2.0.0",
            "wheel>=0.31.0,<1.0.0",
            "setuptools>=38.6.0,<39.0.0"
        ],
        "demo": [
            "django-environ==0.4.5",
            "gunicorn==19.5.0",
            "whitenoise==3.1",
            "pip==9.0.1",
            "beautifulsoup4>=4.6.0,<5.0.0",
        ]
    },
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Framework :: Django :: 1.11',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3.5',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ]
)

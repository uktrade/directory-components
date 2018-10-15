"""
Export Directory API client
"""
import ast
import re
from setuptools import setup, find_packages


def get_version():
    pattern = re.compile(r'__version__\s+=\s+(.*)')

    with open('directory_components/version.py', 'rb') as src:
        return str(ast.literal_eval(
            pattern.search(src.read().decode('utf-8')).group(1)
        ))


setup(
    name='directory_components',
    version=get_version(),
    url='https://github.com/uktrade/directory-components',
    license='MIT',
    author='Department for International Trade',
    description='Shared components library for Export Directory.',
    packages=find_packages(exclude=["tests.*", "tests", "scripts", "demo.*"]),
    long_description=open('README.md').read(),
    include_package_data=True,
    install_requires=[
        'django>=1.9,<2.0a1',
        'export_elements>=0.21.0<=1.0.0',
        'beautifulsoup4>=4.6.0<5.0.0',
    ],
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

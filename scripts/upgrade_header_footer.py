"""Upgrade directory-components version in all repos that use it."""
import pathlib
import re
import os
from colors import color

__here__ = pathlib.Path(__file__).parent
project_root = __here__ / ".."


class Utils:
    """Class for vars used by the scripts."""

    dirs = [
        project_root / ".." / "directory-sso",
        project_root / ".." / "directory-sso-profile",
        project_root / ".." / "help",
        project_root / ".." / "directory-ui-buyer",
        project_root / ".." / "directory-ui-export-readiness",
        project_root / ".." / "navigator",
    ]

    req_files = [
        "requirements.txt",
        "requirements.in",
        "requirements_test.txt",
        "requirements_test.in",
    ]

    exp = r'(?:directory-components\.git@v)(\d*\.\d*\.\d)'
    get_version = r'\d*\.\d*\.\d'


def current_version():
    """Get current version of directory-components."""
    filepath = os.path.abspath(
        project_root / "directory_components" / "version.py")
    version_py = get_file_string(filepath)
    regex = re.compile(Utils.get_version)
    if regex.search(version_py) is not None:
        current_version = regex.search(version_py).group(0)
        print(color(
            "Current directory-components version: {}".format(current_version),
            fg='blue', style='bold'))
        get_update_info()
    else:
        print(color(
            'Error finding directory-components version.',
            fg='red', style='bold'))


def get_file_string(filepath):
    """Get string from file."""
    with open(os.path.abspath(filepath)) as f:
        return f.read()


def get_update_info():
    """Get update version from user input."""
    new_version = input(color("Version to upgrade to: ", fg='blue', style='bold'))
    replace_in_dirs(new_version)


def replace_in_dirs(version):
    """Look through dirs and run replace_in_files in each."""
    print(color(
        "Upgrading directory-components dependency in all repos...",
        fg='blue', style='bold'))
    for dirname in Utils.dirs:
        replace = "directory-components.git@v{}".format(version)
        replace_in_files(dirname, replace)
    done(version)


def replace_in_files(dirname, replace):
    """Replace current version with new version in requirements files."""
    for filename in Utils.req_files:
        filepath = os.path.abspath(dirname / filename)
        if os.path.isfile(filepath) and header_footer_exists(filepath):
            replaced = re.sub(Utils.exp, replace, get_file_string(filepath))
            with open(filepath, "w") as f:
                f.write(replaced)
            print(color(
                "Written to file: {}".format(filepath),
                fg='magenta', style='bold'))


def header_footer_exists(filepath):
    """Check if directory-components is listed in requirements files."""
    with open(filepath) as f:
        return re.search(Utils.exp, f.read())


def done(version):
    """When script is done show the version upgraded to."""
    print(color(
        "Upgraded to version {} !".format(version),
        fg='green', style='bold'))


if __name__ == '__main__':
    current_version()

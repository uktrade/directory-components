"""Upgrade directory-components version in all repos that use it."""
import pathlib
import re
import os

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


class Colours:
    """Terminal colours class."""

    str_bold = "\033[1m"
    str_magenta = "\033[95m"
    str_blue = "\033[34m"
    str_green = "\033[32m"
    str_red = "\033[91m"
    str_reset = "\033[0m"

    def magenta(text):
        """Make text bold and magenta."""
        return (
            Colours.str_bold + Colours.str_magenta + text + Colours.str_reset)

    def blue(text):
        """Make text bold and blue."""
        return Colours.str_bold + Colours.str_blue + text + Colours.str_reset

    def green(text):
        """Make text bold and green."""
        return Colours.str_bold + Colours.str_green + text + Colours.str_reset

    def red(text):
        """Make text bold and red."""
        return Colours.str_bold + Colours.str_red + text + Colours.str_reset


def current_version():
    """Get current version of directory-components."""
    filepath = os.path.abspath(
        project_root / "directory_components" / "version.py")
    version_py = get_file_string(filepath)
    regex = re.compile(Utils.get_version)
    if regex.search(version_py) is not None:
        current_version = regex.search(version_py).group(0)
        print_current_version = (
            "Current directory-components version: {}".format(current_version))
        print(Colours.blue(print_current_version))
        get_update_info()
    else:
        print(Colours.red("Error finding directory-components version."))


def get_file_string(filepath):
    """Get string from file."""
    with open(os.path.abspath(filepath)) as f:
        return f.read()


def get_update_info():
    """Get update version from user input."""
    new_version = input(Colours.blue("Version to upgrade to: "))
    replace_in_dirs(new_version)


def replace_in_dirs(version):
    """Look through dirs and run replace_in_files in each."""
    print(Colours.blue(
        "Upgrading directory-components dependency in all repos..."))
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
            print(Colours.magenta("Written to file: {}".format(filepath)))


def header_footer_exists(filepath):
    """Check if directory-components is listed in requirements files."""
    with open(filepath) as f:
        return re.search(Utils.exp, f.read())


def done(version):
    """When script is done show the version upgraded to."""
    print(Colours.green("Upgraded to version {} !".format(version)))


if __name__ == '__main__':
    current_version()

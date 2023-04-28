from package_name.util import find_package_location, find_repo_location
from package_name import __project__, __version__


def test_version():
    assert __version__


def test_project():
    assert __project__


def test_find_package_location():
    assert find_package_location()


def test_find_repo_location():
    assert find_repo_location()

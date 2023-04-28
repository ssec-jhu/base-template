import importlib
import os

from . import __project__  # Keep as relative for templating reasons.


def find_package_location(package=__project__):
    return importlib.util.find_spec(package).submodule_search_locations[0]


def find_repo_location(package=__project__):
    return os.path.abspath(os.path.join(find_package_location(package), os.pardir))

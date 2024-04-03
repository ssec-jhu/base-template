"""Helps setup a new project based on this template."""
import argparse
import functools
import os
from pathlib import Path
from typing import Callable, List, Tuple

# this is GitPython
import git

TEMPLATE_PACKAGE_NAME = "package_name"
TEMPLATE_REPO_URL = "https://github.com/ssec-jhu/base-template"
TEMPLATE_RTD = "ssec-jhu-base-template"
TEMPLATE_CODECOV = "ssec-jhu/base-template"

UPDATED_PYPROJECT_TOML = "pyproject.toml [project.urls]"
UPDATED_README = "Updated README.md"
UPDATED_FILE = "Updated package_name to {package_name} in {file_path} ✅"
SETUP_COMPLETE = "{package_name} setup complete! 🎉🎉🎉\n"

def make_name_safe(name:str) -> str:
    """Makes a string safe to use as a package name."""
    return name.lower().replace(' ', '_').replace('-', '_')


def valid_file_predicate(file_path:Path) -> bool:
    """Checks if a file is valid for modification."""
    is_valid_extension = file_path.suffix not in [
        # images
        ".png",
        ".jpg",
        ".jpeg",
    ]
    not_ds_store = file_path.name != ".DS_Store"
    not_this = file_path.name != Path(__file__).name

    return is_valid_extension and not_ds_store and not_this


def get_package_name(
    repo_url:str,
) -> str:
    """Guesses the package name from the repo URL."""
    return make_name_safe(Path(repo_url).stem)


def replace_file_contents(
    pairs_to_replace:List[Tuple[str, str]],
    file_path:Path,
) -> bool:
    """Replaces the contents of a file.

    pairs_to_replace (List[Tuple[str, str]]): A list of tuples where the first
        element is the string to replace and the second element is the new string
    file_path (Path): The path to the file to modify

    Returns:
        bool: True if the file was modified, False otherwise
    """
    with open(file_path, "r") as f:
        content = f.read()

    new_content = functools.reduce(lambda x, y: x.replace(*y), pairs_to_replace, content)

    if new_content != content:
        with open(file_path, "w") as f:
            f.write(new_content)
        return True

    return False


def self_destruct() -> None:
    """Deletes this file and its tests."""
    os.remove(__file__)
    os.remove("tests/test_project_setup.py")


def rtd_project_guess(
    repo_url:str,
) -> str:
    """Guesses the RTD project name from the repo URL."""
    return Path(repo_url).stem


def codecov_project_guess(
    repo_url:str,
) -> str:
    """Guesses the codecov project name from the repo URL."""
    return "/".join(Path(repo_url).parts[-2:]).replace(".git", "")


def run_setup(
    repo_url:str,
    package_name:str,
    dir_path:Path = Path("."),
    output_func:Callable[[str], None] = print,
) -> None:

    # Update pyproject.toml and README.md, which contain the repo URL===========
    rtd_guess = rtd_project_guess(repo_url)
    codecov_guess = codecov_project_guess(repo_url)

    pyproject_toml_replacement_pairs = [
        (TEMPLATE_REPO_URL, repo_url),
    ]
    if replace_file_contents(
        pyproject_toml_replacement_pairs,
        dir_path / Path("pyproject.toml"),
    ):
        output_func(UPDATED_PYPROJECT_TOML + "✅")

    readme_replacement_pairs = [
        (TEMPLATE_REPO_URL, repo_url),
        (TEMPLATE_RTD, rtd_guess),
        (TEMPLATE_CODECOV, codecov_guess),
    ]
    if replace_file_contents(
        readme_replacement_pairs,
        dir_path / Path("README.md"),
    ):
        output_func(UPDATED_README + "✅")


    # Update occurences of the package name in the project======================
    # Sometimes the template package name is referred to using `package_name`
    # and other times it is referred to by `<package_name>`. First replace the
    # brackted version becaused replacing the unbracketed version will also
    # replace the bracketed version, but not vice versa.

    # use git to move to preserve the git history
    git.Repo().git.mv(TEMPLATE_PACKAGE_NAME, package_name)

    # filter out files that we don't want to modify
    files_to_check = list(filter(
        valid_file_predicate,
        map(Path, git.Repo().git.ls_tree("-r", "--name-only", "HEAD").split("\n")),
    ))

    # order matters, replace the bracketed version first
    package_name_replacement_pairs = [
        ("<" + TEMPLATE_PACKAGE_NAME + ">", package_name),
        (TEMPLATE_PACKAGE_NAME, package_name),
    ]
    for file_path in files_to_check:
        # only print positive results
        if replace_file_contents(package_name_replacement_pairs, file_path):
            output_func(UPDATED_FILE.format(package_name=package_name, file_path=file_path))

    # self_destruct()

    output_func(SETUP_COMPLETE.format(package_name=package_name))


if __name__ == '__main__':
    arguments = argparse.ArgumentParser()
    arguments.add_argument("--repo_url", type=str, default="")
    arguments.add_argument("--package_name", type=str, default="")
    arguments.parse_args()

    repo_url = arguments.repo_url or git.Repo().remotes.origin.url
    package_name = arguments.package_name or get_package_name(repo_url)
    run_setup(
        repo_url=repo_url,
        package_name=package_name
    )

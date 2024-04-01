# BSD 3-Clause License

# Copyright (c) 2024, Scientific Software Engineering Center at JHU

# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:

# 1. Redistributions of source code must retain the above copyright notice, this
#    list of conditions and the following disclaimer.

# 2. Redistributions in binary form must reproduce the above copyright notice,
#    this list of conditions and the following disclaimer in the documentation
#    and/or other materials provided with the distribution.

# 3. Neither the name of the copyright holder nor the names of its
#    contributors may be used to endorse or promote products derived from
#    this software without specific prior written permission.

# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
# FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
# DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
# SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
# OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

"""Helps setup a new project based on this template."""

import configparser
import functools
import itertools
import os
from typing import Callable, Iterable, Optional

MSG_GIT_URL_NOT_FOUND = "--Remote URL not found in .git/config--"
PROMPT_REMOTE_REPO = "Enter the URL of the remote repository [{url_guess}]: "
PROMPT_PKG_NAME = "Enter the package name [{name_guess}]: "

def make_name_safe(name:str) -> str:
    """Makes a string safe to use as a package name.

    Args:
        name (str): The string to make safe.

    Returns:
        str: The safe string.

    """
    return name.lower().replace(' ', '_').replace('-', '_')


def valid_file_predicate(file_path:str) -> bool:
    """Checks if a file is valid for modification.

    Args:
        file_path (str): The path to the file to check.

    Returns:
        bool: Whether the file is valid for modification.

    """
    not_in_git = not file_path.startswith("./.git/")
    not_image =  (
        not file_path.endswith(".png")
        and not file_path.endswith(".jpg")
        and not file_path.endswith(".jpeg")
    )
    not_binary = not file_path.endswith(".DS_Store")
    not_this = not file_path.endswith("project_setup.py")

    return not_in_git and not_image and not_binary and not_this


def get_repo_url(
    file_contents:Iterable[str],
    input_func:Callable[[Optional[str]], str] = input
) -> str:
    """Gets the URL of the remote repository.

    Args:
        file_contents (Iterable[str]): The contents of the .git/config file.
        input_func (Callable[[Optional[str]], str], optional): The input function to use. Defaults to input.

    Returns:
        str: The URL of the remote repository.

    """
    # cp.read("./.git/config")
    cp = configparser.ConfigParser()
    try:
        cp.read_file(file_contents)
    except configparser.MissingSectionHeaderError:
        url_guess = MSG_GIT_URL_NOT_FOUND

    try:
        url_guess = cp['remote "origin"']["url"]
    except KeyError:
        url_guess = MSG_GIT_URL_NOT_FOUND

    # this could be a problem if someone accidentally hits enter and the URL is
    # is set to MSG_GIT_URL_NOT_FOUND. Maybe change to a while loop if this
    # becomes an issue.
    repo_url = input_func(PROMPT_REMOTE_REPO.format(url_guess=url_guess)).strip()

    return repo_url or url_guess


def get_package_name(
    repo_url:str,
    input_func:Callable[[Optional[str]], str] = input
) -> str:
    """Gets the package name from the user.

    Guesses the package name from the repo URL.

    Args:
        repo_url (str): The URL of the remote repository.
        input_func (Callable[[Optional[str]], str], optional): The input function to use. Defaults to input.

    Returns:
        str: The package name.
    """
    repo_name = os.path.basename(repo_url).split('/')[-1].split('.')[0]
    guessed_name = make_name_safe(repo_name)

    input_name = input_func(PROMPT_PKG_NAME.format(name_guess=guessed_name)).strip()

    return input_name or guessed_name


def replace_file_contents(
    new_str:str,
    old_str:str,
    file_path:str,
) -> bool:
    """Replaces instances of `old_str` with `new_str` in file at file_path.

    Args:
        old_str (str): The string to replace.
        new_str (str): The string to replace `old_str` with.
        file_path (str): The path to the file to modify.

    Returns:
        None
    """
    with open(file_path, "r") as f:
        content = f.read()

    new_content = content.replace(old_str, new_str)

    if new_content != content:
        with open(file_path, "w") as f:
            f.write(new_content)
        return True

    return False


def self_destruct(input_func:Callable[[str], str] = input) -> None:
    """Deletes this file."""

    if input_func("Delete this file? [y/N]: ").strip().lower() == "y":
        os.remove(__file__)


def replace_package_name(new_package_name:str) -> None:
    """Replaces the package name in all files in the repo.

    Args:
        new_package_name (str): The new package name.

    Returns:
        None
    """
    old_package_name = "package_name"
    replace_func = functools.partial(
        replace_file_contents,
        new_package_name,
        old_package_name,
    )

    replace_func_brackets = functools.partial(
        replace_file_contents,
        new_package_name,
        "<" + old_package_name + ">",
    )

    #change project_dir
    os.rename(old_package_name, new_package_name)

    # get all files with paths in the repo directory
    dir_file_pairs = itertools.chain.from_iterable(map(
        lambda walk_tup: zip(itertools.repeat(walk_tup[0]), walk_tup[2]),
        os.walk(".")
    ))
    files_to_check = list(filter(
        valid_file_predicate,
        map(lambda x: os.path.join(*x), dir_file_pairs)
    ))

    # replace the package name in all files
    print(f"Replacing `<{old_package_name}>` with `{new_package_name}` in all files...")
    for _ in map(replace_func_brackets, files_to_check):
        pass
    print()

    print(f"Replacing `{old_package_name}` with `{new_package_name}` in all files...")
    for _ in map(replace_func, files_to_check):
        pass
    print()


def update_url_references(repo_url:str) -> None:
    """Updates the URL references in the repository.

    Updates URLs in the README.md and pyproject.toml files.

    Args:
        repo_url (str): The URL of the remote repository.

    Returns:
        None

    """
    base_url = "https://github.com/ssec-jhu/base-template"
    repo_url = repo_url.replace(".git", "")
    rtd_project_guess = repo_url.split('/')[-1]
    codecov_project_guess = "/".join(repo_url.split('/')[-2:])

    replace_file_contents(repo_url, base_url, "./README.md", True)
    print("Updated README.md -> CI/Security badges ✅")

    replace_file_contents(rtd_project_guess, "ssec-jhu-base-template", "./README.md", False)
    print("Updated README.md -> RTD badge ✅")

    replace_file_contents(codecov_project_guess, "ssec-jhu/base-template", "./README.md", False)
    print("Updated README.md -> codecov badge ✅")

    replace_file_contents(repo_url, base_url, "pyproject.toml", False)
    print("Updated pyproject.toml [project.urls] ✅\n")


def main():
    repo_url = get_repo_url()
    update_url_references(repo_url)

    package_name = get_package_name(repo_url)
    replace_package_name(package_name)

    self_destruct()

    print(f"{package_name} setup complete! 🎉🎉🎉\n")


if __name__ == '__main__':
    main()
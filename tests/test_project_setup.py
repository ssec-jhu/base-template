import os
from pathlib import Path
import shutil
from typing import Iterable, List, Tuple

import pytest

import project_setup as ps

@pytest.mark.parametrize("name, expected", [
    ("My Project", "my_project"),
    ("My-Project", "my_project"),
    ("My_Project", "my_project"),
    ("My_Pro-ject", "my_pro_ject"),
    ("my_project", "my_project"),
    ("", "")
])
def test_make_name_safe(name:str, expected:str):
    assert ps.make_name_safe(name) == expected


@pytest.mark.parametrize("file_path, expected", [
    (Path("test.png"), False),
    (Path("test.jpg"), False),
    (Path("test.jpeg"), False),
    (Path(".DS_Store"), False),
    (Path("project_setup.py"), False),
    (Path("great_idea.py"), True),
    (Path("science.txt"), True),
    (Path("new_ideas.md"), True),
])
def test_valid_file_predicate(file_path:Path, expected:bool):
    assert ps.valid_file_predicate(file_path) == expected


@pytest.mark.parametrize(
    "repo_url, expected_output", [
    (
        "https://github.com/example/good-idea.git",
        "good_idea",
    ),
    (
        "https://github.com/example/bet-ter-id_ea.git",
        "bet_ter_id_ea",
    ),
])
def test_get_package_name(
    repo_url:str,
    expected_output:str,
):
    assert ps.get_package_name(repo_url)==expected_output


@pytest.mark.parametrize(
    "file_contents, replacement_tuple, expected", [
        # old texts exists and is replaced
        (
            "This is a file\nwith old_text\nand more text\n",
            [("old_text", "new_text")],
            True,
        ),
        # old text does not exist
        (
            "This is a file\nwith some text\nand more text\n",
            [("old_text", "new_text")],
            False
        ),
    ]
)
def test_replace_file_contents(
    file_contents:str,
    replacement_tuple:List[Tuple[str, str]],
    expected:bool,
):
    with open("tmp.txt", "w") as f:
        f.write(file_contents)

    actual_file_changed = ps.replace_file_contents(replacement_tuple, "tmp.txt")

    with open("tmp.txt", "r") as f:
        actual_contents = f.read()

    old_str, new_str = replacement_tuple[0]
    old_not_there = old_str not in actual_contents
    new_there = new_str in actual_contents

    os.remove("tmp.txt")

    assert actual_file_changed == expected
    if expected:
        assert expected and old_not_there
        assert expected and new_there
    else:
        assert old_str not in file_contents
        assert file_contents == actual_contents


def test_self_destruct():
    with open("project_setup.py", "r") as f:
        ps_contents = f.read()

    with open("tests/test_project_setup.py", "r") as f:
        test_ps_contents = f.read()

    ps.self_destruct()

    ps_exists = os.path.exists("project_setup.py")
    ps_test_exists = os.path.exists("tests/test_project_setup.py")

    with open("project_setup.py", "w") as f:
        f.write(ps_contents)

    with open("tests/test_project_setup.py", "w") as f:
        f.write(test_ps_contents)

    assert not ps_exists
    assert not ps_test_exists


@pytest.mark.parametrize(
    "repo_url, expected", [
        ("https://www.github.com/amazing-org/really-great-project.git", "really-great-project"),
    ]
)
def test_rtd_project_guess(repo_url:str, expected:str):
    assert ps.rtd_project_guess(repo_url) == expected


@pytest.mark.parametrize(
    "repo_url, expected", [
        ("https://www.github.com/amazing-org/really-great-project.git", "amazing-org/really-great-project"),
    ]
)
def test_codecov_project_guess(repo_url:str, expected:str):
    assert ps.codecov_project_guess(repo_url) == expected


# @pytest.mark.parametrize(
#     "repo_url, package_name", [
#     ("https://www.github.com/good-org/amazing-project.git", "amazing_project"),
# ])
# def test_run_setup(repo_url:str, package_name:str):
#     base_dir = "tests/tmp"
#     def with_base(f:str):
#         return os.path.join(base_dir, f)
#     # setup a mock repo structure
#     os.makedirs(with_base("package_name"), exist_ok=True)
#     os.makedirs(with_base(".git"), exist_ok=True)

#     mock_pyproject = "\n".join([
#         "[project]",
#         'name = "package_name"',
#         "",
#         '[project.urls]',
#         'homepage = "https://github.com/ssec-jhu/base-template"',
#         'documentation = "https://github.com/ssec-jhu/base-template"',
#         'repository = "https://github.com/ssec-jhu/base-template"',
#         "",
#     ])

#     with open(with_base("pyproject.toml"), "w") as f:
#         f.write(mock_pyproject)


#     mock_git_config = "\n".join([
#         '[remote "origin"]',
#         '    url = https://github.com/ssec-jhu/base-template.git',
#         '    fetch = +refs/heads/*:refs/remotes/origin/*',
#     ])

#     with open(with_base(".git/config"), "w") as f:
#         f.write(mock_git_config)

#     mock_readme = "\n".join([
#         "# SSEC-JHU <package_name>",
#         "",
#         "[![CI](https://github.com/ssec-jhu/base-template/actions/workflows/ci.yml/badge.svg)](https://github.com/ssec-jhu/base-template/actions/workflows/ci.yml)",
#         "[![Documentation Status](https://readthedocs.org/projects/ssec-jhu-base-template/badge/?version=latest)](https://ssec-jhu-base-template.readthedocs.io/en/latest/?badge=latest)",
#         "[![codecov](https://codecov.io/gh/ssec-jhu/base-template/branch/main/graph/badge.svg?token=0KPNKHRC2V)](https://codecov.io/gh/ssec-jhu/base-template)",
#         "[![Security](https://github.com/ssec-jhu/base-template/actions/workflows/security.yml/badge.svg)](https://github.com/ssec-jhu/base-template/actions/workflows/security.yml)",
#         "",
#         "This is a package_name kind of thing.",
#     ])

#     with open(with_base("README.md"), "w") as f:
#         f.write(mock_readme)

#     # a file with a change
#     file_with_change = "\n".join([
#         "import os",
#         "",
#         "package_name.app.main()",
#     ])
#     with open(with_base("package_name/app.py"), "w") as f:
#         f.write(file_with_change)


#     # a file without a change
#     file_without_change = "\n".join([
#         "import numpy as np",
#         "",
#         "np.arange(100)",

#     ])
#     with open(with_base("package_name/other.py"), "w") as f:
#         f.write(file_without_change)


#     input_func = InputMock(prompt_replies=[""])
#     outputs = []
#     def output_func(x:str) -> None:
#         outputs.append(x)


#     ps.run_setup(repo_url, package_name, base_dir, input_func, output_func)


#     template_package_name = "package_name"
#     template_url = "https://github.com/ssec-jhu/base-template"

#     # open pyproject.toml
#     with open(with_base("pyproject.toml"), "r") as f:
#         actual_pyproject = f.read()

#     # open README.md
#     with open(with_base("README.md"), "r") as f:
#         actual_readme = f.read()

#     # open package_name/app.py
#     with open(with_base(f"{package_name}/app.py"), "r") as f:
#         actual_app = f.read()

#     # open package_name/other.py
#     with open(with_base(f"{package_name}/other.py"), "r") as f:
#         actual_other = f.read()

#     # clean up the dir, just in case the test fails
#     shutil.rmtree(base_dir)

#     # check pyproject.toml
#     assert template_url not in actual_pyproject
#     assert template_package_name not in actual_pyproject
#     assert package_name in actual_pyproject
#     assert repo_url in actual_pyproject

#     # check README.md
#     assert template_url not in actual_readme
#     assert template_package_name not in actual_readme
#     assert package_name in actual_readme
#     assert repo_url in actual_readme
#     assert ps.codecov_project_guess(repo_url) in actual_readme
#     assert ps.rtd_project_guess(repo_url) in actual_readme

#     # check the app.py
#     assert template_package_name not in actual_app
#     assert package_name in actual_app

#     # check the other.py
#     assert template_package_name not in actual_other
#     assert package_name not in actual_other


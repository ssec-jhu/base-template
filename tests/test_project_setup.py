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

import os
import shutil
from typing import Iterable, List

import pytest

import project_setup as ps

class InputMock:
    def __init__(self, prompt_replies:List[str]=[""]):
        self.prompt_replies = prompt_replies
        self.inputs = []


    def __call__(self, prompt:str) -> str:
        self.inputs.append(prompt)
        return self.prompt_replies.pop(0)

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
    ("./.git/", False),
    ("test.png", False),
    ("test.jpg", False),
    ("test.jpeg", False),
    (".DS_Store", False),
    ("project_setup.py", False),
    ("great_idea.py", True),
    ("science.txt", True),
    ("new_ideas.md", True),
])
def test_valid_file_predicate(file_path:str, expected:bool):
    assert ps.valid_file_predicate(file_path) == expected


@pytest.mark.parametrize(
    "file_contents, prompt_reply, expected_prompt, expected_output", [
    # remote exists, user overrides
    (
        [
            '[remote "origin"]',
            "	url = https://github.com/ssec-jhu/base-template.git",
        ],
        "https://github.com/example/good-idea.git",
        ps.PROMPT_REMOTE_REPO.format(url_guess="https://github.com/ssec-jhu/base-template.git"),
        "https://github.com/example/good-idea.git",
    ),
    # remote exists, user accepts
    (
        [
            '[remote "origin"]',
            "	url = https://github.com/ssec-jhu/base-template.git",
        ],
        "",
        ps.PROMPT_REMOTE_REPO.format(url_guess="https://github.com/ssec-jhu/base-template.git"),
        "https://github.com/ssec-jhu/base-template.git",
    ),
    # config isn't parseable, prompt with error message, user accepts
    (
        ["won't parse"],
        "",
        ps.PROMPT_REMOTE_REPO.format(url_guess=ps.MSG_GIT_URL_NOT_FOUND),
        ps.MSG_GIT_URL_NOT_FOUND,
    ),
    # no remote url, prompt with error message, user accepts
    (
        [
            '[remote "origin"]',
            "	error-url = https://github.com/ssec-jhu/base-template.git",
        ],
        "",
        ps.PROMPT_REMOTE_REPO.format(url_guess=ps.MSG_GIT_URL_NOT_FOUND),
        ps.MSG_GIT_URL_NOT_FOUND,
    ),
])
def test_get_repo_url(
    file_contents:Iterable[str],
    prompt_reply:str,
    expected_prompt:str,
    expected_output:str,
):
    input_func = InputMock(prompt_replies=[prompt_reply])
    assert ps.get_repo_url(file_contents, input_func) == expected_output
    assert input_func.inputs == [expected_prompt]


@pytest.mark.parametrize(
    "repo_url, prompt_reply, expected_prompt, expected_output", [
    # user accepts
    (
        "https://github.com/example/good-idea.git",
        "",
        ps.PROMPT_PKG_NAME.format(name_guess="good_idea"),
        "good_idea",
    ),
    # user overrides
    (
        "https://github.com/example/good-idea.git",
        "better_idea",
        ps.PROMPT_PKG_NAME.format(name_guess="good_idea"),
        "better_idea",
    ),
])
def test_get_package_name(
    repo_url:str,
    prompt_reply:str,
    expected_prompt:str,
    expected_output:str,
):
    input_func = InputMock(prompt_replies=[prompt_reply])
    assert ps.get_package_name(repo_url, input_func)==expected_output
    assert input_func.inputs == [expected_prompt]


@pytest.mark.parametrize(
    "file_contents, new_string, old_string, expected", [
        # old texts exists and is replaced
        (
            "This is a file\nwith old_text\nand more text\n",
            "new_text",
            "old_text",
            True
        ),
        # old text does not exist
        (
            "This is a file\nwith some text\nand more text\n",
            "new_text",
            "no_text",
            False
        ),
    ]
)
def test_replace_file_contents(
    file_contents:str,
    new_string:str,
    old_string:str,
    expected:bool,
):
    with open("tmp.txt", "w") as f:
        f.write(file_contents)

    actual_file_changed = ps.replace_file_contents(new_string, old_string, "tmp.txt")

    with open("tmp.txt", "r") as f:
        actual_contents = f.read()

    old_not_there = old_string not in actual_contents
    new_there = new_string in actual_contents

    os.remove("tmp.txt")

    assert actual_file_changed == expected
    if expected:
        assert expected and old_not_there
        assert expected and new_there
    else:
        assert old_string not in file_contents
        assert file_contents == actual_contents


@pytest.mark.parametrize(
    "input_reply, file_removed", [
        ("y", True),
        ("Y", True),
        ("n", False),
        ("N", False),
        ("", False),
    ]
)
def test_self_destruct(input_reply:str, file_removed:bool):
    with open("project_setup.py", "r") as f:
        ps_contents = f.read()

    input_func = InputMock(prompt_replies=[input_reply])
    ps.self_destruct(input_func)

    file_exists = os.path.exists("project_setup.py")

    with open("project_setup.py", "w") as f:
        f.write(ps_contents)

    if file_removed:
        assert not file_exists
    else:
        assert file_exists

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


@pytest.mark.parametrize(
    "repo_url, package_name", [
    ("https://www.github.com/good-org/amazing-project.git", "amazing_project"),
])
def test_run_setup(repo_url:str, package_name:str):
    base_dir = "tests/tmp"
    def with_base(f:str):
        return os.path.join(base_dir, f)
    # setup a mock repo structure
    os.makedirs(with_base("package_name"), exist_ok=True)
    os.makedirs(with_base(".git"), exist_ok=True)

    mock_pyproject = "\n".join([
        "[project]",
        'name = "package_name"',
        "",
        '[project.urls]',
        'homepage = "https://github.com/ssec-jhu/base-template"',
        'documentation = "https://github.com/ssec-jhu/base-template"',
        'repository = "https://github.com/ssec-jhu/base-template"',
        "",
    ])

    with open(with_base("pyproject.toml"), "w") as f:
        f.write(mock_pyproject)


    mock_git_config = "\n".join([
        '[remote "origin"]',
        '    url = https://github.com/ssec-jhu/base-template.git',
        '    fetch = +refs/heads/*:refs/remotes/origin/*',
    ])

    with open(with_base(".git/config"), "w") as f:
        f.write(mock_git_config)

    mock_readme = "\n".join([
        "# SSEC-JHU <package_name>",
        "",
        "[![CI](https://github.com/ssec-jhu/base-template/actions/workflows/ci.yml/badge.svg)](https://github.com/ssec-jhu/base-template/actions/workflows/ci.yml)",
        "[![Documentation Status](https://readthedocs.org/projects/ssec-jhu-base-template/badge/?version=latest)](https://ssec-jhu-base-template.readthedocs.io/en/latest/?badge=latest)",
        "[![codecov](https://codecov.io/gh/ssec-jhu/base-template/branch/main/graph/badge.svg?token=0KPNKHRC2V)](https://codecov.io/gh/ssec-jhu/base-template)",
        "[![Security](https://github.com/ssec-jhu/base-template/actions/workflows/security.yml/badge.svg)](https://github.com/ssec-jhu/base-template/actions/workflows/security.yml)",
        "",
        "This is a package_name kind of thing.",
    ])

    with open(with_base("README.md"), "w") as f:
        f.write(mock_readme)

    # a file with a change
    file_with_change = "\n".join([
        "import os",
        "",
        "package_name.app.main()",
    ])
    with open(with_base("package_name/app.py"), "w") as f:
        f.write(file_with_change)


    # a file without a change
    file_without_change = "\n".join([
        "import numpy as np",
        "",
        "np.arange(100)",

    ])
    with open(with_base("package_name/other.py"), "w") as f:
        f.write(file_without_change)


    input_func = InputMock(prompt_replies=[""])
    outputs = []
    def output_func(x:str) -> None:
        outputs.append(x)


    ps.run_setup(repo_url, package_name, base_dir, input_func, output_func)


    template_package_name = "package_name"
    template_url = "https://github.com/ssec-jhu/base-template"

    # open pyproject.toml
    with open(with_base("pyproject.toml"), "r") as f:
        actual_pyproject = f.read()

    # open README.md
    with open(with_base("README.md"), "r") as f:
        actual_readme = f.read()

    # open package_name/app.py
    with open(with_base(f"{package_name}/app.py"), "r") as f:
        actual_app = f.read()

    # open package_name/other.py
    with open(with_base(f"{package_name}/other.py"), "r") as f:
        actual_other = f.read()

    # clean up the dir, just in case the test fails
    shutil.rmtree(base_dir)

    # check pyproject.toml
    assert template_url not in actual_pyproject
    assert template_package_name not in actual_pyproject
    assert package_name in actual_pyproject
    assert repo_url in actual_pyproject

    # check README.md
    assert template_url not in actual_readme
    assert template_package_name not in actual_readme
    assert package_name in actual_readme
    assert repo_url in actual_readme
    assert ps.codecov_project_guess(repo_url) in actual_readme
    assert ps.rtd_project_guess(repo_url) in actual_readme

    # check the app.py
    assert template_package_name not in actual_app
    assert package_name in actual_app

    # check the other.py
    assert template_package_name not in actual_other
    assert package_name not in actual_other


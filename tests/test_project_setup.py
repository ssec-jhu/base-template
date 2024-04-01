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
from typing import Iterable

import pytest

import project_setup as ps

class InputMock:
    def __init__(self, prompt_reply:str=""):
        self.prompt_reply = prompt_reply
        self.inputs = []


    def __call__(self, prompt:str) -> str:
        self.inputs.append(prompt)
        return self.prompt_reply

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
    input_func = InputMock(prompt_reply=prompt_reply)
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
    input_func = InputMock(prompt_reply=prompt_reply)
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

    input_func = InputMock(prompt_reply=input_reply)
    ps.self_destruct(input_func)

    file_exists = os.path.exists("project_setup.py")

    with open("project_setup.py", "w") as f:
        f.write(ps_contents)

    if file_removed:
        assert not file_exists
    else:
        assert file_exists
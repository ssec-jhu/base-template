# SSEC-JHU <package_name>

[![CI](https://github.com/ssec-jhu/base-template/actions/workflows/ci.yml/badge.svg)](https://github.com/ssec-jhu/base-template/actions/workflows/ci.yml)
[![Documentation Status](https://readthedocs.org/projects/ssec-jhu-base-template/badge/?version=latest)](https://ssec-jhu-base-template.readthedocs.io/en/latest/?badge=latest)
[![codecov](https://codecov.io/gh/ssec-jhu/base-template/branch/main/graph/badge.svg?token=0KPNKHRC2V)](https://codecov.io/gh/ssec-jhu/base-template)
[![Security](https://github.com/ssec-jhu/base-template/actions/workflows/security.yml/badge.svg)](https://github.com/ssec-jhu/base-template/actions/workflows/security.yml)
[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.14052740.svg)](https://doi.org/10.5281/zenodo.14052740)


![SSEC-JHU Logo](docs/_static/SSEC_logo_horiz_blue_1152x263.png)

Base repo template to be used by all others.

Things to do when using this template:

 * Run ```make setup```
 * Uncomment above DOI in README.md and correct ``<insert_ID_number>``.
 * Correct "description" field in .zenodo.json to reflect description of child repo.
 * Correct the ``CI Status`` badge with the correct token in the URL.
 * Import package into https://readthedocs.org/.
 * Update [zenodo.json](zenodo.json). For more details see [zenodo.json docs](https://developers.zenodo.org/#representation) and [zenodo docs on contributors vs creators](https://help.zenodo.org/docs/deposit/describe-records/contributors/).
 * Update quickstart guide below.

What's included in this template:

 * Licence file
 * Code of Conduct
 * Build & Setup, using `uv`.
 * Dependabot GitHub action
 * CI for GitHub actions: lint, pytest, build & publish docker image to GitHub Packages.
 * Dockerfile.
 * Pytest example(s).
 * Githooks.

# Quickstart Guide

Add here, streamlined instructions on how to get the code running as swiftly as possible, and provide usage example(s).
This shouldn't attempt to cover all OS's and/or build variations - just the canonical. Since users are most likely
viewing this README from GitHub.com, assuming a repo context might be best, where instructions look like those below.
Alternatively, if this package is distributed on PyPi, perhaps just ``pip install <package-name>``, followed by quick
user instructions, will suffice.

  * ``git clone https://github.com/ssec-jhu/base-template``
  * ``conda create -n package_name python pip``
  * ``conda activate package_name``
  * ``pip install -e .``
  * Add user instructions.

# Installation, Build, & Run instructions

### uv:

Dependencies various environments (docs, building, testing) for the base
template area managed via [uv](https://docs.astral.sh/uv/). If you don't have
`uv` installed already, follow the [installation
instructions](https://github.com/astral-sh/uv?tab=readme-ov-file#installation).

Once `uv` is installed, you can set up your environment by running:

```bash
uv sync
```

This will create a new python virtual environment and install all the
current dependencies. To add a dependency, run:

```bash
uv add <package_name>
```

To remove a dependency, run:

```bash
uv remove <package_name>
```

To update a package, run:

```bash
uv lock --upgrade-package <package_name>
```

See the `uv` [documentation](https://docs.astral.sh/uv/guides/projects/#managing-dependencies) for more details on managing dependencies.

> [!CAUTION]
> If you do not use `uv` to manage the dependencies, your package will
> likely fail the CI/CD tests and builds.


### Build:

  #### with Docker:
  * Download & install Docker - see [Docker install docs](https://docs.docker.com/get-docker/).
  * ``cd`` into repo dir.
  * Build image: ``docker build -t <image_name> .``

  #### with Python ecosystem:

  ```bash
  make dist
  ```

### Run

  #### with Docker:
  * Follow the above [Build with Docker instructions](#with-docker).
  * Run container from image: ``docker run -d -p 8000:8000 <image_name>``. _NOTE: ``-p 8000:8000`` is specific to the example application using port 8000._
  * Alternatively, images can be pulled from ``ghcr.io/ssec-jhu/`` e.g., ``docker pull ghcr.io/ssec-jhu/base-template:pr-1``.

  #### with Python ecosystem:
  * Follow the above [Build with Python ecosystem instructions](#with-python-ecosystem).
  * Run ``uv run uvicorn package_name.app.main:app --host 0.0.0.0 --port 8000``.
    _NOTE: This is just an example and is obviously application dependent._

### Usage:
To be completed by child repo.


# Testing

Run

```bash
make test
```


The CI tests run in github actions will use `uv` to run as above. See also
[ci.yml](https://github.com/ssec-jhu/base-template/blob/main/.github/workflows/ci.yml).

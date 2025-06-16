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
 * Uncomment the above DOI in README.md and correct ``<insert_ID_number>``.
 * Correct the "description" field in .zenodo.json to reflect the description of the child repo.
 * Correct the ``CI Status`` badge with the correct token in the URL.
 * Import package into https://readthedocs.org/.
 * Update [zenodo.json](zenodo.json). For more details see [zenodo.json docs](https://developers.zenodo.org/#representation) and [zenodo docs on contributors vs creators](https://help.zenodo.org/docs/deposit/describe-records/contributors/).
 * Update the quickstart guide below.

What's included in this template:

 * License file
 * Code of Conduct
 * Build & Setup, using `uv`.
 * Dependabot GitHub action
 * CI for GitHub actions: lint, tests, build & publish docker image to GitHub Packages.
 * Dockerfile.
 * Pytest example(s).
 * Githooks.

# Quickstart Guide

Add here streamlined instructions on how to get the code running as swiftly as possible and provide usage example(s).
This shouldn't attempt to cover all OS's and/or build variations - just the canonical. Since users are most likely
viewing this README from GitHub.com, assuming a repo context might be best, where instructions look like those below.
Alternatively, if this package is distributed on PyPI, perhaps just ``pip install <package-name>``, followed by quick
user instructions, will suffice.

  * ``git clone https://github.com/ssec-jhu/base-template``
  * ``conda create -n package_name python pip``
  * ``conda activate package_name``
  * ``pip install -e .``
  * Add user instructions.

# Build, Installation, and Run instructions

package_name uses [uv](https://docs.astral.sh/uv/) as an environment manager
for common tasks such as building, running, and testing the package. If you don't have
`uv` installed already, follow the [installation
instructions](https://github.com/astral-sh/uv?tab=readme-ov-file#installation).


### Build:

  #### with Docker:
  * Download & install Docker - see [Docker install docs](https://docs.docker.com/get-docker/).
  * ``cd`` into repo dir.
  * Build image: ``docker build -t <image_name> .``

  #### with Python ecosystem:
  * Run ``make dist``, this will create a ``dist/`` directory with the built package.
  * You can install the package using pip:
    ```bash
    pip install dist/<package_name>-<version>.tar.gz
    ````

### Run

  #### with Docker:
  * Follow the above [Build with Docker instructions](#with-docker).
  * Run container from image: ``docker run -d -p 8000:8000 <image_name>``. _NOTE: ``-p 8000:8000`` is specific to the example application using port 8000._
  * Alternatively, images can be pulled from ``ghcr.io/ssec-jhu/`` e.g., ``docker pull ghcr.io/ssec-jhu/base-template:pr-1``.

  #### with Python ecosystem:
  * Follow the above [Build with Python ecosystem instructions](#with-python-ecosystem).
  * Run ``uvicorn package_name.app.main:app --host 0.0.0.0 --port 8000``.
    _NOTE: This is just an example and is obviously application dependent._

### Usage:
To be completed by child repo.

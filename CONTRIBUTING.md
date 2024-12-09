# Contributing to package_name

Thank you for your interest in contributing to package_name! As a contributor, you’ll work from your fork of the main repository. This document outlines the steps to set up your development environment, guidelines for coding, and instructions for submitting contributions.


## Repository Information

- **Main Repository**: `https://github.com/ssec-jhu/base-template`

## How to Fork the Repository

1. **Go to the Repository on GitHub**:
   - Open your web browser and navigate to the main repository you want to fork. For this project, the URL is `https://github.com/ssec-jhu/base-template`.

2. **Click the Fork Button**:
   - In the upper-right corner of the repository page, you’ll see a button labeled **Fork**. Click it. 
   - GitHub will ask you to select your GitHub account or organization where you want the fork to be created.

3. **Clone Your Fork Locally**:
   - Once your fork is created, you can clone it to your local machine to start working:
   ```bash
   git clone https://github.com/your-username/base-template
   cd <repo dir>
   ```

You now have your own copy (fork) of the repository where you can make changes independently from the main repository. When you’re ready to contribute back, you can create a pull request from your fork to the main repository.

## Getting Started

1. **Fork and Clone the Repository**:
   - Follow the instructions in the [How to Fork the Repository](#how-to-fork-the-repository) section.
   ```

2. **Add the Main Repository as Upstream**: To keep your fork in sync with the latest updates from the main repo, add it as a second remote named `upstream`:
   ```bash
   git remote add upstream https://github.com/ssec-jhu/base-template
   ```

3. **Create a Branch**: Create a new branch for each feature or bug fix:
   ```bash
   git fetch --all
   git checkout upstream/main
   git checkout -b feature/your-feature-name
   ```

## Making Changes

- **Coding Standards**: Follow PEP 8 for Python code (or your organization’s standards). Use `tox -e check-style` to ensure code formatting aligns with the repository’s requirements.
- **Testing**: Ensure your changes pass all tests. Include relevant tests for any new features you add.
- **Documentation**: Update the documentation for any significant code changes. This includes comments, docstrings, and relevant updates to the `README.md`.

## Keeping Your Fork Updated

Regularly pull updates from the main repository to keep your fork in sync:
```bash
git fetch upstream
git checkout <branch-to-update>
git rebase upstream/main
```

## Submitting a Pull Request

When you’re ready to contribute your changes:

1. **Commit Your Changes**: Write concise and descriptive commit messages.
   ```bash
   git add <path-to-newly-added-file-if-applicable>
   git commit -am "Description of changes"
   ```

2. **Push to Your Fork**:
   ```bash
   git push origin feature/your-feature-name
   ```

3. **Open a Pull Request**:
   - Go to your forked repository on GitHub.
   - Click on **New Pull Request**.
   - Ensure the base repository is `https://github.com/ssec-jhu/base-template` and the base branch is `main`.
   - Provide a title and description for your pull request.
   - Submit the pull request for review.

## Code Review Process

Once you submit a pull request:
- The maintainers will review your changes and may request modifications.
- Please address any feedback and re-submit for review.

## Issues and Support

If you encounter issues or have questions, feel free to open an issue on GitHub. We’ll do our best to assist.

## License

By contributing, you agree that your contributions will be licensed under the same open-source license as the project.

## Authorship

Thank you for contributing to this repo! If you would like to be cited as an author/contributor of this project please
open a PR adding yourself to the [.zenodo.json file](.zenodo.json) along with your [ORCID ID](https://orcid.org/).

---

Thank you for your contributions to package_name! We’re excited to work with you.


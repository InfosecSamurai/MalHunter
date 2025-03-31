# MalHunter - Advanced Malware Analysis Sandbox

[![Build Status](https://img.shields.io/github/workflow/status/InfosecSamurai/malhunter/CI)](https://github.com/InfosecSamurai/malhunter/actions)
[![Code Coverage](https://img.shields.io/codecov/c/github/InfosecSamurai/malhunter)](https://codecov.io/gh/InfosecSamurai/malhunter)
[![License](https://img.shields.io/github/license/InfosecSamurai/malhunter)](https://github.com/InfosecSamurai/malhunter/blob/main/LICENSE)

## Introduction
Thank you for considering contributing to MalHunter! We welcome contributions from developers, security researchers, and anyone passionate about improving the state of malware analysis tools. By contributing, you'll help enhance the functionality, stability, and usability of this advanced malware analysis sandbox.

MalHunter is designed for automated static and dynamic analysis of suspicious files, with support for both Python and Docker environments. Whether you're interested in adding new features, improving existing functionality, or fixing bugs, your contributions are vital to the success of the project.

## How to Contribute

### 1. Fork the Repository
Start by forking the repository to your own GitHub account. This allows you to freely experiment with changes without affecting the original project.

1. Navigate to [MalHunter GitHub repository](https://github.com/InfosecSamurai/malhunter).
2. Click the **Fork** button at the top-right corner of the page.
3. Clone your fork to your local machine using:
   ```bash
   git clone https://github.com/your-username/malhunter.git

2. Create a Branch

After cloning the repository, create a new branch for your work. It’s best practice to create a branch for each feature or bug fix you’re working on.

git checkout -b feature/your-feature-name

Or for bug fixes:

git checkout -b bugfix/issue-number

3. Make Your Changes

Work on your changes in your branch. Make sure to follow the code style and conventions used in the project.

Guidelines:

Python code: Follow PEP 8 standards and write clean, readable code.

Docker: Ensure that Docker-related changes are thoroughly tested in both development and production environments.

Documentation: Update the README, inline comments, and any relevant documentation to reflect your changes.

Tests: If applicable, add new tests for your changes. We aim for high test coverage for the project.


4. Commit Your Changes

Once your changes are ready, commit them to your branch. Write clear and concise commit messages.

Example:

git add .
git commit -m "Added new YARA rule support"

5. Push Your Changes

Push your changes to your forked repository on GitHub.

git push origin feature/your-feature-name

6. Open a Pull Request (PR)

Once your changes are pushed to GitHub, open a pull request (PR) to the main repository.

1. Go to the Pull Requests tab of the main repository.


2. Click New Pull Request.


3. Choose your branch and the base branch (usually main or master).


4. Provide a detailed description of the changes, why they’re necessary, and any relevant details.



7. Review and Merge

Once your PR is submitted, a maintainer will review your changes. You may be asked to make further modifications. After review, your PR will be merged into the main codebase.

Code of Conduct

By participating in this project, you agree to follow our code of conduct. Please be respectful, kind, and supportive to others in the community.

Be respectful: Treat all individuals with respect and kindness.

Be constructive: Provide feedback in a way that promotes learning and improvement.

Be inclusive: Create an inclusive, welcoming environment for contributors of all backgrounds and skill levels.


Reporting Bugs

If you encounter a bug, please follow the steps below to report it:

1. Check the Issue Tracker: Before reporting, search the Issues to see if the bug has already been reported.


2. Provide Reproduction Steps: Include a detailed description of how to reproduce the bug, including any sample files or commands used.


3. Error Logs: If applicable, provide any relevant logs or error messages to help us diagnose the issue.


4. Operating System and Version: Specify which operating system (Windows/Linux) and version you are using.



Example:

Bug Title: MalHunter crashes when analyzing large files.

Steps to reproduce:
1. Clone the repository.
2. Run `python main.py samples/large_sample.exe`.
3. Observe crash with error message: "Segmentation fault."

Operating System: Linux 5.4
Python Version: 3.9.5

Feature Requests

If you have an idea for a new feature, we encourage you to submit a feature request.

1. Search Existing Feature Requests: Check the Issues to see if the feature has already been requested.


2. Provide Details: Be as detailed as possible about the feature, its purpose, and how it would benefit users.



Example:

Feature Request: Integrate threat intelligence feeds for real-time analysis.

Details:
- Add integration with known threat intelligence platforms such as VirusTotal or IBM X-Force.
- Automatically update YARA rules and threat databases based on feeds.

Testing

We strive for comprehensive testing coverage across all components of MalHunter. If your contribution includes changes to existing functionality or introduces new functionality, please add relevant unit tests and integration tests.

Running Tests Locally:

To run the test suite locally:

1. Install test dependencies:

pip install -r requirements-dev.txt


2. Run the tests:

pytest



Tests should pass before submitting your pull request.

Documentation

We value clear and concise documentation for both users and developers. If you make changes to the codebase that affect how the software is used or configured, please update the documentation accordingly.

Documentation Files:

README.md: High-level information about the project, installation, and usage.

docs/: Any additional guides or detailed documentation (e.g., developer guides, API docs).

Inline comments: Brief explanations of complex code sections.


License

By contributing to MalHunter, you agree that your contributions will be licensed under the MIT License.

Thank You!

We appreciate your interest in improving MalHunter! Every contribution helps make this project more robust and useful to the community. If you have any questions or need help getting started, don't hesitate to reach out!


---

Happy Hacking! 🛡️🔍
# Contributing to [Project Name]

Thanks for your interest in contributing! This document explains how to
report bugs, suggest features, and submit changes.

## Table of Contents

- [Ways to Contribute](#ways-to-contribute)
- [Development Setup](#development-setup)
- [Coding Standards](#coding-standards)
- [Pull Request Process](#pull-request-process)
- [Reporting Bugs](#reporting-bugs)
- [Suggesting Features](#suggesting-features)
- [Security Vulnerabilities](#security-vulnerabilities)
- [Community Guidelines](#community-guidelines)
- [Questions](#questions)

## Ways to Contribute

Code is not the only way to help:

- **Report bugs** — open an issue with the bug report template.
- **Suggest features** — describe the problem before proposing a solution.
- **Improve documentation** — fix typos, outdated examples, or unclear steps.
- **Triage issues** — reproduce reports, add missing details, or suggest labels.
- **Answer questions** — help other users in Discussions or the issue tracker.

### Finding issues to work on

Look for the `good first issue` or `help wanted` labels — maintainers curate
those for new contributors. Comment on an issue before starting so nobody
duplicates your work.

## Development Setup

    # 1. Fork the repository on GitHub, then clone YOUR fork
    git clone https://github.com/[your-user]/[repo].git
    cd [repo]

    # 2. Add the original repo as upstream so you can sync later
    git remote add upstream https://github.com/[org]/[repo].git

    # 3. Install dependencies and verify the setup
    [install command]
    [test command]

    # 4. Create a branch for your change
    git checkout -b feature/your-feature-name

## Coding Standards

- Follow the style conventions of the language and framework in use.
- Run the linter before committing: `[lint command]`
- Format code with: `[format command]`
- Add tests for every new feature; keep coverage above [coverage target]%.

### Commit messages

We use [Conventional Commits](https://www.conventionalcommits.org/):

    feat: add email validation to signup form
    fix: resolve null pointer in payment retry
    docs: update API examples for v2 endpoints

Sign your commits if the project requires a DCO (`git commit -s`). Check
`CLA.md` or `DCO.md` in the repository for the policy — some projects accept
contributions without any formal agreement.

## Pull Request Process

1. Branch from `main` using `feature/`, `fix/`, or `docs/` prefixes.
2. Keep the PR focused — one change per pull request.
3. Push to your fork and open a PR with the provided template.
4. Link the related issue: write `Closes #123` in the description.
5. Wait for CI to pass, then address reviewer feedback.
6. A maintainer merges once approved. Squash commits if asked.

### PR checklist

- [ ] Tests added or updated
- [ ] Documentation updated
- [ ] Linter and formatter pass
- [ ] Commit messages follow the convention
- [ ] The PR description explains what and why

## Reporting Bugs

1. Search existing issues first — duplicates get closed.
2. Open a new issue with the bug report template.
3. Include steps to reproduce, expected vs actual behavior, environment
   details (OS, version), and logs or screenshots when relevant.

## Suggesting Features

1. Open an issue describing the problem you want solved, not just the API
   you want added.
2. Wait for maintainer feedback before writing the implementation — large
   features may need an RFC first.
3. Once agreed, follow the pull request process above.

## Security Vulnerabilities

**Do not open a public issue for security problems.** Instead:

- Report them privately through the `SECURITY.md` policy or
  [security contact / advisory URL].
- Include a proof of concept or reproduction steps when possible.
- Expect an acknowledgement within [response time] days.

## Community Guidelines

This project follows the [Code of Conduct](CODE_OF_CONDUCT.md). Be respectful,
assume good intent, and keep feedback about the code — not the person.

Contributors are credited in the README or `CONTRIBUTORS` file and in release
notes.

## Questions

- Open a Discussion for general questions.
- Join [Discord/Slack URL] for real-time chat.
- Email [contact email] for private inquiries.

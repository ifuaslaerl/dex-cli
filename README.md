# dex-cli

**dex-cli** is a command-line tool designed to help developers record, bootstrap, and manage their development projects—akin to a high-tech "dex" recording data on various project "species".

This tool automates the tedious parts of starting a new project: copying templates, initializing a local Git repository, and instantly creating a private remote repository on GitHub.

## Features

- **⚡ Template-Based Creation**: Instantly scaffold new projects using pre-defined templates (e.g., C++ projects, Competitive Programming setups).
- **🤖 Automatic Git Initialization**: Initializes a Git repository and authors the first commit automatically.
- **☁️ GitHub Integration**: Uses the GitHub CLI (`gh`) to create a **private** remote repository and push your initial code immediately.
- **⚙️ Configuration Management**: Remembers your identity and GitHub username to streamline repository creation.
- **🗑️ Project Deletion**: Safely (but destructively) removes local project directories and their corresponding remote GitHub repositories.

## Prerequisites

To use `dex-cli`, you must have the following tools installed and configured:

1. **Python 3.9+**
2. **Git**: For version control operations.
3. **GitHub CLI (`gh`)**: For remote repository management.
   - Install: [cli.github.com](https://cli.github.com/)
   - Authenticate: `gh auth login`
   - **Important**: To use the delete command, you must grant the delete scope:
```bash
gh auth refresh -s delete_repo
```

## Installation

Since this project uses `pyproject.toml`, you can install it directly from the source directory:

```bash
# From the root of the project directory
pip install .
```

*Note: If/when published to PyPI, you would use `pip install dex-cli`.*

## Configuration

Before creating your first project, you should configure `dex` with your Git details. This ensures your commits are authored correctly and repositories are created under the correct GitHub user.

```bash
dex config
```

This command will:
1.  Read your global `.gitconfig` for defaults.
2.  Prompt you to set/update your **Name**, **Email**, and **GitHub Username**.
3.  Save these details to `~/.config/dex/git_info.json`.

## Usage

### 1. Create a New Project

The `new` command scaffolds a project, initializes Git, and creates a remote repo.

```bash
dex new <project-name> [options]
```

**Options:**
- `-t, --template <name>`: Specify a template to use. Defaults to `default`.

**Examples:**

```bash
# Create a basic project using the default template
dex new my-app

# Create a C++ project with Makefile structure
dex new my-game-engine --template cpp_project

# Create a setup for competitive programming
dex new codeforces-round-900 --template contest
```

### 2. Available Templates

`dex-cli` comes with bundled templates that are installed to `~/.config/dex/templates/` on the first run.

- **default**: A basic README structure.
- **cpp_project**: A standard C++ setup with a `src/` folder, `Makefile`, and `.gitignore`.
- **contest**: A specialized setup for competitive programming containing debug headers (`.debug.h`) and template files (`a.cpp` through `g.cpp`) pre-configured for testing.

*You can add your own custom templates by creating new folders in `~/.config/dex/templates/`.*

### 3. Delete a Project

This command permanently deletes a project's local directory and its remote GitHub repository.

```bash
dex delete <project-name> [options]
```

**Options:**
- `--local-only`: Only delete the local directory.
- `--remote-only`: Only delete the remote GitHub repository.

**Safety:**
To prevent accidents, this command requires two confirmations, including typing the full name of the repository (e.g., `username/project-name`).

## Directory Structure

`dex-cli` stores your user configuration and templates locally:

```text
~/.config/dex/
├── git_info.json       # User configuration
└── templates/          # Directory containing all project templates
    ├── default/
    ├── contest/
    └── cpp_project/
```

## License

[Add LICENSE later]

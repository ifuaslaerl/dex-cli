dex-cli

dex-cli is a command-line tool to help you manage and automate the creation of your development projects. It's designed to be a high-tech "dex" that records and bootstraps all the "species" of projects you work on.

This tool automates project setup by copying templates, initializing a local Git repository, and creating a private remote repository on GitHub.

Project Status

[x] Core: Project bootstrapping (dex new)

[x] Core: Configuration management (dex config)

[x] Core: Project deletion (dex delete)

[ ] Planned: List and manage existing projects (e.g., dex list)

Features

Template-Based Creation: Create new projects from pre-defined templates.

Automatic Git Init: Automatically initializes a new Git repository for your project.

GitHub Integration: Automatically creates a private GitHub repository and pushes the initial commit (requires gh CLI).

Configuration Management: Remembers your Git and GitHub details for automatic authoring and repo linking.

Installation

(This section is a guide for how you would document the installation once it's on PyPI).

pip install dex-cli


Requirements

For the tool to function, you must have the following command-line tools installed and configured on your system:

Git: For initializing the local repository.

GitHub CLI (gh): For creating and deleting the remote repository.

You must be authenticated: gh auth login

You must add the delete_repo scope for the delete command to work: gh auth refresh -s delete_repo

Commands

dex config

Before you start, run the config command to tell dex about your Git/GitHub user. This will be used to author your commits and link your GitHub account.

dex config


This command will first check your global git config for user.name and user.email. It will then prompt you to set or update this information, along with your GitHub username (which is used for generating repository URLs).

Your information is saved locally in ~/.config/dex/git_info.json.

dex new <project-name>

This is the main command for creating a new project.

dex new my-awesome-project


When you run this, dex-cli will:

Copy the default template into a new folder named my-awesome-project.

Initialize a Git repository in that folder.

Make the first commit, using the author info from your dex config.

Use the gh CLI to create a new private repository on GitHub named my-awesome-project.

Push the initial commit to the remote repository.

Options

--template <template_name> or -t <template_name>:
Use a specific template from your ~/.config/dex/templates directory.

dex new my-cpp-project --template cpp


dex delete <project-name>

This command deletes a project's local directory and its remote GitHub repository. This is a highly destructive and irreversible action.

dex delete my-awesome-project


The command will force you to confirm the action twice, including typing out the full repository name (e.g., username/my-awesome-project) to proceed.

Options

--local-only: Only deletes the local project folder.

--remote-only: Only deletes the remote GitHub repository.

Templates

dex-cli is a template-based system. On its first run, it will install a default template into your user configuration directory.

Template Location: ~/.config/dex/templates/

You can add your own templates by simply creating a new folder in this directory. For example, if you create ~/.config/dex/templates/cpp, you can then use it with the --template cpp option.

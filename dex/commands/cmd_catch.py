# dex/commands/cmd_catch.py
import click
from pathlib import Path
from dex.config import Config
from dex.git import GitManager

@click.command()
@click.argument("repo_identifier")
def catch_command(repo_identifier):
    """
    Clones a repository from GitHub to the current directory.

    REPO_IDENTIFIER can be:
      - A simple name (e.g., 'my-project') -> assumes it belongs to YOU.
      - A full name (e.g., 'owner/repo') -> clones that specific repo.
    """
    config = Config()
    git_manager = GitManager(config)

    # Determine the full repository name (owner/repo)
    if "/" in repo_identifier:
        # User provided "owner/repo"
        full_repo_name = repo_identifier
        project_dir_name = repo_identifier.split("/")[-1]
    else:
        # User provided just "repo", assume it belongs to the config user
        gh_user = git_manager.get_github_username()
        if not gh_user:
            click.secho("GitHub username not configured.", fg="red")
            click.secho("Please run 'dex config' first, or provide the full 'owner/repo' name.", fg="yellow")
            raise click.Abort()
        
        full_repo_name = f"{gh_user}/{repo_identifier}"
        project_dir_name = repo_identifier

    dest_path = Path.cwd() / project_dir_name

    if dest_path.exists():
        click.secho(f"Error: Directory '{project_dir_name}' already exists.", fg="red")
        return

    try:
        click.secho(f"Catching (cloning) repository '{full_repo_name}'...", fg="cyan")
        git_manager.clone_repo(full_repo_name, dest_path)
        
        click.secho(f"Successfully caught '{project_dir_name}'.", fg="green")
        click.secho(f"You can now start developing at: {dest_path}", fg="white")

    except Exception as e:
        click.secho(f"Failed to catch repository.", fg="red")
        # The GitManager usually prints the specific error from 'gh', so we just show a summary here

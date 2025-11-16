# dex/commands/cmd_delete.py
import click
import shutil
import subprocess
from pathlib import Path

from dex.config import Config
from dex.git import GitManager

@click.command()
@click.argument("project_name")
@click.option(
    "--local-only",
    is_flag=True,
    help="Only delete the local project directory."
)
@click.option(
    "--remote-only",
    is_flag=True,
    help="Only delete the remote GitHub repository."
)
def delete_command(project_name, local_only, remote_only):
    """
    Deletes a project's local directory and remote GitHub repo.

    This is a destructive and IRREVERSIBLE action.
    """
    config = Config()
    git_manager = GitManager(config)
    gh_user = git_manager.get_github_username()

    if not gh_user:
        click.secho("GitHub username not configured. Run 'dex config' first.", fg="red")
        click.secho("Cannot determine remote repository name to delete.", fg="red")
        raise click.Abort()

    full_repo_name = f"{gh_user}/{project_name}"
    local_path = Path.cwd() / project_name

    # Determine what to do based on flags
    delete_local = not remote_only
    delete_remote = not local_only
    
    # --- Serious Warning & Confirmation Flow ---

    click.secho("\n--- DANGER ---", fg="red", bold=True)
    click.secho("You are about to permanently delete the following:", fg="yellow")
    if delete_local:
        click.secho(f"  [Local]:  {local_path}", bold=True)
    if delete_remote:
        click.secho(f"  [Remote]: {full_repo_name}", bold=True)
    click.secho("\nThis action is IRREVERSIBLE and cannot be undone.", fg="red", bold=True)

    # Confirmation 1: Simple Yes/No
    if not click.confirm(f"Are you sure you want to proceed?", abort=True):
        # This will abort if they say no
        pass
    
    click.secho("Final confirmation required.", fg="yellow")

    # Confirmation 2: Type the full repo name
    confirmation_prompt = f"To confirm deletion, please type the full remote repo name ({full_repo_name}):"
    
    # If they are only deleting locally, this is annoying.
    # Let's make them type the local folder name instead.
    if local_only:
         confirmation_prompt = f"To confirm deletion, please type the local project name ({project_name}):"

    user_confirmation = click.prompt(confirmation_prompt)
    
    expected_confirmation = full_repo_name
    if local_only:
        expected_confirmation = project_name

    if user_confirmation != expected_confirmation:
        click.secho(f"Confirmation failed. Input '{user_confirmation}' does not match '{expected_confirmation}'.", fg="red")
        click.secho("Deletion aborted.", fg="red")
        raise click.Abort()

    click.secho("\nConfirmation accepted. Proceeding with deletion...", fg="cyan")

    # --- Deletion Logic ---

    if delete_remote:
        try:
            click.secho(f"Attempting to delete remote repo {full_repo_name}...", fg="cyan")
            git_manager.delete_remote_repo(full_repo_name)
            click.secho(f"Successfully deleted remote repo {full_repo_name}.", fg="green")
        except Exception as e:
            click.secho(f"Could not delete remote repo.", fg="red")
            click.secho(f"Error: {e}", fg="yellow")

    if delete_local:
        if local_path.exists():
            try:
                click.secho(f"Attempting to delete local directory {local_path}...", fg="cyan")
                shutil.rmtree(local_path)
                click.secho(f"Successfully deleted local directory {local_path}.", fg="green")
            except OSError as e:
                click.secho(f"Could not delete local directory.", fg="red")
                click.secho(f"Error: {e}", fg="yellow")
        else:
            click.secho(f"Local directory {local_path} not found, skipping.", fg="yellow")

    click.secho("\nDeletion process finished.", fg="green")

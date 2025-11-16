# dex/commands/cmd_delete.py
import click
import shutil
from pathlib import Path
from dex.config import Config
from dex.git import GitManager

@click.command()
@click.argument("project_name")
@click.option(
    "--local",
    is_flag=True,
    help="Also delete the local project folder."
)
def delete_command(project_name, local):
    """
    Delete a GitHub repository and optionally the local folder.

    This command will attempt to delete the remote GitHub repository
    named <project_name> associated with your configured GitHub user.

    This is a DESTRUCTIVE operation.
    """
    config = Config()
    config.setup() # Ensures config is loaded
    git_manager = GitManager(config) # This loads current info

    gh_user = git_manager.get_github_username()
    if not gh_user:
        click.secho("GitHub username not found.", fg="red")
        click.secho("Please run 'dex config' to set your GitHub user.", fg="yellow")
        return

    full_repo_name = f"{gh_user}/{project_name}"
    local_path = Path.cwd() / project_name

    # --- User Confirmation ---
    click.secho(f"You are about to delete the GitHub repository:", fg="yellow", bold=True)
    click.secho(f"    {full_repo_name}", fg="red", bold=True)
    
    if local:
        click.secho(f"\nYou have also requested to delete the local folder:", fg="yellow", bold=True)
        if local_path.exists():
            click.secho(f"    {local_path.resolve()}", fg="red", bold=True)
        else:
            click.secho(f"    (Local folder ./{project_name} not found, will only attempt remote delete)", fg="yellow")
        
    click.secho("\nThis action CANNOT be undone.", fg="red", bold=True, blink=True)

    # First confirmation
    if not click.confirm(f"Are you absolutely sure you want to proceed?", abort=True):
        # abort=True will exit the script if user says No.
        pass

    click.echo("Proceeding with remote deletion...")
    
    # 1. Delete Remote Repo
    # This will trigger a second confirmation from 'gh'
    success = git_manager.delete_remote_repo(project_name)

    if not success:
        click.secho("Remote repository deletion failed.", fg="red")
        # Ask user if they still want to delete local
        if local and local_path.exists():
            if click.confirm(f"Do you *still* want to delete the local folder './{project_name}'?", default=False, abort=True):
                 pass # Proceed to local deletion
            else:
                 click.secho("Aborting local delete.", fg="yellow")
                 return # Exit
        else:
            return # Exit
        
    # 2. Delete Local Folder (if flagged)
    if local:
        if not local_path.exists():
            click.secho(f"Local folder './{project_name}' not found. Skipping local delete.", fg="yellow")
        else:
            try:
                click.secho(f"Deleting local folder: {local_path.resolve()}", fg="yellow")
                shutil.rmtree(local_path)
                click.secho(f"Successfully deleted local folder '{project_name}'.", fg="green")
            except OSError as e:
                click.secho(f"Error deleting local folder: {e}", fg="red")

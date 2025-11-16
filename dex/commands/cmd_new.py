# Main file to command "new"

import click
import shutil
from pathlib import Path
from dex.config import Config
from dex.git import GitManager

@click.command()
@click.argument("project_name")
@click.option(
    "--template",
    "-t",
    default="default",
    help="Template folder name at \"~/.config/dex/templates\"."
)
def new_command(project_name, template):
    """
    Create new project [PROJECT_NAME] by template.
    """
    # Use our new Config class
    config = Config()
    config.setup() # This ensures all config files/dirs are ready

    # Use our new GitManager class
    git_manager = GitManager(config)

    source_path = config.templates_dir / template
    dest_path = Path.cwd() / project_name

    if not source_path.is_dir():
        click.secho(f"ERROR: Template \"{template}\" not found", fg="red")
        click.secho(f"Expected path: \"{source_path}\"")
        click.secho("Please, create template or use 'default'.")
        return

    if dest_path.exists():
        click.secho(f"Error: Directory \"{project_name}\" already exists.", fg="red")
        return

    try:
        click.secho(f"Creating \"{project_name}\" with template \"{template}\"...", fg="cyan")
        shutil.copytree(source_path, dest_path)

        # --- NEW OOP GIT LOGIC ---
        git_manager.initialize_repo_and_create_remote(project_name, dest_path)

    except Exception as e:
        click.secho(f"An unexpected error has ocurred: {e}", fg="red")

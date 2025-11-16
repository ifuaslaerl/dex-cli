# Main file to command "new"

import click
import shutil
import subprocess
from pathlib import Path

CONFIG_DIR = Path.home() / ".config" / "dex"
TEMPLATES_DIR = CONFIG_DIR / "templates"

def setup_config_dir():
    """
    Guarantee that the directory \"~/.config/dex/tempaltes\" exists.
    """
    if not TEMPLATES_DIR.is_dir():
        click.secho("Directory not found.", fg="yellow")
        click.secho(f"Creating directory in {TEMPLATES_DIR}.", \
            fg="yellow")
        try:
            TEMPLATES_DIR.mkdir(parents=True, exist_ok=True)
            click.secho("Config directory sucessfully made.", fg="green")
        except OSError as e:
            click.secho("Critical Error: Not possible to create" + \
                "config directory", fg="red")
            click.secho(f"Detail: {e}")
            raise click.Abort()

@click.command()
@click.argument("project_name")
@click.option(
    "--template",
    "-t",
    default="default",
    help="Template folder name at \"~/.config/dex/templates\"."
)
@click.option(
    "--public",
    "-pub",
    default=False,
    help="Set visibility to new repository on github."
)
def new_command(project_name, template, public):
    """
    Create new project [PROJECT_NAME] by template.
    """

    setup_config_dir()

    source_path = TEMPLATES_DIR / template
    dest_path = Path.cwd() / project_name

    if not source_path.is_dir():
        click.secho(f"ERROR: Template \"{template}\" not found", fg="red")
        click.secho(f"Expected path: \"{source_path}\"")
        click.secho("Please, create template and try again")
        return

    if dest_path.exists():
        click.secho(f"Error: Directory \"{project_name}\"" + \
            "already exists.", fg="red")
        return

    try:
        click.secho(f"Creating \"{project_name}\ with template" + \
            f"{template}\"...")
        shutil.copytree(source_path, dest_path)

        click.secho("Initializing new git repository.", fg="cyan")
        subprocess.run(["git", "init"], cwd=dest_path, check=True, capture_output=True)
        subprocess.run(["git", "add", "."], cwd=dest_path, check=True, capture_output=True)
        subprocess.run(["git", "commit", "-m", "Initial Commit from dex-cli"],
                       cwd=dest_path, check=True, capture_output=True)

        click.secho(f"Creating github repository named {project_name}.", fg="cyan")

        public = "--public" if public else "--private"

        subprocess.run(["gh", "repo", "create", project_name, public, "-s", ".", "--push"],
                        cwd=dest_path, check=True, capture_output=True)

        click.secho(f"Sucessfully created {project_name}.", fg="green")
        click.secho(f"View it on GitHub: https://github.com/{gitConfig.getUser().getName()}/{project_name}", fg="white")

    except subprocess.CalledProcessError as e:
        click.secho(f"\nA Command Failed", fg="red")
        click.secho(f"STDOUT: {e.stdout.decode()}", fg="yellow")
        click.secho(f"STDERR: {e.stderr.decode()}". fg="red")

    except Exception as e:
        click.secho(f"An unexpected error has ocurred: {e}", fg="red")



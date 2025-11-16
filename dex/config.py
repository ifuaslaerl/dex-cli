# dex/config.py
import click
import shutil
import json
from pathlib import Path

# Use importlib.resources for modern Python (3.9+)
# For < 3.9, you'd use pkg_resources, but this is cleaner.
try:
    import importlib.resources as pkg_resources
except ImportError:
    # Fallback for Python < 3.7
    import importlib_resources as pkg_resources

# Import the 'templates' directory *within* the 'dex' package
from . import templates as pkg_templates


class Config:
    """
    Manages the configuration, paths, and setup for dex-cli.
    """
    def __init__(self):
        self.config_dir = Path.home() / ".config" / "dex"
        self.templates_dir = self.config_dir / "templates"
        self.git_info_path = self.config_dir / "git_info.json"

    def setup(self):
        """
        Ensures all necessary config directories and files exist.
        This will be run by commands that need it.
        """
        try:
            # 1. Ensure the main config and templates directories exist
            self.templates_dir.mkdir(parents=True, exist_ok=True)

            # 2. Copy the default template if it doesn't exist
            self._install_default_template()

        except OSError as e:
            click.secho("Critical Error: Not possible to create config directory.", fg="red")
            click.secho(f"Detail: {e}", fg="red")
            raise click.Abort()

    def _install_default_template(self):
        """
        Copies the default template from the package data into the
        user's config directory.
        """
        default_template_dest = self.templates_dir / "default"
        if default_template_dest.exists():
            # Already installed, do nothing
            return

        try:
            # Find the path to the 'default' template *inside* the package
            # 'pkg_templates' is the imported 'dex.templates' module
            with pkg_resources.path(pkg_templates, 'default') as source_path:
                click.secho(f"Installing default template to {default_template_dest}...", fg="yellow")
                shutil.copytree(source_path, default_template_dest)

        except Exception as e:
            click.secho(f"Warning: Could not install default template.", fg="yellow")
            click.secho(f"Error: {e}", fg="yellow")

    def get_git_info(self) -> dict:
        """
        Reads Git info from the git_info.json file.
        """
        if not self.git_info_path.exists():
            return {}
        try:
            with open(self.git_info_path, 'r') as f:
                return json.load(f)
        except json.JSONDecodeError:
            return {}

    def save_git_info(self, name: str, email: str, username: str):
        """
        Saves Git info to the git_info.json file.
        """
        self.setup() # Ensure directory exists
        info = {
            "name": name,
            "email": email,
            "username": username
        }
        try:
            with open(self.git_info_path, 'w') as f:
                json.dump(info, f, indent=4)
            click.secho(f"Configuration saved to {self.git_info_path}", fg="green")
        except IOError as e:
            click.secho(f"Error saving config file: {e}", fg="red")

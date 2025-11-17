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

            # 2. Copy bundled templates if they don't exist
            self._install_bundled_templates()

        except OSError as e:
            click.secho("Critical Error: Not possible to create config directory.", fg="red")
            click.secho(f"Detail: {e}", fg="red")
            raise click.Abort()

    def _install_bundled_templates(self):
        """
        Copies all bundled templates (e.g., 'default', 'contest')
        from the package data into the user's config directory.
        Skips any templates that are already installed.
        """
        try:
            # Iterate over all items in the dex.templates package
            for template_name in pkg_resources.contents(pkg_templates):
                # Skip python files and pycache
                if template_name.startswith('__') or template_name.endswith('.py'):
                    continue

                dest_path = self.templates_dir / template_name

                # If it's already installed, skip it
                if dest_path.exists():
                    continue

                # Get the *actual* path to the bundled template
                with pkg_resources.path(pkg_templates, template_name) as source_path:
                    # Make sure it's a directory (not a random file)
                    if not source_path.is_dir():
                        continue
                    
                    click.secho(f"Installing template '{template_name}' to {dest_path}...", fg="yellow")
                    shutil.copytree(source_path, dest_path)

        except Exception as e:
            click.secho(f"Warning: Could not discover/install bundled templates.", fg="yellow")
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

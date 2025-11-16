import click
import subprocess
from .config import Config
from pathlib import Path

class GitManager:
    """
    Handles all Git-related operations, including reading config
    and initializing repositories.
    """
    def __init__(self, config: Config):
        self.config = config
        self.git_info = self._load_git_info()

    def _run_command(self, *args, raise_on_error=True, **kwargs):
        """Helper to run subprocess commands and capture output."""
        try:
            result = subprocess.run(
                args,
                check=True,
                capture_output=True,
                text=True,
                **kwargs
            )
            return result.stdout.strip()
        except subprocess.CalledProcessError as e:
            # If raise_on_error is True, we let the exception bubble up.
            if raise_on_error:
                raise e
            # Otherwise, just return None (for non-critical commands)
            return None
        except FileNotFoundError as e:
            if raise_on_error:
                raise e
            return None

    def _load_git_info(self) -> dict:
        """
        Loads Git user info, following a priority:
        1. Global `git config`
        2. Local `dex/git_info.json`
        """
        info = {}

        # 1. Try to get from global git config
        # We add raise_on_error=False so it fails silently if git isn't set up
        info['name'] = self._run_command("git", "config", "--global", "user.name", raise_on_error=False)
        info['email'] = self._run_command("git", "config", "--global", "user.email", raise_on_error=False)

        # 2. If not found in git, try local dex config
        local_info = self.config.get_git_info()
        if not info['name']:
            info['name'] = local_info.get('name')
        if not info['email']:
            info['email'] = local_info.get('email')

        # 'username' is for GitHub, so we only get it from our local config
        info['username'] = local_info.get('username')

        return info

    def get_user_name(self):
        return self.git_info.get('name')

    def get_user_email(self):
        return self.git_info.get('email')

    def get_github_username(self):
        return self.git_info.get('username')

    def initialize_repo_and_create_remote(self, project_name: str, project_path: str):
        """
        Runs the full sequence of 'git init', 'git commit', and 'gh repo create'.
        """
        click.secho("Initializing local git repository...", fg="cyan")
        try:
            # These commands will now use raise_on_error=True (the default)
            # and will fail into the 'except' block if they error out.
            self._run_command("git", "init", cwd=project_path)
            self._run_command("git", "add", ".", cwd=project_path)

            commit_msg = "Initial commit from dex-cli"
            # Try to commit with the user's name and email if we found it
            author_info = f"{self.get_user_name()} <{self.get_user_email()}>"
            if self.get_user_name() and self.get_user_email():
                 self._run_command("git", "commit", f"--author={author_info}", "-m", commit_msg, cwd=project_path)
            else:
                 self._run_command("git", "commit", "-m", commit_msg, cwd=project_path)

                 click.secho(f"Creating private GitHub repository named '{project_name}'...", fg="cyan")
            self._run_command(
                "gh", "repo", "create", project_name,
                "--private",     # Private by default
                "--source", ".", # Use the current directory as the source (Changed from -s)
                "--push",        # Push the initial commit
                cwd=project_path # Run in the new project's directory
            )

            click.secho(f"\nSuccessfully created '{project_name}'.", fg="green")

            # Try to show a helpful URL
            gh_user = self.get_github_username()
            if gh_user:
                click.secho(f"View it on GitHub: https://github.com/{gh_user}/{project_name}", fg="white")
            else:
                click.secho("Run 'dex config' to set your GitHub username for better output.", fg="yellow")

        except subprocess.CalledProcessError as e:
            click.secho(f"\n--- A Git command failed ---", fg="red", bold=True)
            click.secho(f"COMMAND: {' '.join(e.cmd)}", fg="white")
            click.secho(f"ERROR: {e.stderr}", fg="yellow") # <-- Removed .decode()
            click.secho("Project folder was created, but Git setup failed.", fg="yellow")
            click.secho("Please check if 'git' and 'gh' are installed and authenticated.", fg="yellow")
        except FileNotFoundError:
            click.secho("Error: 'gh' or 'git' command not found.", fg="red")
            click.secho("Please ensure both are installed and in your PATH.", fg="yellow")
        except Exception as e:
            click.secho(f"An unexpected error has ocurred during Git setup: {e}", fg="red")

    def delete_remote_repo(self, full_repo_name: str):
        """
        Deletes a remote repository from GitHub.
        Uses '--yes' to bypass the 'gh' interactive prompt.
        """
        click.secho(f"Sending 'gh repo delete {full_repo_name}' command...", fg="cyan", dim=True)
        # This will use raise_on_error=True by default
        self._run_command(
            "gh",
            "repo",
            "delete",
            full_repo_name,
            "--yes" # Bypasses the gh confirmation, as we have our own
        )

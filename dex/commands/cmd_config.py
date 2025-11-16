# dex/commands/cmd_config.py
import click
from dex.config import Config
from dex.git import GitManager

@click.command()
def config_command():
    """
    Set or view local Git user information for dex.
    """
    config = Config()
    git_manager = GitManager(config) # This loads current info

    # Get current values, show (dex config) or (git config)
    name = git_manager.get_user_name()
    email = git_manager.get_user_email()
    username = git_manager.get_github_username()

    click.secho("--- Current dex Git Configuration ---", bold=True)
    click.echo(f"Name:     {name or 'Not Set'}")
    click.echo(f"Email:    {email or 'Not Set'}")
    click.echo(f"GH User:  {username or 'Not Set'}")
    click.secho("-------------------------------------")
    click.secho("This info is read from 'git config' first, then 'git_info.json'.\n", dim=True)

    if not click.confirm("Do you want to set/update this info?", default=False):
        return

    click.secho("Please provide your info. This will be saved in git_info.json.", fg="yellow")

    new_name = click.prompt("Name", default=name or "")
    new_email = click.prompt("Email", default=email or "")
    new_username = click.prompt("GitHub Username (for repo URLs)", default=username or "")

    config.save_git_info(new_name, new_email, new_username)

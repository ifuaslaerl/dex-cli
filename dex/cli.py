# Main file to CLI use

import click
from .commands.cmd_new import new_command
from .commands.cmd_config import config_command
from .commands.cmd_delete import delete_command
from .commands.cmd_catch import catch_command # Import new command

@click.group()
def cli():
    """
    The dex is a high-tech electronic encyclopedia that developers have
    with them to record data on the varios species of projects they work
    during their journey.
    """
    pass

cli.add_command(new_command, name="new")
cli.add_command(config_command, name="config")
cli.add_command(delete_command, name="delete")
cli.add_command(catch_command, name="catch") # Add new command

if __name__ == "__main__":
    cli()

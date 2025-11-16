# Main file to CLI use

import click
from .commands.cmd_new import new_command
from .commands.cmd_config import config_command

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

if __name__ == "__main__":
    cli()

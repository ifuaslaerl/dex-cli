# Main file to CLI use

import click
import sys

from .commands.cmd_new import new_command

@click.group()
def cli():
    """
    The dex is a high-tech electronic encyclopedia that developers have
    with them to record data on the varios species of projects they work
    during their journey.

    """
    pass

cli.add_command(new_command, name="new")

if __name__ == "__main__":
    cli()

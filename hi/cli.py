from __future__ import absolute_import
import click
import sys

import hi
from .config import version

@click.command(
    help="""
A configurable shorthand for interfacing with external hosts.\n
\n
Arguments are individually matched against a set of specified hosts. If one result is found the command to interface with that host is run. Otherwise, all matching hosts are printed.
    """,
    epilog="""
\b\bConfigs:\n
\n
Configs are loaded from $HOME/.hi/hosts and $HOME/.hi/groups by default. Configs must be in YAML format.\n
\n
An example host config:\n
\n
  - host: example.com\n
    group: ssh\n
\n
An example group config:\n
  ssh:\n
    command: ssh\n
\n
\b\bRules:\n
\n
Arg rules are applied based on user input. When a user's input matches the name of a specified arg rule, the rule is executed for each host. Arg rules must take a host as an argument and return True or False if the host should be included. A host does not match unless all applicable arg rules return True.\n
\n
Host rules are applied based on the host. When the name of a specified host rule is found in the host, the rule is executed. Host rules must take a tuple of user arguments as an argument and return True or False if the host should be included. A host does not match unless all application host rules return True.
    """,
    context_settings={
        'help_option_names': ['-h','--help'],
    }
)
@click.argument('argv', nargs=-1)
@click.version_option(version=version)
@click.option('--run/--no-run', default=True, help='When enabled, run the command for a host when one match is found.')
@click.option('--hosts-file', help='File to load hosts from. Defaults to $HOME/.hi/hosts.')
@click.option('--groups-file', help='File to load host groups from. Defaults to $HOME/.hi/groups.')
@click.option('--rules/--no-rules', default=True, help='When enabled, use a default set of custom rules to match hosts.')
@click.option('--arg-rule', multiple=True, help='Specify an importable python function to be used as a rule for matching a host. Multiple are allowed. See Rules for more information.')
@click.option('--host-rule', multiple=True, help='Specify an importable python function to be used as a rule for matching a host. Multiple are allowed. See Rules for more information')
def cli(**kwargs):
    kwargs['hosts'] = hi.load_hosts(kwargs['hosts_file'])
    # Don't use the default groups file when using a custom hosts file to avoid unintended behavior/confusion
    if kwargs['hosts_file'] is not None and kwargs['groups_file'] is None:
        kwargs['groups'] = {}
    else:
        kwargs['groups'] = hi.load_groups(kwargs['groups_file'])
    del kwargs['hosts_file']
    del kwargs['groups_file']

    sys.exit(hi.run(**kwargs))

if __name__ == '__main__':
    cli()


import click
import sys

import hi
try:
    from .config import version
except (ValueError, SystemError):
    from config import version

@click.command(
    context_settings={
        'help_option_names': ['-h','--help'],
    }
)
@click.argument('argv', nargs=-1)
@click.version_option(version=version)
@click.option('--run/--no-run', default=True)
@click.option('--hosts-file')
@click.option('--groups-file')
@click.option('--rules/--no-rules', default=True)
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


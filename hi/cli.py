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
def cli(**kwargs):
    kwargs['hosts'] = hi.load_hosts()
    kwargs['groups'] = hi.load_groups()
    sys.exit(hi.run(**kwargs))

if __name__ == '__main__':
    cli()


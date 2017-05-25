try:
    from .cli import cli
except (ValueError, SystemError):
    from cli import cli

if __name__ == '__main__':
    cli()


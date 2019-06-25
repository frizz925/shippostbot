import json
import sys

import click

from . import main, setup_from_env


@click.command()
@click.option('-t', '--selection-type',
              default='FROM_CHARACTER_TO_MEDIA',
              help='Define how the bot selects the characters')
@click.option('-p', '--publisher',
              default='STREAM',
              help='Which publisher to use to publish the post')
@click.option('-s', '--storage',
              default='TEMP_FILE',
              help='Storage type to be used by the bot')
def main_runner(**kwargs):
    try:  # pragma: no cover
        from dotenv import load_dotenv, find_dotenv
        load_dotenv(find_dotenv())
    except ImportError:  # pragma: no cover
        pass

    setup_from_env()
    res = main(**kwargs)

    sys.stdout.write(json.dumps(res))
    sys.stdout.flush()


if __name__ == "__main__":  # pragma: no cover
    main_runner()

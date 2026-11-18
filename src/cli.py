from argparse import ArgumentParser, Namespace
from pathlib import Path
from .rendering.sprites import is_frozen
import sys


def command_line() -> str:
    """Parse the arguments and return the content of the config file"""
    def _parse() -> Namespace:
        """Parse sys.argv (one positional argument: the config file)."""
        parser = ArgumentParser(
            description='Pac-Man game')
        parser.add_argument(
            'config_file', type=Path,
            help='JSON file with the right format')
        return parser.parse_args()
    try:
        if not is_frozen():
            config_path = Path(_parse().config_file)

        else:
            config_path = Path(sys.executable).parent / "config.json"
        with open(config_path, "r") as f:
            content = f.read()
    except (OSError, ValueError) as e:
        raise OSError(e)
    return content

from argparse import Namespace, ArgumentParser
from pathlib import Path


def command_line() -> str:
    def _parse() -> Namespace:
        parser = ArgumentParser(
            description='Pac-Man game')
        parser.add_argument(
            'config_file', type=Path,
            help='JSON file with the right format')
        return parser.parse_args()
    try:
        config_path = _parse()
        with open(config_path.config_file, "r") as f:
            content = f.read()
    except (OSError, ValueError) as e:
        raise OSError(e)
    return content

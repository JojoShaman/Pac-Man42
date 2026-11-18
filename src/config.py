import json
import logging
from dataclasses import dataclass, field, fields
from functools import partial
from pathlib import PurePath
from typing import Any, Callable


class ConfigError(Exception):
    """Raised when a config value is invalid."""


@dataclass
class Level:
    """Maze dimensions of one level."""

    width: int = 15
    height: int = 15


def _default_levels() -> list[Level]:
    """Return the 10 default levels."""
    return [Level() for _ in range(10)]


@dataclass
class Config:
    """All the game settings, with their default values."""

    highscore_filename: str = "highscore.json"
    levels: list[Level] = field(default_factory=_default_levels)
    lives: int = 3
    pacgums: int = 42
    points_per_pacgum: int = 10
    points_per_super_pacgum: int = 50
    points_per_ghost: int = 200
    seed: int = 42
    level_max_time: int = 90


def _strip_comments(content: str) -> str:
    """Remove the lines starting with '#' (leading spaces ignored)."""
    lines = content.splitlines()
    return "\n".join(
        line for line in lines if not line.lstrip().startswith("#"))


def _validate_int(
        value: object,
        min_value: int, max_value: int | None) -> int:
    """Return value clamped to [min_value, max_value].

    Raise ConfigError if value is not an int (booleans are rejected).
    """
    if isinstance(value, bool) or not isinstance(value, int):
        raise ConfigError
    if value < min_value:
        return min_value
    if max_value is not None and value > max_value:
        return max_value
    return value


def _validate_filename(value: object) -> str:
    """Return value if it is a plain, non-empty file name."""
    if not isinstance(value, str):
        raise ConfigError
    name = value.strip()
    if not name or name in (".", "..") or PurePath(name).name != name:
        raise ConfigError
    return name


def _validate_level(value: object, nb_lvl: int) -> Level:
    """Build a Level from a dict, clamping each dimension (logged)."""
    if not isinstance(value, dict):
        raise ConfigError
    dimensions: dict[str, int] = {}
    for key, raw in value.items():
        if key not in LVL_DIMENSION_BOUNDS:
            logging.warning(f"Level {nb_lvl} - unknown key '{key}'")
            continue
        min_v, max_v = LVL_DIMENSION_BOUNDS[key]
        valid = _validate_int(raw, min_v, max_v)
        dimensions[key] = valid
        if raw != valid:
            logging.warning(
                f"Level {nb_lvl} - {key} clamped from {raw} to {valid}")
    return Level(**dimensions)


def _validate_levels(value: object) -> list[Level]:
    """Return 10 levels: the valid given ones, completed by defaults."""
    if not isinstance(value, list):
        raise ConfigError
    levels = _default_levels()
    if len(value) > 10:
        logging.warning("more than 10 levels given, extra ones ignored")
    for n, level in enumerate(value[:10]):
        try:
            levels[n] = _validate_level(level, n)
        except ConfigError:
            logging.error(f"Level {n} - invalid, using default level")
    return levels


def load_config(content: str) -> Config:
    """Parse the JSON content and return a Config.

    Lines starting with '#' are ignored. Missing or invalid keys fall back
    to their default, out-of-range values are clamped, unknown keys are
    ignored; everything is logged. Invalid JSON gives the default Config.
    """
    try:
        data = json.loads(_strip_comments(content))
    except ValueError:
        logging.error("config file is not valid JSON, using defaults")
        return Config()
    if not isinstance(data, dict):
        logging.error("config root must be a JSON object, using defaults")
        return Config()

    values: dict[str, Any] = {}
    keys = {f.name for f in fields(Config)}
    for key, value in data.items():
        if key not in keys:
            logging.warning(f"unknown key '{key}'")
            continue
        try:
            valid = VALIDATE[key](value)
        except ConfigError:
            logging.error(f"invalid value for '{key}', using default")
            continue
        values[key] = valid
        if key in INT_KEYS and value != valid:
            logging.warning(f"{key} clamped from {value} to {valid}")
    for key in keys - data.keys():
        logging.warning(f"missing key '{key}', using default")
    return Config(**values)


VALIDATE: dict[str, Callable[[object], Any]] = {
    "highscore_filename": _validate_filename,
    "levels": _validate_levels,
    "lives": partial(_validate_int, min_value=1, max_value=5),
    "pacgums": partial(_validate_int, min_value=10, max_value=1000),
    "points_per_pacgum": partial(_validate_int, min_value=0, max_value=1000),
    "points_per_super_pacgum": partial(
        _validate_int, min_value=0, max_value=5000),
    "points_per_ghost": partial(
        _validate_int, min_value=0, max_value=20000),
    "seed": partial(_validate_int, min_value=1, max_value=None),
    "level_max_time": partial(_validate_int, min_value=30, max_value=600),
}

INT_KEYS: set[str] = {
    "lives", "pacgums", "points_per_pacgum", "points_per_super_pacgum",
    "points_per_ghost", "seed", "level_max_time",
}

LVL_DIMENSION_BOUNDS: dict[str, tuple[int, int]] = {
    "width": (10, 50),
    "height": (10, 50),
}
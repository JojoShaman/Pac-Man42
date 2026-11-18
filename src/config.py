import json
import logging
from dataclasses import dataclass, field, fields
from typing import Any, Callable
from functools import partial


class ConfigError(Exception):
    """Raised when a config value is invalid."""

    ...


@dataclass
class Level:
    """Maze dimensions of one level."""

    width: int = 15
    height: int = 15


def _default_tags() -> list[Level]:
    """Return the 10 default levels."""
    return [Level() for _ in range(10)]


@dataclass
class Config:
    """All the game settings, with their default values."""

    highscore_filename: str = "highscore.json"
    levels: list[Level] = field(default_factory=_default_tags)
    lives: int = 3
    pacgums: int = 42
    points_per_pacgum: int = 10
    points_per_super_pacgum: int = 50
    points_per_ghost: int = 200
    seed: int = 42
    level_max_time: int = 90
    cheat_mode: bool = False


def _validate_int(
        value: object,
        min_value: int, max_value: int | None) -> int:
    """Return value clamped to [min_value, max_value];
        ConfigError if no int."""
    if not isinstance(value, int):
        raise ConfigError
    if value < min_value:
        value = min_value
    elif max_value and value > max_value:
        value = max_value
    return value


def _validate_bool(value: object) -> bool:
    """Return value if it is a bool, else raise ConfigError."""
    if not isinstance(value, bool):
        raise ConfigError
    return value


def _validate_filename(value: object) -> str:
    """Return value if it is a string, else raise ConfigError."""
    if not isinstance(value, str):
        raise ConfigError
    return value


def _validate_level(value: object, nb_lvl: int) -> Level:
    """Build a Level from a dict, clamping each dimension (logged)."""
    dimensions: dict[str, int] = {}
    if not isinstance(value, dict):
        raise ConfigError
    for a, b in value.items():
        min_v, max_v = LVL_DIMESION_BOUNDS[a]
        valid_v = _validate_int(b, min_v, max_v)
        dimensions[a] = valid_v
        if b != valid_v:
            logging.warning(
                f"Level {nb_lvl} - {a} clamped from "
                f"{b} to {dimensions[a]}")
    return Level(**dimensions)


def _validate_levels(value: object) -> list[Level]:
    """Return 10 levels: the valid given ones, completed by defaults."""
    if not isinstance(value, list):
        raise ConfigError
    levels: list[Level] = Config().levels
    max_lvl = 10 if len(value) >= 10 else len(value)
    for n, level in enumerate(value[:max_lvl]):
        try:
            levels[n] = _validate_level(level, n)
        except ConfigError:
            raise ConfigError
    return levels


def load_config(content: str) -> Config:
    """Parse the JSON content and return a Config.

    Invalid keys fall back to their default (logged); unknown keys are
    ignored. Invalid JSON raises ValueError.
    """
    values: dict[str, Any] = {}
    keys = set(k.name for k in fields(Config))
    try:
        config_load: dict[str, Any] = json.loads(content)
        if not isinstance(config_load, dict):
            logging.error("config file is not valid JSON, using defaults")
            return Config()
        for key, value in config_load.items():
            if key not in keys:
                logging.warning(f"unknown key '{key}'")
                continue
            try:
                if key in INT_V:
                    v_value = VALIDATE[key](value)
                    values[key] = v_value
                    if value != v_value:
                        logging.warning(
                            f"{key} clamped from {value} to {v_value}")
                else:
                    values[key] = VALIDATE[key](value)
            except ConfigError:
                logging.error(f"invalid value for {key}, using default")
        for k in keys:
            if k not in config_load:
                logging.warning(f"missing key '{k}'")
    except ValueError:
        logging.error("config file is not valid JSON, using defaults")
    return Config(**values)


VALIDATE: dict[str, Callable[[object], Any]] = {
    "highscore_filename": _validate_filename,
    "levels": _validate_levels,
    "lives": partial(
        _validate_int, min_value=1, max_value=5),
    "pacgums": partial(
        _validate_int, min_value=1, max_value=1000),
    "points_per_pacgum": partial(
        _validate_int, min_value=0, max_value=1000),
    "points_per_super_pacgum": partial(
        _validate_int, min_value=0, max_value=5000),
    "points_per_ghost": partial(
        _validate_int, min_value=0, max_value=20000),
    "seed": partial(
        _validate_int, min_value=1, max_value=None),
    "level_max_time": partial(
        _validate_int, min_value=30, max_value=600),
    "cheat_mode": _validate_bool
}

INT_V: list[str] = [
    "lives", "pacgums", "points_per_pacgum",
    "points_per_super_pacgum", "points_per_ghost",
    "seed", "level_max_time"
]

LVL_DIMESION_BOUNDS: dict[str, tuple[int, int]] = {
    "width": (10, 50),
    "height": (10, 50)
}

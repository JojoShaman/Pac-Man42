from dataclasses import (
    dataclass,
    fields,
    field)
from typing import Any, Callable
import json
import logging


class ConfigError(Exception):
    ...


@dataclass
class Level:
    width: int = 15
    height: int = 15


def _default_tags() -> list[Level]:
    return [Level() for _ in range(10)]


@dataclass
class Config:
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
    if not isinstance(value, int):
        raise ConfigError
    if value < min_value:
        value = min_value
    elif max_value and value > max_value:
        value = max_value
    return value


def _validate_bool(value: object) -> bool:
    if not isinstance(value, bool):
        raise ConfigError
    return value


def _validate_filename(value: object) -> str:
    if not isinstance(value, str):
        raise ConfigError
    return value


def _validate_level(value: object, nb_lvl: int) -> Level:
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
    values: dict[str, Any] = {}
    keys = set(k.name for k in fields(Config))
    try:
        config_load: dict[str, Any] = json.loads(content)
        for key, value in config_load.items():
            if key not in keys:
                logging.warning(f"unknown key '{key}'")
                continue
            try:
                if key in INT_BOUNDS:
                    min_v, max_v = INT_BOUNDS[key]
                    v_value = VALIDATE[key](value, min_v, max_v)
                    values[key] = v_value
                    if value != v_value:
                        logging.warning(
                            f"{key} clamped from {value} to {v_value}")
                else:
                    values[key] = VALIDATE[key](value)
            except ConfigError:
                logging.error(f"invalid value for {key}, using default")
                ...
        for k in keys:
            if k not in config_load:
                logging.warning(f"missing key '{k}'")
    except ValueError as e:
        raise ValueError(e)
    return Config(**values)


VALIDATE: dict[type[Any] | str | Any, Callable] = {
    "highscore_filename": _validate_filename,
    "levels": _validate_levels,
    "lives": _validate_int,
    "pacgums": _validate_int,
    "points_per_pacgum": _validate_int,
    "points_per_super_pacgum": _validate_int,
    "points_per_ghost": _validate_int,
    "seed": _validate_int,
    "level_max_time": _validate_int,
    "cheat_mode": _validate_bool
}

INT_BOUNDS: dict[str, tuple[int, int | None]] = {
    "lives": (1, 5),
    "pacgums": (10, 1000),
    "points_per_pacgum": (0, 1000),
    "points_per_super_pacgum": (0, 5000),
    "points_per_ghost": (0, 20000),
    "seed": (1, None),
    "level_max_time": (30, 600),
}

LVL_DIMESION_BOUNDS: dict[str, tuple[int, int]] = {
    "width": (10, 50),
    "height": (10, 50)
}

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
    width = 15
    height = 15

@dataclass
class Config:
    highscore_filename: str = "highscore.json"
    levels: list[Level] = [Level() for _ in range(10)]
    lives: int = 3
    pacgums: int = 42
    points_per_pacgum: int = 10
    points_per_super_pacgum: int = 50
    points_per_ghost: int = 200
    seed: int = 42
    level_max_time: int = 90
    cheat_mode: bool = False

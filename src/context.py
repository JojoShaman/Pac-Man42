from dataclasses import dataclass
from pathlib import Path
from typing import Any

import pygame

from .config import Config


@dataclass
class GameResult:
    """Outcome of the last game, read by the end screen."""

    score: int
    won: bool
    # grid: Grid


@dataclass
class Context:
    """Shared state: config, display objects, highscores and last result."""

    config: Config
    font: pygame.font.Font
    screen: pygame.Surface
    file_path: Path
    highscores: list[dict[str, Any]]
    backdrop: pygame.Surface
    result: GameResult

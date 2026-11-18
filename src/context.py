from dataclasses import dataclass
from .config import Config
import pygame
from pathlib import Path
from typing import Any
from .maze.grid import Grid
import pygame


@dataclass
class GameResult:
    score: int
    won: bool
    # grid: Grid


@dataclass
class Context:
    config: Config
    font: pygame.font.Font
    screen: pygame.Surface
    file_path: Path
    highscores: list[dict[str, Any]]
    backdrop: pygame.Surface
    result: GameResult

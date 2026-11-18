from dataclasses import dataclass
from .config import Config
from .maze.grid import Grid
import pygame


@dataclass
class GameResult:
    score: int
    won: bool
    grid: Grid


@dataclass
class Context:
    config: Config
    screen: pygame.Surface
    font: pygame.font.Font
    result: GameResult | None = None

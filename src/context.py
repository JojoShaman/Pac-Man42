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
    font: pygame.font.Font
    screen: pygame.Surface
    result: GameResult | None = None

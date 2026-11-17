from dataclasses import dataclass
from .config import Config
from .maze.grid import Grid


@dataclass
class GameResult:
    score: int
    won: bool
    grid: Grid


@dataclass
class Context:
    config: Config
    result: GameResult | None = None

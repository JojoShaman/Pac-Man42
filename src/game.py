from .direction import Direction
from .entities import Player
from .maze.maze_loader import process_maze
from .maze.grid import Grid
from .context import Context
from .config import Level
import random

class Intents:
    def __init__(self) -> None:
        self.direction: Direction | None = None
        self.next_lvl: bool = False

class Game:
    def __init__(self) -> None:
        self.grid: Grid = process_maze(15, 15, 42)
        self.player: Player = Player(
            self.grid.width // 2, self.grid.height // 2,
            Direction.S, 4)

    def update(self, dt: float, intents: Intents) -> None:
        self.player.set_wanted_direction(intents.direction)
        self.player.update(dt, self.grid)
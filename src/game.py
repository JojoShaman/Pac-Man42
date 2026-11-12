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
    def __init__(self, context: Context) -> None:
        self.context: Context = context
        self.levels: list[Level] = context.config.levels
        self.current_lvl: int = 0
        self.seed: int = context.config.seed
        self.grid: Grid = self.get_grid()
        self.pacgums: list[tuple[int, int]] = self.init_pacgums()
        self.score: int = 0
        self.player: Player = Player(
            self.grid.width // 2, self.grid.height // 2,
            Direction.S, 4)

    def get_grid(self) -> Grid:
        return process_maze(
            self.levels[self.current_lvl].width,
            self.levels[self.current_lvl].height,
            self.seed)


    def init_pacgums(self) -> list[tuple[int, int]]:
        pacgums: list[tuple[int, int]] = []
        w = self.levels[self.current_lvl].width
        h = self.levels[self.current_lvl].height
        for _ in range(self.context.config.pacgums):
            while True:
                x, y = (random.randint(0, w - 1), random.randint(0, h - 1))
                cell = self.grid.cells[y][x]
                if not all(cell.has_wall(wall) for wall in [
                    Direction.N, Direction.E, Direction.S, Direction.W]):
                    break
            pacgums.append((x, y))
        return pacgums
    def update(self, dt: float, intents: Intents) -> None:
        self.player.set_wanted_direction(intents.direction)
        self.player.update(dt, self.grid)
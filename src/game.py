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
        self.score: int = 0
        self.player: Player = Player(
            self.grid.width // 2, self.grid.height // 2,
            Direction.S, 4)
        self.pacgums: list[tuple[int, int]] = self.init_pacgums()

    def get_grid(self) -> Grid:
        return process_maze(
            self.levels[self.current_lvl].width,
            self.levels[self.current_lvl].height,
            self.seed)

    def init_pacgums(self) -> list[tuple[int, int]]:
        candidates = self._pacgum_candidates()
        count = min(self.context.config.pacgums, len(candidates))
        if count < self.context.config.pacgums:
            print(f"pacgums clamped {count} (number of free cells)")
        return random.sample(candidates, count)

    def _pacgum_candidates(self) -> list[tuple[int, int]]:
        """Open cells where a pacgum may be placed."""
        w, h = self.grid.width, self.grid.height
        excluded = {
            (0, 0), (w - 1, 0), (0, h - 1), (w - 1, h - 1),
            (self.player.x, self.player.y)
        }
        return [(x, y)
                for y in range(h) for x in range(w)
                if self.grid.cells[y][x].walls != 15
                and (x, y) not in excluded]

    def next_level(self) -> None:
        if self.current_lvl < 9:
            self.current_lvl += 1
            self.seed = random.getrandbits(32)
            self.grid = self.get_grid()

    def increase_score(self) -> None:
        player_pos: tuple[float, float] = (self.player.x, self.player.y)
        if player_pos in self.pacgums:
            self.score += self.context.config.points_per_pacgum
            self.pacgums.remove((
                int(player_pos[0]),
                int(player_pos[1])))

    def update(self, dt: float, intents: Intents) -> None:
        if intents.next_lvl:
            self.next_level()
        self.player.set_wanted_direction(intents.direction)
        self.player.update(dt, self.grid)
        self.increase_score()

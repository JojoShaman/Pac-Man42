from .direction import Direction
from .entities import Player, Blinky, Pinky, Inky, Ghost
from .maze.maze_loader import process_maze
from .maze.grid import Grid
from .context import Context
from .config import Level
import random

class Intents:
    def __init__(self) -> None:
        self.direction: Direction | None = None
        self.next_lvl: bool = False
        self.previous_lvl: bool = False


class Game:
    def __init__(self, context: Context) -> None:
        self.context: Context = context
        self.levels: list[Level] = context.config.levels
        self.lives: int = context.config.lives
        self.time_left: float = context.config.level_max_time
        self.current_lvl: int = 0
        self.seed: list[int | None] = (
            [context.config.seed] + [None] * (len(self.levels) - 1)
        )
        self.grid: Grid = self.get_grid()
        self.score: int = 0
        self.player: Player = self.init_player()
        self.blinky: Blinky = Blinky(0, 0, Direction.E, 3, self.player)
        self.pinky: Pinky = Pinky(self.grid.width - 1, 0, Direction.W, 3, self.player)
        self.inky: Inky = Inky(0, self.grid.height - 1, Direction.S, 3, self.player, self.blinky)
        self.pacgums: list[tuple[int, int]] = self.init_pacgums()
        self.super_pacgums: list[tuple[int, int]] = self.init_super_pacgums()
        self.seed_random: random.Random = random.Random()
        self.start_timer: float = 3

    def get_grid(self) -> Grid:
        return process_maze(
            self.levels[self.current_lvl].width,
            self.levels[self.current_lvl].height,
            self.get_seed())

    def get_seed(self) -> int:
        seed = self.seed[self.current_lvl]
        if seed is None:
            seed = self.seed_random.getrandbits(32) # random from new_instance separated from global generator
            self.seed[self.current_lvl] = seed
        return seed

    def init_pacgums(self) -> list[tuple[int, int]]:
        candidates = self._pacgum_candidates()
        count = min(self.context.config.pacgums, len(candidates))
        if count < self.context.config.pacgums:
            print(f"pacgums clamped {count} (number of free cells)")
        return random.sample(candidates, count)

    def init_super_pacgums(self) -> list[tuple[int, int]]:
        return self._corners()

    def init_player(self) -> Player:
        x, y = self.get_init_player_pos()
        return Player(x, y, Direction.S, 4)

    def set_player_pos(self) -> None:
        self.player.x, self.player.y = self.get_init_player_pos()

    def get_init_player_pos(self) -> tuple[float, float]:
        x: float = 0
        y: float = self.grid.height // 2
        if not self.grid.width % 2:
            x = self.grid.width // 2 - 1
        else:
            x = self.grid.width // 2
        return x, y

    def reset_ghost_pos(self) -> None:
        ghosts: list[Ghost] = [self.blinky, self.pinky, self.inky]
        for i, (x, y) in enumerate(self._corners()[:3]):
            ghosts[i].x = x
            ghosts[i].y = y

    def _corners(self) -> list[tuple[int, int]]:
        """Return the 4 corner positions of the grid."""
        w, h = self.grid.width, self.grid.height
        return [(0, 0), (w - 1, 0), (0, h - 1), (w - 1, h - 1)]

    def _pacgum_candidates(self) -> list[tuple[int, int]]:
        w, h = self.grid.width, self.grid.height
        excluded: set[tuple[int, int]] = {
            *self._corners(),
            (round(self.player.x), round(self.player.y))} # had to call and depile self._corners in order to obtain them and added type hiny
        return [(x, y)
                for y in range(h) for x in range(w)
                if self.grid.cells[y][x].walls != 15
                and (x, y) not in excluded]


    def increase_score(self) -> None:
        player_pos: tuple[float, float] = (
            self.player.x, self.player.y)
        if player_pos in self.pacgums:
            self.score += self.context.config.points_per_pacgum
            self.pacgums.remove((
                int(player_pos[0]),
                int(player_pos[1])))
        elif player_pos in self.super_pacgums:
            self.score += self.context.config.points_per_super_pacgum
            self.super_pacgums.remove((
                int(player_pos[0]),
                int(player_pos[1])))

    def new_level(self, intent: Intents, dt: float) -> float:
        def _wait() -> float:
            if self.start_timer > 0:
                self.start_timer -= dt
                return 0
            return dt
        skips: list[bool] = [
            intent.next_lvl, intent.previous_lvl,
            len(self.pacgums) == False
            ]
        if any(skips):
            if skips[0] or skips[2]:
                self.next_level()
            elif skips[1]:
                self.previous_level()
            self.reset_ghost_pos()
            self.start_timer = 3
        return _wait()

    def next_level(self) -> None:
        if self.current_lvl < 9:
            self.current_lvl += 1
            self.load_level()

    def previous_level(self) -> None:
        if self.current_lvl > 0:
            self.current_lvl -= 1
            self.load_level()

    def load_level(self) -> None:
        self.grid = self.get_grid()
        self.pacgums = self.init_pacgums()
        self.super_pacgums = self.init_super_pacgums()
        self.set_player_pos()
        self.player.direction = Direction.S

    def update(self, dt: float, intents: Intents) -> None:
        dt = self.new_level(intents, dt)
        self.player.set_wanted_direction(intents.direction)
        self.player.update(dt, self.grid)
        self.blinky.update(dt, self.grid)
        self.pinky.update(dt, self.grid)
        self.inky.update(dt, self.grid)
        self.increase_score()
        self.time_left -= dt

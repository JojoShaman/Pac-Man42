from .direction import Direction
from .entities import Player, Blinky, Pinky, Inky, Clyde, Ghost, GhostMode, Entity
from .maze.maze_loader import process_maze
from .maze.grid import Grid
from .context import Context
from .config import Level
import random
from typing import Callable

class Intents:
    def __init__(self) -> None:
        self.direction: Direction | None = None
        self.next_lvl: bool = False
        self.previous_lvl: bool = False

class Game:
    GHOST_INIT_POS: dict[type[Ghost], tuple[int, int]] = {}
    GHOST_INIT_DIRECTION: dict[type[Ghost], Direction] = {
        Blinky: Direction.E,
        Pinky: Direction.W,
        Inky: Direction.E,
        Clyde: Direction.W
    }
    GHOST_CLASS: dict[str, type[Ghost]] = {
        "blinky": Blinky,
        "pinky": Pinky,
        "inky": Inky,
        "clyde": Clyde}

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
        self.ghosts: dict[str, Ghost] = {}
        self.init_ghosts()
        self.pacgums: list[tuple[int, int]] = self.init_pacgums()
        self.super_pacgums: list[tuple[int, int]] = self.init_super_pacgums()
        self.seed_random: random.Random = random.Random()
        self.start_timer: float = 3
        self.restart_level: bool = False

    def ghost_pos_init(self) -> None:
        corners: list[tuple[int, int]]= self._corners()
        for i, (_, ghost) in enumerate(self.GHOST_CLASS.items()):
            self.GHOST_INIT_POS[ghost] = corners[i]

    def init_ghosts(self) -> None:
        self.ghost_pos_init()
        def _init_blinky() -> Blinky:
            x, y = self.GHOST_INIT_POS[Blinky]
            direction = self.GHOST_INIT_DIRECTION[Blinky]
            return Blinky(x, y, direction, 3, self.player)

        def _init_pinky() -> Pinky:
            x, y = self.GHOST_INIT_POS[Pinky]
            direction = self.GHOST_INIT_DIRECTION[Pinky]
            return Pinky(x, y, direction, 3, self.player)

        def _init_inky() -> Inky:
            x, y = self.GHOST_INIT_POS[Inky]
            direction = self.GHOST_INIT_DIRECTION[Inky]
            return Inky(x, y, direction, 3, self.player, self.ghosts["blinky"])

        def _init_clyde() -> Clyde:
            x, y = self.GHOST_INIT_POS[Clyde]
            direction = self.GHOST_INIT_DIRECTION[Clyde]
            return Clyde(x, y, direction, 3, self.player, self.grid)

        g: dict[str, Callable[[], Blinky | Pinky | Inky | Clyde]] = {
            "blinky": _init_blinky,
            "pinky": _init_pinky,
            "inky": _init_inky,
            "clyde": _init_clyde
        }
        for ghost, init in g.items():
            self.ghosts[ghost] = init()

    def get_grid(self) -> Grid:
        return process_maze(
            self.levels[self.current_lvl].width,
            self.levels[self.current_lvl].height,
            self.get_seed())

    def get_seed(self) -> int:
        seed = self.seed[self.current_lvl]
        if seed is None:
            seed = self.seed_random.getrandbits(32)
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


    def _corners(self) -> list[tuple[int, int]]:
        """Return the 4 corner positions of the grid."""
        w, h = self.grid.width, self.grid.height
        return [(0, 0), (w - 1, 0), (0, h - 1), (w - 1, h - 1)]

    def _pacgum_candidates(self) -> list[tuple[int, int]]:
        w, h = self.grid.width, self.grid.height
        excluded: set[tuple[int, int]] = {
            *self._corners(),
            (round(self.player.x), round(self.player.y))}
        return [(x, y)
                for y in range(h) for x in range(w)
                if self.grid.cells[y][x].walls != 15
                and (x, y) not in excluded]

    def super_gum_activate(self) -> None:
        for ghost in self.ghosts.values():
            if ghost.mode == GhostMode.CHASE:
                ghost.mode = GhostMode.EDIBLE
                ghost.edible_delay = 30
                ghost.speed = 2
                ghost.direction = ghost.direction.opposite
    
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
            self.super_gum_activate()
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
        if any(skips) or self.restart_level:
            if self.restart_level:
                self.restart_lvl()
            if skips[0] or skips[2]:
                self.next_level()
            elif skips[1]:
                self.previous_level()
            self.init_ghosts()
            self.load_level()
            self.start_timer = 3
        return _wait()

    def next_level(self) -> None:
        if self.current_lvl < 9:
            self.current_lvl += 1

    def previous_level(self) -> None:
        if self.current_lvl > 0:
            self.current_lvl -= 1

    def restart_lvl(self) -> None:
        self.restart_level = False

    def load_level(self) -> None:
        self.grid = self.get_grid()
        self.pacgums = self.init_pacgums()
        self.super_pacgums = self.init_super_pacgums()
        self.set_player_pos()
        self.player.direction = Direction.S
        self.player.buffer_input = Direction.S

    def collides(self, a: Entity, b: Entity) -> bool:
        return ((a.x - b.x)**2 + (a.y - b.y)**2) < 0.25**2

    def update_ghosts(self, dt: float) -> None:
        for ghost in self.ghosts.values():
            if ghost.mode in (GhostMode.WAITING, GhostMode.EATEN):
                self.update_waiting_ghost(ghost, dt)
                if ghost.mode == GhostMode.EATEN:
                    if ghost.spawn_delay < 5:
                        ghost.update(dt, self.grid)
                continue
            if ghost.mode == GhostMode.EDIBLE:
                self.update_edible_ghost(ghost, dt)
            ghost.update(dt, self.grid)

    def update_waiting_ghost(self, ghost: Ghost, dt: float) -> None:
        if ghost.mode == GhostMode.WAITING:
            ghost.start_delay -= dt
            if ghost.start_delay <= 0:
                ghost.mode = GhostMode.CHASE
        else:
            ghost.spawn_delay -= dt
            if ghost.spawn_delay <= 0:
                ghost.mode = GhostMode.CHASE
                ghost.speed = 3

    def update_edible_ghost(self, ghost: Ghost, dt: float) -> None:
        ghost.edible_delay -= dt
        if ghost.edible_delay <= 0:
            ghost.mode = GhostMode.CHASE
            return
        if self.collides(self.player, ghost):
            ghost.mode = GhostMode.EATEN
            ghost.x, ghost.y = ghost.init_pos
            ghost.edible_delay = 0
            ghost.spawn_delay = 7
            self.score += self.context.config.points_per_ghost

    def update(self, dt: float, intents: Intents) -> None:
        for g in self.ghosts.values():
            if g.mode == GhostMode.CHASE:
                if self.collides(self.player, g):
                    self.lives -= 1
                    self.restart_level = True
        dt = self.new_level(intents, dt)
        self.player.set_wanted_direction(intents.direction)
        self.player.update(dt, self.grid)
        self.update_ghosts(dt)
        self.increase_score()
        self.time_left -= dt

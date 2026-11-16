from .entity import Entity
from .player import Player
from ..direction import Direction, priority
from ..maze.grid import Grid
from enum import Enum
from abc import abstractmethod
import random

class GhostMode(Enum):
    WAITING = 1
    CHASE = 2
    EDIBLE = 3
    EATEN = 4


class Ghost(Entity):
    def __init__(self,
                 x: float,
                 y: float,
                 direction: Direction,
                 speed: int,
                 player: Player) -> None:
        self.player: Player = player
        self.name: str = ""
        self.mode: GhostMode = GhostMode.WAITING
        self.init_pos: tuple[float, float] = (x, y)
        self.start_delay: float = 0
        self.spawn_delay: float = 0
        self.edible_delay: float = 0
        super().__init__(x, y, direction, speed)

    @abstractmethod
    def get_target(self) -> tuple[float, float]:
        return 0, 0

    def choose_direction(self, grid) -> Direction:
        tx, ty = self.get_target()
        direction: Direction = self.direction
        candidates: list[Direction] = []
        best_dist = float('inf')
        current = grid.cells[int(self.y)][int(self.x)]
        for d in priority():
            if (current.has_wall(d) or
                d == self.direction.opposite):
                continue
            candidates.append(d)
        if candidates:
            for candidate in candidates:
                off_x, off_y = candidate.offset
                dx, dy = (off_x + self.x, off_y + self.y)
                dist = (dx - tx)**2 + (dy - ty)**2
                if self.mode == GhostMode.EDIBLE:
                    dist = -dist
                if dist < best_dist:
                    best_dist = dist
                    direction = candidate
        else:
            direction = self.direction.opposite
        return direction

class Blinky(Ghost):
    def __init__(self, x, y, direction, speed, player) -> None:
        super().__init__(x, y, direction, speed, player)
        self.name = "blinky"
        self.start_delay = 0


    def chase(self) -> tuple[float, float]:
        return self.player.x, self.player.y

    def get_target(self):
        return self.chase()

class Pinky(Ghost):
    def __init__(self, x, y, direction, speed, player) -> None:
        super().__init__(x, y, direction, speed, player)
        self.name = "pinky"
        self.start_delay = 3

    def chase(self) -> tuple[float, float]:
        off_x, off_y = self.player.direction.offset
        target_x = self.player.x + 4 * off_x
        target_y = self.player.y + 4 * off_y
        return target_x, target_y

    def get_target(self):
        return self.chase()

class Inky(Ghost):
    def __init__(self, x, y, direction, speed, player, blinky) -> None:
        super().__init__(x, y, direction, speed, player)
        self.blinky: Blinky = blinky
        self.name = "inky"
        self.start_delay = 7

    def chase(self) -> tuple[float, float]:
        off_x, off_y = self.player.direction.offset
        pivot_x = self.player.x + 2 * off_x
        pivot_y = self.player.y + 2 * off_y
        bx = self.blinky.x
        by = self.blinky.y
        target_x = pivot_x + (pivot_x - bx)
        target_y = pivot_y + (pivot_y - by)
        return target_x, target_y

    def get_target(self):
        return self.chase()

class Clyde(Ghost):
    FLEE_RATIO = 8 / 28
    def __init__(self, x, y, direction, speed, player, grid) -> None:
        super().__init__(x, y, direction, speed, player)
        self.grid: Grid = grid
        self.min_size: int = min(self.grid.width, self.grid.height)
        self.flee_threshold_sq: float = (self.min_size * self.FLEE_RATIO)**2
        self.name = "clyde"
        self.start_delay = 12

    def chase(self) -> tuple[float, float]:
            _dist = (self.x - self.player.x)**2 + (self.y - self.player.y)**2
            if _dist < self.flee_threshold_sq:
                return self.init_pos
            return self.player.x, self.player.y
    
    def get_target(self):
        return self.chase()

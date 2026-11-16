from .entity import Entity
from .player import Player
from ..direction import Direction
from ..maze.grid import Grid
from enum import Enum
from abc import abstractmethod

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
                 player: Player,
                 name: str) -> None:
        self.player: Player = player
        self.mode: GhostMode = GhostMode.WAITING
        self.name: str = name
        super().__init__(x, y, direction, speed)

    @abstractmethod
    def get_target(self) -> tuple[float, float]:
        return 0, 0

    def choose_direction(self, grid) -> Direction:
        tx, ty = self.get_target()
        direction: Direction = self.direction
        best_dist = float('inf')
        current = grid.cells[int(self.y)][int(self.x)]
        for d in Direction:
            off_x, off_y = d.offset
            dx, dy = (off_x + self.x, off_y + self.y)
            if current.has_wall(d):
                continue
            dist = (dx - tx)**2 + (dy - ty)**2
            if dist < best_dist:
                best_dist = dist
                direction = d
        return direction

class Blinky(Ghost):
    def __init__(self, x, y, direction, speed, player) -> None:
        super().__init__(x, y, direction, speed, player, "blinky")


    def chase(self) -> tuple[float, float]:
        return self.player.x, self.player.y

    def get_target(self):
        return self.chase()

class Pinky(Ghost):
    def __init__(self, x, y, direction, speed, player) -> None:
        super().__init__(x, y, direction, speed, player, "pinky")

    def chase(self) -> tuple[float, float]:
        off_x, off_y = self.player.direction.offset
        target_x = self.player.x + 4 * off_x
        target_y = self.player.y + 4 * off_y
        return target_x, target_y

    def get_target(self):
        return self.chase()

class Inky(Ghost):
    def __init__(self, x, y, direction, speed, player, blinky) -> None:
        self.blinky: Blinky = blinky
        super().__init__(x, y, direction, speed, player, "inky")

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
    def __init__(self, x, y, direction, speed, player) -> None:
        super().__init__(x, y, direction, speed, player, "clyde")

    def choose_direction(self, grid):
        return super().choose_direction(grid)

    def get_target(self):
        return super().get_target()

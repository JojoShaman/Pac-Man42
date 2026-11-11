from abc import *
from ..direction import *
from ..maze.grid import Grid
import math
from typing import Callable


class Entity(ABC):
    def __init__(
            self,
            x: float, y: float,
            direction: Direction,
            speed: float) -> None:
        self.x = x
        self.y = y
        self.direction: Direction = direction
        self.speed: float = speed

    @abstractmethod
    def choose_direction(self, grid: Grid) -> Direction:
        ...

    def update(self, dt: float, grid: Grid) -> None:
        distance = self.speed * dt
        dx, dy = self.direction.offset
        rnd: Callable[[float], int] = (
            math.floor if dx > 0 or dy > 0 else math.ceil)
        if int(self.x) == self.x and int(self.y) == self.y:
            if grid.cells[int(self.y)][int(self.x)].has_wall(self.direction):
                self.direction = self.choose_direction(grid)
                return
        old_pos = (rnd(self.x), rnd(self.y))
        self.x += dx * distance
        self.y += dy * distance
        new_pos = (rnd(self.x), rnd(self.y))
        if new_pos[0] != old_pos[0] or new_pos[1] != old_pos[1]:
            self.x = new_pos[0]
            self.y = new_pos[1]
            self.direction = self.choose_direction(grid)

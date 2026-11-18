import math
from abc import ABC, abstractmethod
from typing import Callable

from ..direction import Direction
from ..maze.grid import Grid


class Entity(ABC):
    """A moving entity with continuous coordinates (in cells)."""

    def __init__(
            self,
            x: float, y: float,
            direction: Direction,
            speed: float) -> None:
        """Place the entity; speed is in cells per second."""
        self.x = x
        self.y = y
        self.direction: Direction = direction
        self.speed: float = speed
        self.travelled: float = 0

    @abstractmethod
    def choose_direction(self, grid: Grid) -> Direction:
        """Return the direction to take at a cell centre."""
        ...

    def update(self, dt: float, grid: Grid) -> None:
        """Move by speed * dt, snapping to a cell centre when crossing it."""
        distance = self.speed * dt
        dx, dy = self.direction.offset
        rnd: Callable[[float], int] = (
            math.floor if dx > 0 or dy > 0 else math.ceil)
        if int(self.x) == self.x and int(self.y) == self.y:
            if grid.cells[int(self.y)][int(self.x)].has_wall(self.direction):
                self.direction = self.choose_direction(grid)
                self.travelled = 0
                return
        old_pos = (rnd(self.x), rnd(self.y))
        self.x += dx * distance
        self.y += dy * distance
        new_pos = (rnd(self.x), rnd(self.y))
        if new_pos[0] != old_pos[0] or new_pos[1] != old_pos[1]:
            self.x = new_pos[0]
            self.y = new_pos[1]
            self.direction = self.choose_direction(grid)
        self.travelled += distance

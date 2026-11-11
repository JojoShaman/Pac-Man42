from .entity import Entity
from ..direction import *
from ..maze.grid import *

class Player(Entity):
    def __init__(self,
                 x: float, y: float,
                 direction: Direction,
                 speed: int) -> None:
        super().__init__(x, y, direction, speed)
        self.buffer_input: Direction = direction

    def choose_direction(self, grid: Grid) -> Direction:
        cell = grid.cells[int(self.y)][int(self.x)]
        if not cell.has_wall(self.buffer_input):
            return self.buffer_input
        return self.direction

    def set_wanted_direction(self, direction: Direction | None) -> None:
        if direction is not None:
            if direction == self.direction.opposite:
                self.direction = direction
            self.buffer_input = direction
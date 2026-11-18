from ..direction import Direction
from ..maze.grid import Grid
from .entity import Entity


class Player(Entity):
    """Pac-Man: follows the buffered direction as soon as it is free."""

    def __init__(self,
                 x: float, y: float,
                 direction: Direction,
                 speed: int) -> None:
        """Create the player with an empty input buffer."""
        super().__init__(x, y, direction, speed)
        self.buffer_input: Direction = direction
        self.immortal: bool = False

    def choose_direction(self, grid: Grid) -> Direction:
        """Take the buffered direction if there is no wall, else go on."""
        cell = grid.cells[int(self.y)][int(self.x)]
        if not cell.has_wall(self.buffer_input):
            return self.buffer_input
        return self.direction

    def set_wanted_direction(self, direction: Direction | None) -> None:
        """Buffer the wanted direction; a U-turn is applied immediately."""
        if direction is not None:
            if direction == self.direction.opposite:
                self.direction = direction
            self.buffer_input = direction

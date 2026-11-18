from dataclasses import dataclass

from ..direction import Direction


@dataclass(frozen=True)
class Cell:
    """One maze cell: wall bitmask (N=1, E=2, S=4, W=8) and position."""

    walls: int
    x: int
    y: int

    def has_wall(self, d: Direction) -> bool:
        """Return True if there is a wall on side d."""
        return bool(self.walls & d)


class Grid:
    """Rectangular matrix of cells, indexed cells[y][x]."""

    def __init__(self, cells: list[list[Cell]]) -> None:
        """Store the cells and deduce width and height."""
        self.cells = cells
        self.height, self.width = len(cells), len(cells[0])

    def cell(self, x: int, y: int) -> Cell:
        """Return the cell at column x, row y."""
        return self.cells[y][x]

    def is_consistent(self) -> bool:
        """Check that neighbouring cells agree on their shared wall."""
        for y in range(self.height):
            for x in range(self.width):
                for d in (Direction.S, Direction.E):
                    dx, dy = d.offset
                    nx, ny = (x + dx, y + dy)
                    if nx < self.width and ny < self.height:
                        a = self.cell(x, y).has_wall(d)
                        b = self.cell(nx, ny).has_wall(d.opposite)
                        if a != b:
                            return False
        return True

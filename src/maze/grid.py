from dataclasses import dataclass
from src.direction import Direction


@dataclass(frozen=True)
class Cell:
    walls: int
    x: int
    y: int

    def has_wall(self, d: Direction) -> bool:
        return bool(self.walls & d)


class Grid:
    def __init__(self, cells: list[list[Cell]]) -> None:
        self.cells = cells
        self.height, self.width = len(cells), len(cells[0])

    def cell(self, x: int, y: int) -> Cell:
        return self.cells[y][x]

    def is_consistent(self) -> bool:
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

from dataclasses import dataclass
from ..maze.direction import Direction


@dataclass(frozen=True)
class Cell:
    walls: int

    def has_wall(self, d: Direction) -> bool:
        return bool(self.walls & d)


class Grid:
    def __init__(self, cells: list[list[Cell]]) -> None:
        self.cells = cells
        self.height, self.width = len(cells), len(cells[0])

    def cell(self, x: int, y: int) -> Cell:
        return self.cells[y][x]

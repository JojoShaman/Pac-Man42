from mazegenerator import MazeGenerator
from .grid import Cell, Grid


class MazeError(Exception):
    ...


def process_maze(width: int, height: int, seed: int) -> Grid:
    gen = MazeGenerator(size=(width, height), perfect=False, seed=seed)
    # print(vars(gen))
    raw = gen.maze
    # print(raw)
    return Grid(
        [[Cell(walls=(v & 15), x=x, y=y) for x, v in enumerate(row)]
         for y, row in enumerate(raw)])

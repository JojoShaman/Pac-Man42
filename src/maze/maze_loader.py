from mazegenerator import MazeGenerator
from .grid import Cell, Grid


class MazeError(Exception):
    ...


def process_maze(width: int, height: int, seed: int) -> Grid:
    gen = MazeGenerator(size=(width, height), perfect=False, seed=seed)
    print(vars(gen))
    raw = gen.maze
    print(raw)
    return Grid([[Cell(v & 15) for v in row] for row in raw])

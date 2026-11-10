from mazegenerator import MazeGenerator
from .grid import Cell, Grid

MIN_SIZE, MAX_SIZE = 10, 50


class MazeError(Exception):
    ...


def process_maze(width: int, height: int, seed: int) -> Grid:
<<<<<<< HEAD
    """Process the maze from the MazeGenerator """
    try:
        seed = max(1, seed)
        gen = MazeGenerator(size=(width, height), perfect=False, seed=seed)
        raw = gen.maze
    except Exception as e:
        raise MazeError(f"Maze Generation failed: {e}")
    _validate_raw(raw, width, height)
    grid = Grid([[Cell(v & 15) for v in row] for row in raw])
    if not grid.is_consistent():
        raise MazeError("Inconsistent walls between neighbouring cells")
    return grid


def _validate_raw(raw: list[list[int]], width: int, height: int) -> None:
    """Raise MazeError if raw is not a sane maze."""
    if len(raw) != height or any(len(row) != width for row in raw):
        raise MazeError("unexpected maze dimensions")
    if not all(isinstance(v, int) and 0 <= v <= 15
               for row in raw for v in row):
        raise MazeError("cell value out of range 0-15")
=======
    gen = MazeGenerator(size=(width, height), perfect=False, seed=seed)
    # print(vars(gen))
    raw = gen.maze
    # print(raw)
    return Grid(
        [[Cell(walls=(v & 15), x=x, y=y) for x, v in enumerate(row)]
         for y, row in enumerate(raw)])
>>>>>>> 990614025fa8bcd9b30db308f3718981a3a1ff00

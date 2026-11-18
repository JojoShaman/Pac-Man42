from mazegenerator import MazeGenerator  # type: ignore[import-untyped]

from .grid import Cell, Grid

MIN_SIZE, MAX_SIZE = 10, 50


class MazeError(Exception):
    """Raised when the maze cannot be generated or is invalid."""

    ...


def process_maze(width: int, height: int, seed: int) -> Grid:
    """Generate a maze and return it as a validated Grid."""
    try:
        seed = max(1, seed)
        gen = MazeGenerator(size=(width, height), perfect=False, seed=seed)
        raw = gen.maze
    except Exception as e:
        raise MazeError(f"Maze Generation failed: {e}")
    _validate_raw(raw, width, height)
    grid = Grid(
        [[Cell(v & 15, x, y) for x, v in enumerate(row)]
         for y, row in enumerate(raw)])
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

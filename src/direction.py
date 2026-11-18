from enum import IntFlag


class Direction(IntFlag):
    """A cardinal direction, usable as a wall bitmask."""

    N = 1
    E = 2
    S = 4
    W = 8

    @property
    def offset(self) -> tuple[int, int]:
        """Return the (dx, dy) step of this direction."""
        return {Direction.N: (0, -1), Direction.E: (1, 0),
                Direction.S: (0, 1), Direction.W: (-1, 0)}[self]

    @property
    def opposite(self) -> "Direction":
        """Return the opposite direction."""
        return {Direction.N: Direction.S, Direction.S: Direction.N,
                Direction.E: Direction.W, Direction.W: Direction.E}[self]


def priority() -> list["Direction"]:
    """Return the tie-break order used by ghosts: up, left, down, right."""
    return [Direction.N, Direction.W, Direction.S, Direction.E]

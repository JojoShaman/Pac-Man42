from enum import IntFlag


class Direction(IntFlag):
    N = 1
    E = 2
    S = 4
    W = 8

    @property
    def offset(self) -> tuple[int, int]:
        return {Direction.N: (0, -1), Direction.E: (1, 0),
                Direction.S: (0, 1), Direction.W: (-1, 0)}[self]

    @property
    def opposite(self) -> "Direction":
        return {Direction.N: Direction.S, Direction.S: Direction.N,
                Direction.E: Direction.W, Direction.W: Direction.E}[self]

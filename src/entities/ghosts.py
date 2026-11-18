from enum import Enum
from abc import abstractmethod

from ..direction import Direction, priority
from ..maze.grid import Grid
from .entity import Entity
from .player import Player


class GhostMode(Enum):
    """Behaviour mode of a ghost."""

    WAITING = 1
    CHASE = 2
    EDIBLE = 3
    EATEN = 4


class Ghost(Entity):
    """Base ghost: greedy movement towards a target (away if edible)."""

    def __init__(self,
                 x: float,
                 y: float,
                 direction: Direction,
                 speed: int,
                 player: Player) -> None:
        """Create a waiting ghost; its corner is kept in init_pos."""
        self.player: Player = player
        self.name: str = ""
        self.mode: GhostMode = GhostMode.WAITING
        self.init_pos: tuple[float, float] = (x, y)
        self.start_delay: float = 0
        self.spawn_delay: float = 0
        self.edible_delay: float = 0
        super().__init__(x, y, direction, speed)

    @abstractmethod
    def get_target(self) -> tuple[float, float]:
        """Return the cell this ghost aims for in chase mode."""
        return 0, 0

    def choose_direction(self, grid: Grid) -> Direction:
        """Pick the free direction closest to the target (no U-turn).

        Ties follow priority() (up, left, down, right). In edible mode the
        farthest one is chosen. A dead end allows the U-turn.
        """
        tx, ty = self.get_target()
        direction: Direction = self.direction
        candidates: list[Direction] = []
        best_dist = float('inf')
        current = grid.cells[int(self.y)][int(self.x)]
        for d in priority():
            if (current.has_wall(d) or
                    d == self.direction.opposite):
                continue
            candidates.append(d)
        if candidates:
            for candidate in candidates:
                off_x, off_y = candidate.offset
                dx, dy = (off_x + self.x, off_y + self.y)
                dist = (dx - tx)**2 + (dy - ty)**2
                if self.mode == GhostMode.EDIBLE:
                    dist = -dist
                if dist < best_dist:
                    best_dist = dist
                    direction = candidate
        else:
            direction = self.direction.opposite
        return direction


class Blinky(Ghost):
    """Red ghost: targets the player directly."""

    def __init__(self, x: float, y: float, direction: Direction,
                 speed: int, player: Player) -> None:
        """Create Blinky (leaves immediately)."""
        super().__init__(x, y, direction, speed, player)
        self.name = "blinky"
        self.start_delay = 0

    def chase(self) -> tuple[float, float]:
        """Target the player's position."""
        return self.player.x, self.player.y

    def get_target(self) -> tuple[float, float]:
        """Return the chase target."""
        return self.chase()


class Pinky(Ghost):
    """Pink ghost: targets 4 cells ahead of the player."""

    def __init__(self, x: float, y: float, direction: Direction,
                 speed: int, player: Player) -> None:
        """Create Pinky (leaves after 3 s)."""
        super().__init__(x, y, direction, speed, player)
        self.name = "pinky"
        self.start_delay = 3

    def chase(self) -> tuple[float, float]:
        """Target 4 cells in front of the player."""
        off_x, off_y = self.player.direction.offset
        target_x = self.player.x + 4 * off_x
        target_y = self.player.y + 4 * off_y
        return target_x, target_y

    def get_target(self) -> tuple[float, float]:
        """Return the chase target."""
        return self.chase()


class Inky(Ghost):
    """Cyan ghost: target mirrored from Blinky around a pivot ahead."""

    def __init__(self, x: float, y: float, direction: Direction,
                 speed: int, player: Player, blinky: Blinky) -> None:
        """Create Inky (leaves after 7 s)."""
        super().__init__(x, y, direction, speed, player)
        self.blinky: Blinky = blinky
        self.name = "inky"
        self.start_delay = 7

    def chase(self) -> tuple[float, float]:
        """Double the vector from Blinky to 2 cells ahead of the player."""
        off_x, off_y = self.player.direction.offset
        pivot_x = self.player.x + 2 * off_x
        pivot_y = self.player.y + 2 * off_y
        bx = self.blinky.x
        by = self.blinky.y
        target_x = pivot_x + (pivot_x - bx)
        target_y = pivot_y + (pivot_y - by)
        return target_x, target_y

    def get_target(self) -> tuple[float, float]:
        """Return the chase target."""
        return self.chase()


class Clyde(Ghost):
    """Orange ghost: chases from afar, retreats to its corner when close."""

    FLEE_RATIO = 8 / 28

    def __init__(self, x: float, y: float, direction: Direction,
                 speed: int, player: Player, grid: Grid) -> None:
        """Create Clyde (leaves after 12 s); flee distance scales with grid."""
        super().__init__(x, y, direction, speed, player)
        self.grid: Grid = grid
        self.min_size: int = min(self.grid.width, self.grid.height)
        self.flee_threshold_sq: float = (self.min_size * self.FLEE_RATIO)**2
        self.name = "clyde"
        self.start_delay = 12

    def chase(self) -> tuple[float, float]:
        """Target the player, or the home corner when too close."""
        _dist = (self.x - self.player.x)**2 + (self.y - self.player.y)**2
        if _dist < self.flee_threshold_sq:
            return self.init_pos
        return self.player.x, self.player.y

    def get_target(self) -> tuple[float, float]:
        """Return the chase target."""
        return self.chase()

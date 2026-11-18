from pygame import Surface
from pygame.event import Event
from pygame.locals import (
    K_DOWN, K_ESCAPE, K_LEFT, K_RIGHT, K_UP, KEYDOWN,
    K_a, K_d, K_n, K_p, K_q, K_s, K_w, K_z,
)

from ..context import Context, GameResult
from ..direction import Direction
from ..game import Game, Intents
from ..maze.grid import Grid
from ..rendering.render import draw_hud, render_maze
from ..rendering.sprites import (
    draw_ghost, draw_pacgums, draw_pacman,
    draw_start_timer, draw_super_pacgums,
)
from .state import State, StateName

_KEYS: dict[Direction, tuple[int, ...]] = {
    Direction.N: (K_UP, K_w, K_z),
    Direction.E: (K_RIGHT, K_d),
    Direction.S: (K_DOWN, K_s),
    Direction.W: (K_LEFT, K_a, K_q),
}

K_DIRECTION: dict[int, Direction] = {
    key: direction for direction, keys in _KEYS.items() for key in keys
}


class Playing(State):
    """The game screen."""

    def __init__(self, context: Context) -> None:
        """Create a new Game and the maze surface cache."""
        self.game: Game = Game(context)
        self.m_surf: Surface | None = None
        self.m_grid: Grid | None = None
        self.intents: Intents = Intents()
        self.context: Context = context
        self.pause: bool = False
        self.state: StateName = StateName.PLAYING

    def handle_input(self, events: list[Event]) -> None:
        """Translate the keys into intentions and cheat actions."""
        self.intents = Intents()
        for event in events:
            if event.type == KEYDOWN:
                if event.key in K_DIRECTION:
                    self.intents.direction = K_DIRECTION[event.key]
                elif event.key == K_n:
                    self.intents.next_lvl = True
                elif event.key == K_p:
                    self.intents.previous_lvl = True
                elif event.key == K_ESCAPE:
                    self.pause = True
                elif event.unicode == "+":
                    self.game.lives += 1
                elif event.unicode == "-":
                    self.game.lives -= 1
                elif event.unicode == "1":
                    self.game.player.immortal = (
                        not self.game.player.immortal)
                elif event.unicode == "2":
                    speed = self.game.player.speed
                    self.game.player.speed = 6 if speed == 4 else 4
                elif event.unicode == "3":
                    self.intents.freeze = (
                        not self.intents.freeze)

    def update(self, dt: float) -> StateName | None:
        """Update the game; go to the end screen or the pause menu."""
        self.game.update(dt, self.intents)
        self.context.backdrop = self.context.screen
        if self.game.lives == 0 or self.game.time_left <= 0:
            self.context.result = GameResult(self.game.score, False)
            return StateName.GAME_OVER
        elif self.game.current_lvl == 9 and len(self.game.pacgums) == 0:
            self.context.result = GameResult(self.game.score, True)
            return StateName.GAME_OVER
        if self.pause:
            self.pause = False
            if self.m_surf:
                return StateName.PAUSE
        return None

    def render(self) -> None:
        """Draw the maze (cached), the items, the entities and the HUD."""
        if (self.m_surf is None or self.m_grid is not self.game.grid):
            self.m_surf = render_maze(self.context.screen, self.game.grid)
            self.m_grid = self.game.grid
        if self.m_surf is not None:
            self.context.screen.blit(self.m_surf, (0, 0))
        draw_pacgums(self.context.screen, self.game.pacgums, self.game.grid)
        draw_super_pacgums(
            self.context.screen, self.game.super_pacgums, self.game.grid)
        draw_pacman(self.context.screen, self.game.player, self.game.grid)
        for ghost in self.game.ghosts.values():
            draw_ghost(self.context.screen, ghost, self.game.grid)
        if self.game.start_timer:
            draw_start_timer(self.context.screen, self.game)
        draw_hud(self.context.screen, self.game, self.context.font)

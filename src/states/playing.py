from .state import State
from pygame.event import Event
from ..rendering.render import (render_maze, draw_pacman, draw_pacgums,
                                draw_super_pacgums, draw_hud, draw_start_timer, draw_ghost)
from ..game import Game, Intents
from ..direction import Direction
from ..context import Context
from ..maze.grid import Grid
from pygame import Surface, font
from pygame.locals import (
    K_UP, K_DOWN, K_LEFT, K_RIGHT, K_ESCAPE, K_p,
    K_w, K_a, K_s, K_d, K_z, K_q, K_n, K_l, K_f, KEYDOWN
)
from .end import End

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
    def __init__(self, context: Context) -> None:
        self.game: Game = Game(context)
        self.m_surf: Surface | None = None
        self.m_grid: Grid | None = None
        self.intents: Intents = Intents()
        self.context: Context = context
        self.pause: bool = False
        self.state: State = self

    def handle_input(self, events: list[Event]) -> None:
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
                    self.game.player.immortal = self.game.player.immortal == False
                elif event.unicode == "2":
                    speed = self.game.player.speed
                    self.game.player.speed = 6 if speed == 4 else 4
                elif event.unicode == "3":
                    self.intents.freeze = self.intents.freeze == False

    def update(self, dt) -> State | None:
        self.game.update(dt, self.intents)
        self.context.last_state = self
        if self.game.lives == 0 or self.game.time_left <= 0:
            return End(self.context, self.game, False)
        elif self.game.current_lvl == 9 and len(self.game.pacgums) == 0:
            return End(self.context, self.game, True)
        if self.pause:
            from .pause import PauseMenu
            self.pause = False
            if self.m_surf:
                return PauseMenu(self.context)
        return self

    def render(self) -> None:
        if (self.m_surf is None or self.m_grid is not self.game.grid):
            self.m_surf = render_maze(self.context.screen, self.game.grid)
            self.m_grid = self.game.grid
        if self.m_surf is not None:
            self.context.screen.blit(self.m_surf, (0, 0))
        draw_pacgums(self.context.screen, self.game.pacgums, self.game.grid)
        draw_super_pacgums(self.context.screen, self.game.super_pacgums, self.game.grid)
        draw_pacman(self.context.screen, self.game.player, self.game.grid)
        for ghost in self.game.ghosts.values():
            draw_ghost(self.context.screen, ghost, self.game.grid)
        if self.game.start_timer:
            draw_start_timer(self.context.screen, self.game)
        draw_hud(self.context.screen, self.game, self.context.font)

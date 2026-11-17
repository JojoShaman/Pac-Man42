from .state import State, StateName
from pygame.event import Event
from ..rendering.render import (render_maze, draw_pacman, draw_pacgums,
                                draw_super_pacgums, draw_hud, draw_start_timer,
                                draw_ghost)
from ..game import Game, Intents
from ..direction import Direction
from ..context import Context, GameResult
from ..maze.grid import Grid
from pygame import Surface, font
from pygame.locals import (
    K_UP, K_DOWN, K_LEFT, K_RIGHT, K_p,
    K_w, K_a, K_s, K_d, K_z, K_q, K_n, K_l, KEYDOWN
)

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
        self.state: StateName = StateName.PLAYING

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
                elif event.key == K_l:
                    self.pause = True

    def update(self, dt) -> StateName | None:
        self.game.update(dt, self.intents)
        if self.game.lives == 0:
            game_result_defeat = GameResult(self.game.score, False,
                                            self.game.grid)
            self.context.result = game_result_defeat
            return StateName.GAME_OVER
        elif self.game.current_lvl == 9 and len(self.game.pacgums) == 0:
            game_result_victory = GameResult(self.game.score, True,
                                             self.game.grid)
            self.context.result = game_result_victory
            return StateName.GAME_OVER
        if self.pause:
            self.pause = False
            if self.m_surf:
                return StateName.PAUSE
        return None

    def render(self, screen: Surface, font: font.Font) -> None:
        if (self.m_surf is None or self.m_grid is not self.game.grid):
            self.m_surf = render_maze(screen, self.game.grid)
            self.m_grid = self.game.grid
        if self.m_surf is not None:
            screen.blit(self.m_surf, (0, 0))
        draw_pacgums(screen, self.game.pacgums, self.game.grid)
        draw_super_pacgums(screen, self.game.super_pacgums, self.game.grid)
        draw_pacman(screen, self.game.player, self.game.grid)
        for ghost in self.game.ghosts.values():
            draw_ghost(screen, ghost, self.game.grid)
        if self.game.start_timer:
            draw_start_timer(screen, self.game)
        draw_hud(screen, self.game, font)

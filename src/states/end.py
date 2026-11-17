from .state import State, StateName
from ..context import Context, GameResult
from ..maze.grid import Grid
from pygame.event import Event
from pygame import Surface, font
from pygame.locals import (
    K_RETURN, K_BACKSPACE, K_SPACE, KEYDOWN,
)
from ..rendering.render import draw_end, render_maze


class End(State):
    def __init__(self, context: Context, result: GameResult) -> None:
        self.context = context
        self.state: StateName | None = StateName.GAME_OVER
        self.name: str = ""
        self.score: int = result.score
        self.win: bool = result.won
        self.grid: Grid = result.grid
        self.elapsed: float = 0.0
        self.maze_surf: Surface | None = None

    def handle_input(self, events: list[Event]) -> None:
        for event in events:
            if event.type != KEYDOWN:
                continue
            if event.key == K_BACKSPACE:
                self.name = self.name[:-1]
            elif event.key in (K_RETURN, K_SPACE):
                self.state = StateName.MENU
            elif event.unicode:
                char: str = event.unicode
                self.name += char if char.isascii() else ""

    def update(self, dt: float) -> StateName | None:
        self.elapsed += dt
        return self.state

    def render(self, screen: Surface, font: font.Font) -> None:
        if self.maze_surf is None:
            self.maze_surf = render_maze(screen, self.grid)
        fade = self.elapsed / 2.5
        draw_end(screen, self.maze_surf, self.score, self.win, fade, self.name,
                 font)

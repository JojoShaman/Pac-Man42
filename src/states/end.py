from .state import State, StateName
from ..context import Context, GameResult
from ..maze.grid import Grid
from pygame.event import Event
from pygame import Surface
from pygame.locals import (
    K_RETURN, K_BACKSPACE, KEYDOWN,
)
from ..rendering.render import draw_end, render_maze
from ..highscore import new_score, load_highscore
import re


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
            elif event.key == K_RETURN:
                new_score(self.context, {"name": self.name, "score": self.score})
                load_highscore(self.context)
                self.state = StateName.MENU
            elif event.unicode:
                char: str = event.unicode
                if len(self.name) < 10:
                    if re.fullmatch(r"[A-Za-z0-9]", char):
                        self.name += char

    def update(self, dt: float) -> StateName | None:
        self.elapsed += dt
        return self.state

    def render(self) -> None:
        if self.maze_surf is None:
            self.maze_surf = render_maze(
                self.context.screen, self.grid)
        fade = self.elapsed / 2.5
        draw_end(self.context.screen, self.maze_surf,
                 self.score, self.win, fade, self.name,
                 self.context.font)

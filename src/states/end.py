from .state import State
from .main_menu import Main_Menu
from ..context import Context
from pygame.event import Event
from ..game import Game
from pygame import Surface
import re
from pygame.locals import (
    K_RETURN, K_BACKSPACE, KEYDOWN,
)
from ..rendering.render import draw_end, render_maze
class End(State):
    OPTIONS = ("Start Game", "View Highscores", "Settings", "Exit")
    def __init__(self, context: Context, game: Game, win: bool) -> None:
        self.context = context
        self.state: State | None = self
        self.name: str = ""
        self.game: Game = game
        self.win: bool = win
        self.elapsed: float = 0.0
        self.maze_surf: Surface | None = None

    def handle_input(self, events: list[Event]) -> None:
        for event in events:
            if event.type != KEYDOWN:
                continue
            if event.key == K_BACKSPACE:
                self.name = self.name[:-1]
            elif event.key == K_RETURN:
                from ..highscore import new_score, load_highscore
                new_score(self.context, {"name": self.name, "score": self.game.score})
                load_highscore(self.context)
                self.state =  Main_Menu(self.context)
            elif event.unicode:
                char: str = event.unicode
                if len(self.name) < 10:
                    if re.fullmatch(r"[A-Za-z0-9]", char):
                        self.name += char

    def update(self, dt: float) -> "State | None":
        self.elapsed += dt
        return self.state

    def render(self) -> None:
        if self.maze_surf is None:
            self.maze_surf = render_maze(
                self.context.screen, self.game.grid)
        fade = self.elapsed / 2.5
        draw_end(self.context.screen, self.maze_surf,
                 self.game, self.win, fade, self.name,
                 self.context.font)
from .state import State, StateName
from ..context import Context
from pygame.event import Event
from pygame import Surface
from pygame.locals import (
    K_RETURN, K_BACKSPACE, KEYDOWN,
)
from ..rendering.user_interface import draw_end
from ..highscore import new_score, load_highscore
import re


class End(State):
    def __init__(self, context: Context) -> None:
        self.context = context
        self.state: StateName | None = None
        self.name: str = ""
        self.backdrop: Surface = self.context.backdrop
        self.elapsed: float = 0.0

    def handle_input(self, events: list[Event]) -> None:
        for event in events:
            if event.type != KEYDOWN:
                continue
            if event.key == K_BACKSPACE:
                self.name = self.name[:-1]
            elif event.key == K_RETURN:
                new_score(self.context,
                          {"name": self.name,
                           "score": self.context.result.score})
                load_highscore(self.context)
                self.state = StateName.MENU
            elif event.unicode:
                char: str = event.unicode
                if len(self.name) < 10:
                    if re.fullmatch(r"[A-Za-z0-9]", char):
                        self.name += char

    def update(self, dt: float) -> StateName | None:
        self.elapsed += dt
        next_state, self.state = self.state, None
        return next_state

    def render(self) -> None:
        fade = self.elapsed / 0.5
        draw_end(self.context, fade, self.name, self.context.font)

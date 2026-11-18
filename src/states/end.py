import re

from pygame import Surface
from pygame.event import Event
from pygame.locals import K_BACKSPACE, K_RETURN, KEYDOWN

from ..context import Context
from ..highscore import load_highscore, new_score
from ..rendering.user_interface import draw_end
from .state import State, StateName


class End(State):
    """Asks the player's name and saves the score."""

    def __init__(self, context: Context) -> None:
        """Start with an empty name and a fade timer at zero."""
        self.context = context
        self.state: StateName | None = None
        self.name: str = ""
        self.backdrop: Surface = self.context.backdrop
        self.elapsed: float = 0.0
        self.error: bool = False

    def _validate_name(self) -> bool:
        if re.fullmatch(r"[A-Za-z0-9 ]{1,10}", self.name):
            return True
        return False

    def handle_input(self, events: list[Event]) -> None:
        """Type the name (max 10 alnum); Enter saves it and quits to menu."""
        for event in events:
            if event.type != KEYDOWN:
                continue
            if event.key == K_BACKSPACE:
                self.name = self.name[:-1]
            elif event.key == K_RETURN:
                if not self.error and self._validate_name():
                    new_score(self.context,
                              {"name": self.name,
                               "score": self.context.result.score})
                    load_highscore(self.context)
                    self.state = StateName.MENU
                else:
                    self.error = self.error is False
                self.name = ""
            elif event.unicode:
                char: str = event.unicode
                if len(self.name) < 10:
                    self.name += char

    def update(self, dt: float) -> StateName | None:
        """Advance the fade; return the pending request once."""
        self.elapsed += dt
        next_state, self.state = self.state, None
        return next_state

    def render(self) -> None:
        """Draw the end screen with a 0.5 s fade-in."""
        fade = self.elapsed / 0.5
        draw_end(self.context, fade, self.name, self.context.font, self.error)

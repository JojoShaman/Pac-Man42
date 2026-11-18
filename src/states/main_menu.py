from pygame import Surface
from pygame.event import Event
from pygame.locals import (
    K_DOWN, K_RETURN, K_SPACE, K_UP, KEYDOWN, K_s, K_w, K_z,
)

from ..context import Context
from ..rendering.user_interface import draw_main_menu
from .state import State, StateName


class MainMenu(State):
    """Start the game, open the instructions or quit."""

    OPTIONS = ("Start Game", "Instructions", "Exit")

    def __init__(self, context: Context) -> None:
        """Select the first option."""
        self.context = context
        self.selected = 0
        self.menu_surface: Surface | None = None
        self.state: StateName | None = None

    def handle_input(self, events: list[Event]) -> None:
        """Move the selection; Enter/Space requests the chosen screen."""
        for event in events:
            if event.type != KEYDOWN:
                continue
            if event.key in (K_UP, K_w, K_z):
                self.selected = (self.selected - 1) % len(self.OPTIONS)
            elif event.key in (K_DOWN, K_s):
                self.selected = (self.selected + 1) % len(self.OPTIONS)
            elif event.key in (K_RETURN, K_SPACE):
                if self.OPTIONS[self.selected] == "Start Game":
                    self.state = StateName.PLAYING
                if self.OPTIONS[self.selected] == "Instructions":
                    self.state = StateName.INSTRUCTIONS
                if self.OPTIONS[self.selected] == "Exit":
                    self.state = StateName.QUIT

    def update(self, dt: float) -> StateName | None:
        """Return the pending request once, then clear it."""
        next_state, self.state = self.state, None
        return next_state

    def render(self) -> None:
        """Draw the menu and the highscores."""
        draw_main_menu(self.context.screen, self.OPTIONS,
                       self.selected, self.context.highscores)

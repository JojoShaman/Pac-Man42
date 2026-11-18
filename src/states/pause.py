from pygame.event import Event
from pygame.locals import (
    K_DOWN, K_ESCAPE, K_RETURN, K_SPACE, K_UP, KEYDOWN, K_s, K_w, K_z,
)

from ..context import Context
from ..rendering.user_interface import draw_pause_menu
from .state import State, StateName


class PauseMenu(State):
    """Resume, open the instructions or go back to the main menu."""

    OPTIONS: tuple[tuple[str, StateName], ...] = (
        ("Resume", StateName.BACK),
        ("Instructions", StateName.INSTRUCTIONS),
        ("Main Menu", StateName.MENU),
    )

    def __init__(self, context: Context) -> None:
        """Select the first option."""
        self.context = context
        self.selected = 0
        self.state: StateName | None = None

    def handle_input(self, events: list[Event]) -> None:
        """Move the selection; Escape resumes the game."""
        for event in events:
            if event.type != KEYDOWN:
                continue
            if event.key in (K_UP, K_w, K_z):
                self.selected = (self.selected - 1) % len(self.OPTIONS)
            elif event.key in (K_DOWN, K_s):
                self.selected = (self.selected + 1) % len(self.OPTIONS)
            elif event.key in (K_RETURN, K_SPACE):
                self.state = self.OPTIONS[self.selected][1]
            elif event.key == K_ESCAPE:
                self.state = StateName.BACK

    def update(self, dt: float) -> StateName | None:
        """Return the pending request once, then clear it."""
        next_state, self.state = self.state, None
        return next_state

    def render(self) -> None:
        """Draw the pause menu over the blurred game."""
        labels = tuple(label for label, _ in self.OPTIONS)
        draw_pause_menu(self.context, labels, self.selected, "PAUSE")

from pygame.event import Event
from pygame.locals import (
    K_DOWN, K_ESCAPE, K_RETURN, K_SPACE, K_UP, KEYDOWN, K_s, K_w, K_z,
)

from ..context import Context
from ..rendering.user_interface import draw_pause_menu
from .state import State, StateName

INSTRUCTIONS = ("Control keys", "Rules")


class Instructions(State):
    """Choose between the control keys and the rules."""

    def __init__(self, context: Context) -> None:
        """Select the first entry."""
        self.context = context
        self.selected = 0
        self.state: StateName | None = None

    def handle_input(self, events: list[Event]) -> None:
        """Move the selection; Escape goes back."""
        for event in events:
            if event.type != KEYDOWN:
                continue
            if event.key in (K_UP, K_w, K_z):
                self.selected = (self.selected - 1) % len(INSTRUCTIONS)
            elif event.key in (K_DOWN, K_s):
                self.selected = (self.selected + 1) % len(INSTRUCTIONS)
            elif event.key in (K_RETURN, K_SPACE):
                if INSTRUCTIONS[self.selected] == "Control keys":
                    self.state = StateName.CONTROL_KEYS
                if INSTRUCTIONS[self.selected] == "Rules":
                    self.state = StateName.RULES
            elif event.key == K_ESCAPE:
                self.state = StateName.BACK

    def update(self, dt: float) -> StateName | None:
        """Return the pending request once, then clear it."""
        next_state, self.state = self.state, None
        return next_state

    def render(self) -> None:
        """Draw the instructions menu."""
        draw_pause_menu(
            self.context, INSTRUCTIONS, self.selected, "INSTRUCTIONS")

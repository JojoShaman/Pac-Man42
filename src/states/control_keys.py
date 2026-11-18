from pygame.event import Event
from pygame.locals import K_ESCAPE, KEYDOWN

from ..context import Context
from ..rendering.user_interface import draw_controls_menu
from .state import State, StateName

KEYS: dict[str, str] = {
    "UP": "arrow up  w  z",
    "LEFT": "arrow left  a  q",
    "DOWN": "arrow down  s",
    "RIGHT": "arrow right  d",
    "Next Level": "N",
    "Previous Level": "P",
    "Pause/ Resume": "esc",
    "Add 1 life": "+",
    "Remove 1 life": "-",
    "Immortality": "1",
    "Super speed": "2",
    "Freeze ghosts": "3"
}


class Keys(State):
    """Lists the keys of the game and of the cheat mode."""

    def __init__(self, context: Context) -> None:
        """Keep the shared context."""
        self.context = context
        self.selected = 0
        self.state: StateName | None = None

    def handle_input(self, events: list[Event]) -> None:
        """Escape goes back."""
        for event in events:
            if event.type != KEYDOWN:
                continue
            if event.key == K_ESCAPE:
                self.state = StateName.BACK

    def update(self, dt: float) -> StateName | None:
        """Return the pending request once, then clear it."""
        next_state, self.state = self.state, None
        return next_state

    def render(self) -> None:
        """Draw the keys list."""
        draw_controls_menu(self.context, KEYS)

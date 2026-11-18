from .state import State, StateName
from ..context import Context
from pygame.event import Event
from ..rendering.user_interface import draw_controls_menu
from pygame.locals import (
    K_ESCAPE, KEYDOWN
)

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
    def __init__(self, context: Context) -> None:
        self.context = context
        self.selected = 0
        self.state: StateName | None = None

    def handle_input(self, events: list[Event]) -> None:
        for event in events:
            if event.type != KEYDOWN:
                continue
            if event.key == K_ESCAPE:
                self.state = StateName.BACK

    def update(self, dt: float) -> StateName | None:
        next_state, self.state = self.state, None
        return next_state

    def render(self) -> None:
        draw_controls_menu(self.context, KEYS)

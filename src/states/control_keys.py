from .state import State
from .instructions import Instructions
from ..context import Context
from pygame.event import Event
from pygame import Surface, font
from ..rendering.render import draw_controls_menu
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
    def __init__(self, context: Context, last_state: Instructions) -> None:
        self.context = context
        self.selected = 0
        self.instructions = last_state
        self.state: State | None = self

    def handle_input(self, events: list[Event]) -> None:
        for event in events:
            if event.type != KEYDOWN:
                continue
            if event.key == K_ESCAPE:
                self.state = self.instructions

    def update(self, dt: float) -> State | None:
        return self.state

    def render(self) -> None:
        draw_controls_menu(self.context.screen, self.instructions.backdrop, KEYS)
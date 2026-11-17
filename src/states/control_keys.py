from .state import State, StateName
from ..context import Context
from pygame.event import Event
from pygame import Surface, font
from ..rendering.render import draw_controls_menu, blur
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
    "Pause": "L"}


class Keys(State):
    def __init__(self, context: Context,
                 screen: Surface) -> None:
        self.context = context
        self.selected = 0
        self.state: StateName | None = StateName.SETTINGS
        self.backdrop: Surface = blur(screen)

    def handle_input(self, events: list[Event]) -> None:
        for event in events:
            if event.type != KEYDOWN:
                continue
            if event.key == K_ESCAPE:
                self.state = StateName.SETTINGS

    def update(self, dt: float) -> StateName | None:
        return self.state

    def render(self, screen: Surface, font: font.Font) -> None:
        draw_controls_menu(screen, self.backdrop, KEYS, self.selected)

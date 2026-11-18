from .state import State, StateName
from ..context import Context
from pygame.event import Event
from pygame import Surface
from ..rendering.render import draw_pause_menu, blur
from pygame.locals import (
    K_UP, K_DOWN, K_RETURN, K_SPACE, K_ESCAPE,
    K_w, K_s, K_z, KEYDOWN
)

INSTRUCTIONS = ("Control keys", "Rules")


class Instructions(State):
    def __init__(self, context: Context) -> None:
        self.context = context
        self.selected = 0
        self.state: StateName | None = None

    def handle_input(self, events: list[Event]) -> None:
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
        next_state, self.state = self.state, None
        return next_state

    def render(self) -> None:
        draw_pause_menu(self.context.screen, self.context.backdrop, INSTRUCTIONS, self.selected, "INSTRUCTIONS")

from .state import State
from .pause import PauseMenu
from ..context import Context
from pygame.event import Event
from pygame import Surface, font
from ..rendering.render import draw_pause_menu, blur
from pygame.locals import (
    K_UP, K_DOWN, K_RETURN, K_SPACE, K_ESCAPE,
    K_w, K_s, K_z, KEYDOWN
)

INSTRUCTIONS = ("Control keys", "Rules")
class Instructions(State):
    def __init__(self, context: Context, pause: PauseMenu, screen: Surface) -> None:
        self.context = context
        self.selected = 0
        self.screen = screen
        self.pause_menu = pause
        self.state: State | None = self
        self.backdrop: Surface = blur(screen)

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
                    from .control_keys import Keys
                    self.state = Keys(self.context, self, self.screen)
            elif event.key == K_ESCAPE:
                self.state = self.pause_menu

    def update(self, dt: float) -> State | None:
        next_state, self.state = self.state, self
        return next_state

    def render(self, screen: Surface, font: font.Font) -> None:
        draw_pause_menu(screen, self.backdrop, INSTRUCTIONS, self.selected)
from .state import State
from .playing import Playing
from .main_menu import Main_Menu
from ..context import Context
from pygame.event import Event
from pygame import Surface, font
from ..rendering.render import draw_pause_menu, blur
from pygame.locals import (
    K_UP, K_DOWN, K_RETURN, K_SPACE, K_ESCAPE,
    K_w, K_s, K_z, K_l, KEYDOWN
)

PAUSE_OPTIONS = ("Resume", "Instructions", "Main Menu")
class PauseMenu(State):
    def __init__(self, context: Context) -> None:
        self.context = context
        self.selected = 0
        self.state: State | None = self
        self.backdrop: Surface = blur(self.context.screen)
        self.playing: State | None = self.context.last_state

    def handle_input(self, events: list[Event]) -> None:
        for event in events:
            if event.type != KEYDOWN:
                continue
            if event.key in (K_UP, K_w, K_z):
                self.selected = (self.selected - 1) % len(PAUSE_OPTIONS)
            elif event.key in (K_DOWN, K_s):
                self.selected = (self.selected + 1) % len(PAUSE_OPTIONS)
            elif event.key == K_ESCAPE:
                self.state = self.playing
            elif event.key in (K_RETURN, K_SPACE):
                if PAUSE_OPTIONS[self.selected] == "Resume":
                    self.state = self.playing
                if PAUSE_OPTIONS[self.selected] == "Instructions":
                    from .instructions import Instructions
                    self.context.last_state = self
                    self.state = Instructions(self.context, self.backdrop)
                if PAUSE_OPTIONS[self.selected] == "Main Menu":
                    self.state = Main_Menu(self.context)

    def update(self, dt: float) -> State | None:
        next_state, self.state = self.state, self
        return next_state

    def render(self) -> None:
        draw_pause_menu(self.context.screen, self.backdrop, PAUSE_OPTIONS, self.selected, "PAUSE")
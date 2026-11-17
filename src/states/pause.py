from .state import State
from .playing import Playing
from .main_menu import Main_Menu
from ..context import Context
from pygame.event import Event
from pygame import Surface, font
from ..rendering.render import draw_pause_menu, blur
from pygame.locals import (
    K_UP, K_DOWN, K_RETURN, K_SPACE,
    K_w, K_s, K_z, KEYDOWN
)

PAUSE_OPTIONS = ("Resume", "Instructions", "Main Menu")
class PauseMenu(State):
    def __init__(self, context: Context, playing: Playing, screen: Surface) -> None:
        self.context = context
        self.selected = 0
        self.screen = screen
        self.state: State | None = self
        self.playing: Playing = playing
        self.backdrop: Surface = blur(screen)

    def handle_input(self, events: list[Event]) -> None:
        for event in events:
            if event.type != KEYDOWN:
                continue
            if event.key in (K_UP, K_w, K_z):
                self.selected = (self.selected - 1) % len(PAUSE_OPTIONS)
            elif event.key in (K_DOWN, K_s):
                self.selected = (self.selected + 1) % len(PAUSE_OPTIONS)
            elif event.key in (K_RETURN, K_SPACE):
                if PAUSE_OPTIONS[self.selected] == "Resume":
                    self.state = self.playing
                if PAUSE_OPTIONS[self.selected] == "Instructions":
                    from .instructions import Instructions
                    self.state = Instructions(self.context, self, self.screen)
                if PAUSE_OPTIONS[self.selected] == "Main Menu":
                    self.state = Main_Menu(self.context)

    def update(self, dt: float) -> State | None:
        next_state, self.state = self.state, self
        return next_state

    def render(self, screen: Surface, font: font.Font) -> None:
        draw_pause_menu(screen, self.backdrop, PAUSE_OPTIONS, self.selected)
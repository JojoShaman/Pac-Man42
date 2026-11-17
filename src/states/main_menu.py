from .state import State, StateName
from ..context import Context
from pygame.event import Event
from pygame import Surface, font
from ..rendering.render import draw_main_menu
from pygame.locals import (
    K_UP, K_DOWN, K_RETURN, K_SPACE,
    K_w, K_s, K_z, KEYDOWN
)


class MainMenu(State):
    OPTIONS = ("Start Game", "View Highscores", "Instructions", "Exit")

    def __init__(self, context: Context) -> None:
        self.context = context
        self.selected = 0
        self.menu_surface: Surface | None = None
        self.highscores: list[tuple[str, int]] = [("test", 100),
                                                  ("Thomas", 1200)]
        self.state: StateName = StateName.MENU

    def handle_input(self, events: list[Event]) -> None:
        for event in events:
            if event.type != KEYDOWN:
                continue
            if event.key in (K_UP, K_w, K_z):
                self.selected = (self.selected - 1) % len(self.OPTIONS)
            elif event.key in (K_DOWN, K_s):
                self.selected = (self.selected + 1) % len(self.OPTIONS)
            elif event.key in (K_RETURN, K_SPACE):
                if self.OPTIONS[self.selected] == "Start Game":
                    self.state = StateName.PLAYING
                if self.OPTIONS[self.selected] == "Exit":
                    self.state = StateName.QUIT

    def update(self, dt: float) -> StateName | None:
        return self.state

    def render(self, screen: Surface, font: font.Font) -> None:
        draw_main_menu(screen, self.OPTIONS, self.selected, self.highscores)

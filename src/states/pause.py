from .state import State, StateName
from ..context import Context
from pygame.event import Event
from pygame import Surface, font
from ..rendering.render import draw_pause_menu, blur
from pygame.locals import (
    K_UP, K_DOWN, K_RETURN, K_SPACE, K_ESCAPE,
    K_w, K_s, K_z, KEYDOWN
)


class PauseMenu(State):

    OPTIONS: tuple[tuple[str, StateName], ...] = (
        ("Resume", StateName.BACK),
        ("Instructions", StateName.INSTRUCTIONS),
        ("Main Menu", StateName.MENU),
    )

    def __init__(self, context: Context, screen: Surface) -> None:
        self.context = context
        self.selected = 0
        self.state: StateName | None = None
        self.backdrop: Surface = blur(screen)

    def handle_input(self, events: list[Event]) -> None:
        for event in events:
            if event.type != KEYDOWN:
                continue
            if event.key in (K_UP, K_w, K_z):
                self.selected = (self.selected - 1) % len(self.OPTIONS)
            elif event.key in (K_DOWN, K_s):
                self.selected = (self.selected + 1) % len(self.OPTIONS)
            elif event.key in (K_RETURN, K_SPACE):
                self.state = self.OPTIONS[self.selected][1]
            elif event.key == K_ESCAPE:
                self.state = StateName.BACK

    def update(self, dt: float) -> StateName | None:
        next_state, self.state = self.state, None
        return next_state

    def render(self, screen: Surface, font: font.Font) -> None:
        labels = tuple(label for label, _ in self.OPTIONS)
        draw_pause_menu(screen, self.backdrop, labels, self.selected)

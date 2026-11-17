from .state import State
from .instructions import Instructions
from ..context import Context
from pygame.event import Event
from pygame import Surface, font
from ..rendering.render import draw_rules_menu, blur
from pygame.locals import (
    K_ESCAPE, KEYDOWN
)

RULES: list[str] = [
    "• Eat every pac-gum to clear the level.",
    "• Super pac-gums make ghosts edible",
    "   for a few seconds.",
    "• Eat an edible ghost for bonus points.",
    "• A ghost touching you costs one life.",
    "• Each level has a time limit.",
    "• When time runs out, it's game over.",
    "• Lose all your lives and it's game over.",
    "• Clear all 10 levels to win.",
]

class Rules(State):
    def __init__(self, context: Context, last_state: Instructions) -> None:
        self.context = context
        self.selected = 0
        self.instructions = last_state
        self.state: State | None = self
        self.backdrop: Surface = blur(self.context.screen)

    def handle_input(self, events: list[Event]) -> None:
        for event in events:
            if event.type != KEYDOWN:
                continue
            if event.key == K_ESCAPE:
                self.state = self.instructions

    def update(self, dt: float) -> State | None:
        return self.state

    def render(self) -> None:
        draw_rules_menu(self.context.screen, self.backdrop, RULES)
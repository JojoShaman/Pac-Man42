from pygame.event import Event
from pygame.locals import K_ESCAPE, KEYDOWN

from ..context import Context
from ..rendering.user_interface import draw_rules_menu
from .state import State, StateName

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
    """Displays the rules of the game."""

    def __init__(self, context: Context) -> None:
        """Keep the shared context."""
        self.context = context
        self.selected = 0
        self.state: StateName | None = None

    def handle_input(self, events: list[Event]) -> None:
        """Escape goes back."""
        for event in events:
            if event.type != KEYDOWN:
                continue
            if event.key == K_ESCAPE:
                self.state = StateName.BACK

    def update(self, dt: float) -> StateName | None:
        """Return the pending request once, then clear it."""
        next_state, self.state = self.state, None
        return next_state

    def render(self) -> None:
        """Draw the rules."""
        draw_rules_menu(self.context, RULES)

from abc import ABC, abstractmethod
from enum import Enum, auto

from pygame.event import Event


class StateName(Enum):
    """Name of a screen; returned by a state to request a transition."""

    MENU = auto()
    PLAYING = auto()
    HIGHSCORES = auto()
    INSTRUCTIONS = auto()
    CONTROL_KEYS = auto()
    RULES = auto()
    BACK = auto()
    GAME_OVER = auto()
    QUIT = auto()
    PAUSE = auto()


class State(ABC):
    """A screen: reads input, updates itself, draws itself."""

    @abstractmethod
    def handle_input(self, events: list[Event]) -> None:
        """Read the events and store the intentions."""
        pass

    @abstractmethod
    def update(self, dt: float) -> StateName | None:
        """Advance by dt; return the next screen, or None to stay."""
        pass

    @abstractmethod
    def render(self) -> None:
        """Draw the screen."""
        pass

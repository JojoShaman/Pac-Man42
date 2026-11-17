from abc import ABC, abstractmethod
from pygame import Surface, font
from pygame.event import Event
from enum import Enum, auto


class StateName(Enum):
    MENU = auto()
    PLAYING = auto()
    HIGHSCORES = auto()
    SETTINGS = auto()
    INSTRUCTIONS = auto()
    BACK = auto()
    GAME_OVER = auto()
    QUIT = auto()
    PAUSE = auto()


class State(ABC):
    @abstractmethod
    def handle_input(self, events: list[Event]) -> None:
        pass

    @abstractmethod
    def update(self, dt: float) -> StateName | None:
        pass

    @abstractmethod
    def render(self, screen: Surface, font: font.Font) -> None:
        pass



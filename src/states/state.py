from abc import ABC, abstractmethod
from pygame import Surface
from pygame.event import Event


class State(ABC):
    @abstractmethod
    def handle_input(self, events: list[Event]) -> None:
        pass

    @abstractmethod
    def update(self, dt: float) -> "State | None":
        pass

    @abstractmethod
    def render(self, screen: Surface) -> None:
        pass

from abc import *
from pygame import Surface

class State(ABC):
    @abstractmethod
    def handle_input(self) -> None:
        pass

    @abstractmethod
    def update(self, dt: float) -> "State | None":
        pass

    @abstractmethod
    def render(self, screen: Surface) -> None:
        pass

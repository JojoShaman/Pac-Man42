from dataclasses import dataclass
from .config import Config
from .states.state import State
import pygame

@dataclass
class Context:
    config: Config
    font: pygame.font.Font
    screen: pygame.Surface
    last_state: State | None
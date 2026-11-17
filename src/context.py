from dataclasses import dataclass
from .config import Config
from .states.state import State
import pygame
from pathlib import Path
from typing import Any

@dataclass
class Context:
    config: Config
    font: pygame.font.Font
    screen: pygame.Surface
    last_state: State | None
    file_path: Path
    highscores: list[dict[str, Any]]
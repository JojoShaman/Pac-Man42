from dataclasses import dataclass
from .config import Config

@dataclass
class Context:
    config: Config
from .states.state import State
from .states.playing import Playing
from .rendering.render import load_sprites
from .config import Config
import pygame
from pygame.event import Event
from .context import Context


class App:
    def __init__(self, config: Config) -> None:
        self.context: Context = Context(config)
        self.state: State = Playing(self.context)

    def run(self) -> None:
        pygame.init()
        screen = pygame.display.set_mode((1280, 720))
        screen.fill("red")
        load_sprites()
        running = True
        clock = pygame.time.Clock()
        dt: float = 0
        while running:
            events: list[Event] = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    running = False
            self.state.handle_input(events)
            self.state.update(dt)
            self.state.render(screen)
            pygame.display.flip()
            dt = clock.tick(60) / 1000
        pygame.quit()

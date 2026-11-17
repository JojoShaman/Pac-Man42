from .states.state import State
from .states.control_keys import Keys
from .states.main_menu import Main_Menu
from .rendering.render import load_sprites
from .config import Config
import pygame
from pygame.event import Event
from .context import Context


class App:
    def __init__(self, config: Config) -> None:
        pygame.init()
        self.context: Context = Context(config)
        self.state: State | None = Main_Menu(self.context)

    def run(self) -> None:
        font_size = 12
        font = pygame.font.Font(None, font_size)
        screen = pygame.display.set_mode((500, 720))
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
            if self.state:
                self.state.handle_input(events)
                self.state = self.state.update(dt)
                if self.state:
                    self.state.render(screen, font)
                else:
                    break
            pygame.display.flip()
            dt = clock.tick(60) / 1000
        pygame.quit()

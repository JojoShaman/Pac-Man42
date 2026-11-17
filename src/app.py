from .states.state import State
from .states.main_menu import Main_Menu
from .rendering.render import load_sprites
from .config import Config
import pygame
from pygame.event import Event
from .context import Context
from .highscore import load_highscore, get_highscore_path


class App:
    def __init__(self, config: Config) -> None:
        pygame.init()
        self.font = pygame.font.Font(None, 24)
        self.screen = pygame.display.set_mode((500, 720))
        self.context: Context = Context(
            config, self.font, self.screen, None,
            get_highscore_path(config.highscore_filename), [])
        load_highscore(self.context)
        self.state: State | None = Main_Menu(self.context)

    def run(self) -> None:
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
                    self.state.render()
                else:
                    break
            pygame.display.flip()
            dt = clock.tick(60) / 1000
        pygame.quit()

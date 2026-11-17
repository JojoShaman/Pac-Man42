from .states.state import State, StateName
# from .states.control_keys import Keys
from .states.main_menu import MainMenu
from .states.playing import Playing
from .states.end import End
# from .states.pause import PauseMenu
from .rendering.render import load_sprites
from .config import Config
import pygame
from pygame.event import Event
from .context import Context


class App:
    def __init__(self, config: Config) -> None:
        pygame.init()
        self.context: Context = Context(config)
        self.state: State = MainMenu(self.context)

    def _build_state(self, name: StateName) -> State:
        if name is StateName.PLAYING:
            return Playing(self.context)
        elif name is StateName.SETTINGS:
            ...
        elif name is StateName.GAME_OVER:
            if self.context.result is None:
                return MainMenu(self.context)
            return End(self.context, self.context.result)
        return MainMenu(self.context)

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
            self.state.handle_input(events)
            requested = self.state.update(dt)
            if requested is StateName.QUIT:
                running = False
            elif requested is not None:
                self.state = self._build_state(requested)
            self.state.render(screen, font)
            pygame.display.flip()
            dt = min(clock.tick(60) / 1000, 0.05)
        pygame.quit()

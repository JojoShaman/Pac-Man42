from .states.state import State, StateName
# from .states.control_keys import Keys
from .states.main_menu import MainMenu
from .states.playing import Playing
from .states.end import End
from .states.pause import PauseMenu
from .states.instructions import Instructions
from .rendering.render import load_sprites
from .config import Config
import pygame
from pygame.event import Event
from .context import Context


class App:
    def __init__(self, config: Config) -> None:
        pygame.init()
        self.font = pygame.font.Font(None, 24)
        self.screen = pygame.display.set_mode((500, 720))
        self.context: Context = Context(config, self.font, self.screen, None)
        self.states: list[State] = [MainMenu(self.context)]

    def current(self) -> State:
        return self.states[-1]

    def _build_state(self, name: StateName, screen: pygame.Surface) -> State:
        if name is StateName.PLAYING:
            return Playing(self.context)
        if name is StateName.PAUSE:
            return PauseMenu(self.context, screen)
        if name is StateName.INSTRUCTIONS:
            return Instructions(self.context, screen)
        if name is StateName.RULES:
            return Rules(self.context)
        if name is StateName.CONTROL_KEYS:
            return Control_keys(self.context)
        if name is StateName.GAME_OVER:
            result = self.context.result
            if result is not None:
                return End(self.context, result)
        return MainMenu(self.context)

    def _apply(self, requested: StateName, screen: pygame.Surface) -> bool:

        OVERLAYS = {StateName.PAUSE, StateName.INSTRUCTIONS}
        if requested is StateName.QUIT:
            return False
        if requested is StateName.BACK:
            if len(self.states) > 1:
                self.states.pop()
        elif requested in OVERLAYS:
            self.states.append(self._build_state(requested, screen))
        else:
            self.states = [self._build_state(requested, screen)]
        return True

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
            state = self.current()
            state.handle_input(events)
            requested = state.update(dt)
            state.render(screen, font)
            pygame.display.flip()
            if requested is not None and not self._apply(requested, screen):
                running = False
            dt = min(clock.tick(60) / 1000, 0.05)
        pygame.quit()

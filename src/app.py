from .states.state import State, StateName
# from .states.control_keys import Keys
from .states.main_menu import MainMenu
from .states.playing import Playing
from .states.end import End
from .states.pause import PauseMenu
from .states.rules import Rules
from .states.control_keys import Keys
from .states.instructions import Instructions
from .rendering.render import load_sprites, blur
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
            config, self.font, self.screen,
            get_highscore_path(config.highscore_filename), [],
            blur(self.screen))
        load_highscore(self.context)
        self.states: list[State] = [MainMenu(self.context)]

    def _build_state(self, name: StateName) -> State:
        if name is StateName.PLAYING:
            return Playing(self.context)
        if name is StateName.PAUSE:
            return PauseMenu(self.context)
        if name is StateName.INSTRUCTIONS:
            return Instructions(self.context)
        if name is StateName.RULES:
            return Rules(self.context)
        if name is StateName.CONTROL_KEYS:
            return Keys(self.context)
        if name is StateName.GAME_OVER:
            result = self.context.result
            if isinstance(self.states[-1], End):
                return self.states[-1]
            if result:
                return End(self.context, result)
        return MainMenu(self.context)

    def _apply(self, requested: StateName) -> bool:
        OVERLAYS = {StateName.PAUSE, StateName.INSTRUCTIONS,
                    StateName.RULES, StateName.CONTROL_KEYS}
        if requested is StateName.QUIT:
            return False
        if requested is StateName.BACK:
            if len(self.states) > 1:
                self.states.pop()
        elif requested in OVERLAYS:
            self.context.backdrop = blur(self.context.screen)
            self.states.append(self._build_state(requested))
        else:
            self.states = [self._build_state(requested)]
        return True

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
            state = self.states[-1]
            state.handle_input(events)
            requested = state.update(dt)
            # print(state)
            state.render()
            pygame.display.flip()
            if requested is not None and not self._apply(requested):
                running = False
            dt = min(clock.tick(60) / 1000, 0.05)
        pygame.quit()

import pygame
from pygame.event import Event

from .config import Config
from .context import Context, GameResult
from .highscore import get_highscore_path, load_highscore
from .rendering.sprites import load_sprites, resources_path
from .rendering.user_interface import blur
from .states import (
    End,
    Instructions,
    Keys,
    MainMenu,
    PauseMenu,
    Playing,
    Rules,
    State,
    StateName,
)

STATES: dict[StateName, State] = {}
OVERLAYS = {StateName.PAUSE, StateName.INSTRUCTIONS,
            StateName.RULES, StateName.CONTROL_KEYS}


class App:
    """Owns the window, the shared context and the stack of states."""

    def __init__(self, config: Config) -> None:
        """Init pygame, the shared context, the highscores and the states."""
        pygame.init()
        self.font = pygame.font.Font(None, 24)
        self.screen = pygame.display.set_mode((1000, 1440))
        pygame.display.set_caption("Pac-Man")
        self.context: Context = Context(
            config, self.font, self.screen,
            get_highscore_path(config.highscore_filename), [],
            blur(self.screen), GameResult(0, False))
        load_highscore(self.context)
        self.states: list[State] = [MainMenu(self.context)]
        self.init_states()
        self.icon = pygame.image.load(
            resources_path("resources/game_icon.png"))
        pygame.display.set_icon(self.icon)

    def init_states(self) -> None:
        """Create one instance of every screen."""
        STATES[StateName.PLAYING] = Playing(self.context)
        STATES[StateName.PAUSE] = PauseMenu(self.context)
        STATES[StateName.INSTRUCTIONS] = Instructions(self.context)
        STATES[StateName.RULES] = Rules(self.context)
        STATES[StateName.CONTROL_KEYS] = Keys(self.context)
        STATES[StateName.GAME_OVER] = End(self.context)
        STATES[StateName.MENU] = MainMenu(self.context)

    def new_game(self) -> None:
        """Replace the game screen with a fresh one."""
        STATES[StateName.PLAYING] = Playing(self.context)

    def _apply(self, requested: StateName) -> bool:
        """Apply a transition; return False when the app must quit."""
        if requested is StateName.QUIT:
            return False
        if requested is StateName.BACK:
            if len(self.states) > 1:
                self.states.pop()
        elif requested in OVERLAYS:
            if self.states[-1] not in [STATES[name] for name in OVERLAYS]:
                self.context.backdrop = blur(self.context.screen)
            self.states.append(STATES[requested])
        else:
            if requested == StateName.PLAYING:
                self.new_game()
            self.states = [STATES[requested]]
        return True

    def run(self) -> None:
        """Run the main loop: input, update, render, transition."""
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
            state.render()
            pygame.display.flip()
            if requested is not None and not self._apply(requested):
                running = False
            dt = min(clock.tick(60) / 1000, 0.05)
        pygame.quit()

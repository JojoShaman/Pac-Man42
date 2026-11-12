from .state import State
from pygame import *
from pygame.event import Event
from ..rendering.render import render_maze, draw_pacman
from ..game import Game, Intents
from ..direction import Direction

K_DIRECTION: dict[int, Direction] = {
    K_w: Direction.N,
    K_d: Direction.E,
    K_s: Direction.S,
    K_a: Direction.W,
    K_UP: Direction.N,
    K_RIGHT: Direction.E,
    K_DOWN: Direction.S,
    K_LEFT: Direction.W
}

class Playing(State):
    def __init__(self) -> None:
        self.game: Game = Game()
        self.m_surf: Surface | None = None
        self.intents: Intents = Intents() 

    def handle_input(self, events: list[Event]) -> None:
        for event in events:
            if event.type == KEYDOWN and event.key in K_DIRECTION:
                self.intents.direction = K_DIRECTION[event.key]

    def update(self, dt):
        self.game.update(dt, self.intents)
        return self

    def render(self, screen: Surface):
        if self.m_surf is None:
            self.m_surf = render_maze(screen, self.game.grid)
        screen.blit(self.m_surf, (0, 0))
        draw_pacman(screen, self.game.player, self.game.grid)
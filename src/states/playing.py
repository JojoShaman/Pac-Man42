from .state import State
from pygame import Surface
from ..rendering.render import render_maze
from ..maze.grid import Grid
from ..maze.maze_loader import process_maze
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
        return None

    def render(self, screen: Surface):
        grid: Grid = process_maze(15, 15, 42)
        maze_surf: Surface = render_maze(screen, grid)
        screen.blit(maze_surf, (0, 0))
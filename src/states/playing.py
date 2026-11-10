from .state import State
from pygame import Surface
from ..rendering.render import render_maze
from ..maze.grid import Grid
from ..maze.maze_loader import process_maze

class Playing(State):
    def handle_input(self):
        pass

    def update(self, dt):
        return None

    def render(self, screen: Surface):
        grid: Grid = process_maze(15, 15, 42)
        maze_surf: Surface = render_maze(screen, grid)
        screen.blit(maze_surf, (0, 0))
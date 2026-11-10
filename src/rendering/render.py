from pygame import Surface
import pygame
from ..maze.grid import Grid, Cell
from ..direction import Direction

def window_pos(x: float, y: float,
               offset_x: int, offset_y: int,
               cell_size: int) -> tuple[int, int]:
    return (
        int(offset_x + x * cell_size),
        int(offset_y + y * cell_size))

def compute_layout(screen: Surface, maze: Grid) -> tuple[int, int, int]:
    w, h = screen.get_size()
    gw, gh = maze.width, maze.height
    free_h = h - h // 10
    free_w = w - w // 10
    cell_size = min(free_w // gw, free_h // gh)
    offset_x = (w - gw * cell_size) // 2 
    offset_y = (h - gh * cell_size) // 2
    return cell_size, offset_x, offset_y

def render_maze(layout: Surface, grid: Grid) -> Surface:
    maze = Surface(layout.get_size())
    maze.fill('black')
    cell_size, off_x, off_y = compute_layout(maze, grid)
    for row in grid.cells:
        for cell in row:
            x = cell.x
            y = cell.y
            top_left = window_pos(
                x, y, off_x, off_y, cell_size)
            top_right = window_pos(
                x + 1, y, off_x, off_y, cell_size)
            bottom_left = window_pos(
                x, y + 1, off_x, off_y, cell_size)
            bottom_right = window_pos(
                x + 1, y + 1, off_x, off_y, cell_size)
            if cell.has_wall(Direction.N):
                pygame.draw.line(maze, 'white', top_left, top_right, 4)
            if cell.has_wall(Direction.S):
                pygame.draw.line(maze, 'white', bottom_left, bottom_right, 4)
            if cell.has_wall(Direction.E):
                pygame.draw.line(maze, 'white', top_right, bottom_right, 4)
            if cell.has_wall(Direction.W):
                pygame.draw.line(maze, 'white', top_left, bottom_left, 4)
    return maze
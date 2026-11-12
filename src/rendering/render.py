from pygame import *
from ..maze.grid import Grid
from ..direction import Direction
from ..entities import Player


PACMAN: dict[str, Surface] = {}
PM_ROTATE: dict[Direction, list[Surface]] = {}

def load_sprites() -> None:
    rotation: list[tuple[Direction, int]] = [
        (Direction.E, 0),
        (Direction.N, 90),
        (Direction.W, 180),
        (Direction.S, -90)
    ]
    PACMAN['closed'] = image.load(
        "resources/pacman/pacman2.png").convert_alpha()
    PACMAN['open'] = image.load(
        "resources/pacman/pacman.png").convert_alpha()
    PACMAN['half'] = image.load(
        "resources/pacman/pacman1.png").convert_alpha()
    PACMAN['closed1'] = image.load(
    "resources/pacman/pacman2.png").convert_alpha()
    for _, pacman in PACMAN.items():
        for d, r in rotation:
            PM_ROTATE.setdefault(d, []).append(transform.rotate(pacman, r))
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

def render_maze(screen: Surface, grid: Grid) -> Surface:
    maze = Surface(screen.get_size(), SRCALPHA)
    screen.fill('black')
    size, off_x, off_y = compute_layout(maze, grid)
    for row in grid.cells:
        for cell in row:
            x = cell.x
            y = cell.y
            top_left = window_pos(
                x, y, off_x, off_y, size)
            top_right = window_pos(
                x + 1, y, off_x, off_y, size)
            bottom_left = window_pos(
                x, y + 1, off_x, off_y, size)
            bottom_right = window_pos(
                x + 1, y + 1, off_x, off_y, size)
            if cell.has_wall(Direction.N):
                draw.line(maze, 'white', top_left, top_right, 4)
            if cell.has_wall(Direction.S):
                draw.line(maze, 'white', bottom_left, bottom_right, 4)
            if cell.has_wall(Direction.E):
                draw.line(maze, 'white', top_right, bottom_right, 4)
            if cell.has_wall(Direction.W):
                draw.line(maze, 'white', top_left, bottom_left, 4)
            if all(
                cell.has_wall(wall) for wall in [
                    Direction.N, Direction.S, Direction.E, Direction.W]):
                left, top = top_left
                screen.fill('blue', Rect(left, top, size, size))
    screen.blit(maze, (0, 0))
    return screen
from pygame import Surface, image, transform, draw, SRCALPHA, Rect, time
from ..maze.grid import Grid
from ..direction import Direction
from ..entities import Player
import math


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


def draw_pacman(screen: Surface, player: Player, grid: Grid) -> None:
    step = int(player.travelled / 0.25) % 4
    pacman = transform.scale(PM_ROTATE[player.direction][step], (26, 26))
    x = player.x
    y = player.y
    size, off_x, off_y = compute_layout(screen, grid)
    re_center = window_pos(x + 0.5, y + 0.5, off_x, off_y, size)
    screen.blit(pacman, pacman.get_rect(center=re_center))


def draw_pacgums(screen: Surface, pacgums: list[tuple[int, int]],
                 grid: Grid) -> None:
    size, off_x, off_y = compute_layout(screen, grid)
    for x, y in pacgums:
        p_center = window_pos(x + 0.5, y + 0.5, off_x, off_y, size)
        draw.circle(screen, 'yellow', p_center, 3)


def draw_super_pacgums(screen: Surface, super_pacgums: list[tuple[int, int]],
                       grid: Grid) -> None:
    size, off_x, off_y = compute_layout(screen, grid)
    t = time.get_ticks() / 1000
    breath = math.sin(t * 3)
    radius = max(2, int(size * (0.2 + 0.03 * breath)))
    for x, y in super_pacgums:
        center = window_pos(x + 0.5, y + 0.5, off_x, off_y, size)
        draw.circle(screen, (255, 235, 200), center, radius)   # crème


def window_pos(x: float, y: float,
               offset_x: int, offset_y: int,
               cell_size: int) -> tuple[int, int]:
    return (
        int(offset_x + x * cell_size),
        int(offset_y + y * cell_size))


def compute_layout(screen: Surface, maze: Grid) -> tuple[int, int, int]:
    w, h = screen.get_size()
    gw, gh = maze.width, maze.height
    free_h = h - h // 5
    free_w = w - w // 5
    cell_size = min(free_w // gw, free_h // gh)
    offset_x = (w - gw * cell_size) // 2
    offset_y = (h - gh * cell_size) // 2
    return cell_size, offset_x, offset_y


def render_maze(screen: Surface, grid: Grid) -> Surface:
    maze = Surface(screen.get_size(), SRCALPHA)
    background: Surface = Surface(screen.get_size(), SRCALPHA)
    background.fill('black')
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
                background.fill('blue', Rect(left, top, size, size))
    background.blit(maze, (0, 0))
    return background

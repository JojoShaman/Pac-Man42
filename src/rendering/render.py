from pygame import Surface, image, transform, draw, SRCALPHA, Rect, font, time
from ..maze.grid import Grid
from ..direction import Direction
from ..entities import Player
from ..entities.ghosts import Ghost, GhostMode
from ..game import Game
import math
import pygame


PACMAN: dict[str, Surface] = {}
PM_ROTATE: dict[Direction, list[Surface]] = {}
STARTER: dict[int, Surface] = {}
GHOSTS: dict[str, Surface] = {}
EDIBLE: list[Surface] = []


def load_sprites() -> None:
    rotation: list[tuple[Direction, int]] = [
        (Direction.E, 0),
        (Direction.N, 90),
        (Direction.W, 180),
        (Direction.S, -90)
    ]
    PACMAN['closed'] = image.load(
        "resources/pacman/pacman2.png")
    PACMAN['open'] = image.load(
        "resources/pacman/pacman.png")
    PACMAN['half'] = image.load(
        "resources/pacman/pacman1.png")
    PACMAN['closed1'] = image.load(
        "resources/pacman/pacman2.png")
    for _, pacman in PACMAN.items():
        for d, r in rotation:
            PM_ROTATE.setdefault(d, []).append(transform.rotate(pacman, r))
    for i in range(1,4):
        STARTER[i] = image.load(
            f"resources/starter/{i}_40x40.png")
    for ghost in ["blinky", "pinky", "inky", "clyde"]:
        GHOSTS[ghost] = image.load(
            f"resources/ghost_gang/{ghost}.png")
    for i in range(2):
        EDIBLE.append(
            image.load(f"resources/ghost_gang/edible/edible{i}.png"))


def draw_pacman(screen: Surface, player: Player, grid: Grid) -> None:
    step = int(player.travelled / 0.25) % 4
    cell_size, _, _ = compute_layout(screen, grid)
    size = int(cell_size - cell_size * 0.35)
    pacman = transform.scale(
        PM_ROTATE[player.direction][step], (size, size))
    x = player.x
    y = player.y
    size, off_x, off_y = compute_layout(screen, grid)
    re_center = window_pos(x + 0.5, y + 0.5, off_x, off_y, size)
    screen.blit(pacman, pacman.get_rect(center=re_center))

def draw_ghost(screen: Surface, ghost: Ghost, grid: Grid) -> None:
    cell_size, _, _ = compute_layout(screen, grid)
    size = int(cell_size - cell_size * 0.35)
    if ghost.mode != GhostMode.EDIBLE:
        image = GHOSTS[ghost.name].copy()
        if ghost.mode in (GhostMode.EATEN, GhostMode.WAITING):
            value = (128, 192)
            step = (int(ghost.spawn_delay * 4) % 2
                    if ghost.spawn_delay < 4 else 0)
            image.set_alpha(value[step])
    else:
        step = int(ghost.edible_delay * 4) % 2
        if ghost.edible_delay < 2:
            image = EDIBLE[step]
        else:
            image = EDIBLE[0]
    g = transform.scale(image, (size - 2, size))
    x = ghost.x
    y = ghost.y
    size, off_x, off_y = compute_layout(screen, grid)
    re_center = window_pos(x + 0.5, y + 0.5, off_x, off_y, size)
    screen.blit(g, g.get_rect(center=re_center))

def draw_pacgums(screen: Surface, pacgums: list[tuple[int, int]],
                 grid: Grid) -> None:
    size, off_x, off_y = compute_layout(screen, grid)
    for x, y in pacgums:
        p_center = window_pos(
            x + 0.5, y + 0.5, off_x, off_y, size)
        draw.circle(screen, 'yellow', p_center, 3)


def draw_start_timer(screen: Surface, game: Game) -> None:
    step = math.ceil(game.start_timer)
    s = STARTER.get(step)
    if s is None:
        return
    cell_size, off_x, off_y = compute_layout(screen,  game.grid)
    gr_w = game.grid.width * cell_size
    gr_h = game.grid.height * cell_size
    size = gr_w - gr_w * 0.7
    center_x = off_x + gr_w // 2
    center_y = off_y + gr_h // 2
    resize = transform.scale(s, (size, size))
    screen.blit(resize, resize.get_rect(center=(center_x, center_y)))

def draw_hud(screen: Surface, game: Game, font: font.Font) -> None:
    texts = (
        f"Score: {game.score}",
        f"Lives: {game.lives}",
        f"Level: {game.current_lvl + 1}",
        f"Time left: {int(game.time_left)}"
    )
    col = screen.get_width() // len(texts)
    for i, text in enumerate(texts):
        surface = font.render(text, True, (255, 255, 255))
        rect = surface.get_rect(center=(col * i + col // 2, 20))
        screen.blit(surface, rect)


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
    free_h = h - h // 10
    free_w = w - w // 10
    cell_size = min(free_w // gw, free_h // gh)
    offset_x = (w - gw * cell_size) // 2
    offset_y = h // 10
    return cell_size, offset_x, offset_y


def render_maze(screen: Surface, grid: Grid) -> Surface:
    maze = Surface(screen.get_size(), SRCALPHA)
    background: Surface = Surface(screen.get_size(), SRCALPHA)
    background.fill('black')
    size, off_x, off_y = compute_layout(maze, grid)
    largest = max(grid.width, grid.height)
    v_const = 50
    line_width = round(v_const / largest)
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
                draw.line(maze, 'white', top_left, top_right, line_width)
            if cell.has_wall(Direction.S):
                draw.line(maze, 'white', bottom_left, bottom_right, line_width)
            if cell.has_wall(Direction.E):
                draw.line(maze, 'white', top_right, bottom_right, line_width)
            if cell.has_wall(Direction.W):
                draw.line(maze, 'white', top_left, bottom_left, line_width)
            if all(
                cell.has_wall(wall) for wall in [
                    Direction.N, Direction.S, Direction.E, Direction.W]):
                left, top = top_left
                background.fill('blue', Rect(left, top, size, size))
    background.blit(maze, (0, 0))
    return background

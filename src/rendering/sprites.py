from ..direction import Direction
from pygame import (
    Surface, image, transform, draw, Color, time,
    BLEND_RGB_MAX, BLEND_RGB_MULT)
from ..entities import Player, Ghost, GhostMode
from ..maze.grid import Grid
from ..game import Game
from .render import compute_layout, window_pos
import math


PACMAN: dict[str, Surface] = {}
PM_ROTATE: dict[Direction, list[Surface]] = {}
STARTER: dict[int, Surface] = {}
GHOSTS: dict[str, Surface] = {}
EDIBLE: list[Surface] = []
END: dict[str, Surface] = {}

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
        "resources/pacman/pacman0.png").convert_alpha()
    PACMAN['half'] = image.load(
        "resources/pacman/pacman1.png").convert_alpha()
    PACMAN['closed1'] = image.load(
        "resources/pacman/pacman2.png").convert_alpha()
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
    END["game_over"] = image.load(f"resources/end_game/GameOver.png")
    END["you_win"] = image.load(f"resources/end_game/YouWon.png")

def draw_pacman(screen: Surface, player: Player, grid: Grid) -> None:
    step = int(player.travelled / 0.5) % 4
    cell_size, off_x, off_y = compute_layout(screen, grid)
    size = int(cell_size - cell_size * 0.35)
    pacman = transform.scale(
        PM_ROTATE[player.direction][step], (size, size))
    if player.immortal:
        hue = (time.get_ticks() / 200 * 180) % 360
        color = Color(0, 0, 0)
        color.hsva = (hue, 100, 100, 100)
        pacman.fill((255, 255, 255), special_flags=BLEND_RGB_MAX)
        pacman.fill(color, special_flags=BLEND_RGB_MULT)
    x = player.x
    y = player.y
    re_center = window_pos(x + 0.5, y + 0.5, off_x, off_y, cell_size)
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
        draw.circle(screen, 'yellow', p_center, size * 0.1)

def draw_super_pacgums(screen: Surface, super_pacgums: list[tuple[int, int]],
                       grid: Grid) -> None:
    size, off_x, off_y = compute_layout(screen, grid)
    t = time.get_ticks() / 1000
    breath = math.sin(t * 3)
    radius = max(2, int(size * (0.2 + 0.03 * breath)))
    for x, y in super_pacgums:
        center = window_pos(x + 0.5, y + 0.5, off_x, off_y, size)
        draw.circle(screen, (255, 235, 200), center, radius)

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
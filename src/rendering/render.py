from pygame import Surface, image, transform, draw, SRCALPHA, Rect, font, time
from ..maze.grid import Grid
from ..direction import Direction
from ..entities import Player
from ..entities.ghosts import Ghost, GhostMode
from ..game import Game
import math
from functools import lru_cache
from pygame.font import Font


PACMAN: dict[str, Surface] = {}
PM_ROTATE: dict[Direction, list[Surface]] = {}
STARTER: dict[int, Surface] = {}
GHOSTS: dict[str, Surface] = {}
EDIBLE: list[Surface] = []
END: dict[str, Surface] = {}
BACKGROUND = (8, 8, 20)
YELLOW = (255, 221, 0)
ORANGE = (200, 110, 0)
WHITE = (235, 235, 240)
GREY = (125, 125, 140)
BLUE = (40, 60, 220)
INPUT_BAR_SIZE = (260, 44)
TEXT_COLOR = "white"


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
    END["game_over"] = image.load(f"resources/end_game/GameOver.png")
    END["you_win"] = image.load(f"resources/end_game/YouWon.png")


def draw_end(
        screen: Surface,
        maze_surf: Surface,
        score: int,
        win: bool,
        fade: float,
        name: str,
        font: font.Font) -> None:
    w, h = screen.get_size()
    fade = max(0.0, min(fade, 1.0))

    screen.blit(maze_surf, (0, 0))
    veil = Surface((w, h), SRCALPHA)
    veil.fill((0, 0, 0, int(255 * fade)))
    screen.blit(veil, (0, 0))

    title = transform.scale(END["you_win" if win else "game_over"], (400, 100))
    screen.blit(title, title.get_rect(center=(w // 2, h // 4)))

    if fade < 1.0:
        return

    center_y = h // 2

    score_font = font.render(f"SCORE  {score}", True, TEXT_COLOR)
    screen.blit(score_font,
                score_font.get_rect(center=(w // 2, center_y - 60)))

    label = font.render("ENTER YOUR NAME", True, TEXT_COLOR)
    screen.blit(label, label.get_rect(center=(w // 2, center_y - 20)))

    bar = Rect((0, 0), INPUT_BAR_SIZE)
    bar.center = (w // 2, center_y + 30)
    draw.rect(screen, TEXT_COLOR, bar, 2)

    text = font.render(name, True, TEXT_COLOR)
    screen.blit(text, text.get_rect(center=bar.center))


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


@lru_cache(maxsize=None)
def get_font(size: int) -> Font:
    """Return a font of this size, created on first use."""
    return Font(None, size)

def _blit_centered(screen: Surface, text: str, size: int,
                   color: tuple[int, int, int], center: tuple[int, int]
                   ) -> None:
    surface = get_font(size).render(text, True, color)
    screen.blit(surface, surface.get_rect(center=center))

def _blit_left(screen: Surface, text: str, size: int,
                   color: tuple[int, int, int], midleft: tuple[int, int]
                   ) -> None:
    surface = get_font(size).render(text, True, color)
    screen.blit(surface, surface.get_rect(midleft=midleft))

def _blit_right(screen: Surface, text: str, size: int,
                   color: tuple[int, int, int], midright: tuple[int, int]
                   ) -> None:
    surface = get_font(size).render(text, True, color)
    screen.blit(surface, surface.get_rect(midright=midright))


def _draw_title(screen: Surface, t: float) -> None:
    """Big yellow title with a soft shadow and a gentle float."""
    w, h = screen.get_size()
    y = int(h * 0.17 + 5 * math.sin(t * 2))
    _blit_centered(screen, "PAC-MAN", 120, ORANGE, (w // 2 + 5, y + 6))
    _blit_centered(screen, "PAC-MAN", 120, YELLOW, (w // 2, y))


def _draw_dots(screen: Surface, t: float) -> None:
    """A row of dots scrolling to the left under the title."""
    w, h = screen.get_size()
    y, step = int(h * 0.29), 36
    shift = (t * 60) % step
    for i in range(-1, w // step + 2):
        draw.circle(screen, WHITE, (int(i * step - shift), y), 4)


def _draw_option(screen: Surface, text: str, center: tuple[int, int],
                 selected: bool, t: float, frame_w: int = 460) -> None:
    """One menu line; the selected one gets a frame and a bobbing cursor."""
    if not selected:
        _blit_centered(screen, text, 44, GREY, center)
        return
    cx, cy = center
    half = frame_w // 2
    draw.rect(screen, BLUE, (cx - half, cy - 28, frame_w, 56), width=3,
              border_radius=14)
    _blit_centered(screen, text, 54, YELLOW, center)
    x = cx - half + 40 + int(6 * math.sin(t * 6))  # cursor goes back and forth
    draw.polygon(screen, YELLOW, [(x, cy - 12), (x + 20, cy), (x, cy + 12)])


def _draw_highscores(screen: Surface,
                     highscores: list[tuple[str, int]]) -> None:
    """Compact top 5 at the bottom of the screen."""
    w, h = screen.get_size()
    top = int(h * 0.73)
    _blit_centered(screen, "HIGHSCORES", 30, YELLOW, (w // 2, top))
    if not highscores:
        _blit_centered(screen, "No score yet", 26, GREY, (w // 2, top + 34))
        return
    for i, (name, score) in enumerate(highscores[:5]):
        line = f"{i + 1}.  {name}  -  {score} pts"
        _blit_centered(screen, line, 26, WHITE, (w // 2, top + 34 + i * 26))


def draw_main_menu(screen: Surface, options: tuple[str, ...], selected: int,
                   highscores: list[tuple[str, int]]) -> None:
    """Draw the whole main menu."""
    w, h = screen.get_size()
    t = time.get_ticks() / 1000
    screen.fill(BACKGROUND)
    _draw_title(screen, t)
    _draw_dots(screen, t)
    for i, text in enumerate(options):
        _draw_option(screen, text, (w // 2, int(h * 0.40) + i * 58),
                     i == selected, t)
    _draw_highscores(screen, highscores)
    _blit_centered(screen, "UP / DOWN to move  -  ENTER to select", 22, GREY,
                   (w // 2, h - 22))

def blur(surface: Surface, factor: int = 20) -> Surface:
    """Return a blurred copy: shrink then enlarge with smoothing."""

    w, h = surface.get_size()
    small = transform.smoothscale(surface,
                                  (max(1, w // factor), max(1, h // factor)))
    return transform.smoothscale(small, (w, h))


def draw_pause_menu(screen: Surface, backdrop: Surface,
                    options: tuple[str, ...], selected: int) -> None:
    """Draw a small pause window over the blurred, dimmed game."""
    PANEL_W = 420
    FRAME_W = PANEL_W - 60
    w, h = screen.get_size()
    t = time.get_ticks() / 1000
    screen.blit(backdrop, (0, 0))

    veil = Surface((w, h), SRCALPHA)
    veil.fill((0, 0, 0, 5))
    screen.blit(veil, (0, 0))

    panel = Rect(0, 0, PANEL_W, 140 + len(options) * 58)
    panel.center = (w // 2, h // 2)
    draw.rect(screen, BACKGROUND, panel, border_radius=18)
    draw.rect(screen, BLUE, panel, width=3, border_radius=18)

    _blit_centered(screen, "PAUSED", 64, YELLOW, (w // 2, panel.top + 50))
    for i, text in enumerate(options):
        _draw_option(screen, text, (w // 2, panel.top + 120 + i * 58),
                     i == selected, t, FRAME_W)

def draw_controls_menu(screen: Surface, backdrop: Surface,
                    options: dict[str, str], selected: int) -> None:
    """Draw a small pause window over the blurred, dimmed game."""
    PANEL_W = 420
    w, h = screen.get_size()
    screen.blit(backdrop, (0, 0))

    veil = Surface((w, h), SRCALPHA)
    veil.fill((0, 0, 0, 5))
    screen.blit(veil, (0, 0))

    panel = Rect(0, 0, PANEL_W, 140 + len(options) * 58)
    panel.center = (w // 2, h // 2)
    draw.rect(screen, BACKGROUND, panel, border_radius=18)
    draw.rect(screen, BLUE, panel, width=3, border_radius=18)

    _blit_centered(screen, "KEYS", 64, YELLOW, (w // 2, panel.top + 50))
    for i, (key, value) in enumerate(options.items()):
        midleft = (panel.left + 30, panel.top + 120 + i * 58)
        midright = (panel.right - 30, panel.top + 120 + i * 58)
        _blit_left(screen, key, 34, YELLOW, midleft)
        _blit_right(screen, value, 34, YELLOW, midright)

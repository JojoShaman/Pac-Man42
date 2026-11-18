from pygame import (
    Surface, transform, draw, Rect, font, time, SRCALPHA)
from .colors import (BACKGROUND, YELLOW, ORANGE, WHITE, GREY, BLUE)
from .sprites import END
from ..context import Context
from functools import lru_cache
from pygame.font import Font
from typing import Any
import math


INPUT_BAR_SIZE = (260, 44)
TEXT_COLOR = "white"

@lru_cache(maxsize=None)
def get_font(size: int) -> Font:
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
    w, h = screen.get_size()
    y = int(h * 0.17 + 5 * math.sin(t * 2))
    _blit_centered(screen, "PAC-MAN", 120, ORANGE, (w // 2 + 5, y + 6))
    _blit_centered(screen, "PAC-MAN", 120, YELLOW, (w // 2, y))


def _draw_dots(screen: Surface, t: float) -> None:
    w, h = screen.get_size()
    y, step = int(h * 0.29), 36
    shift = (t * 60) % step
    for i in range(-1, w // step + 2):
        draw.circle(screen, WHITE, (int(i * step - shift), y), 4)


def _draw_option(screen: Surface, text: str, center: tuple[int, int],
                 selected: bool, t: float, frame_w: int = 460) -> None:
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
                     highscores: list[dict[str, Any]]) -> None:
    w, h = screen.get_size()
    top = int(h * 0.63)
    _blit_centered(screen, "HIGHSCORES", 30, YELLOW, (w // 2, top))
    if not highscores:
        _blit_centered(screen, "No score yet", 26, GREY, (w // 2, top + 34))
        return
    for i, player in enumerate(highscores[:10]):
        name = player['name']
        score = player['score']
        line = f"{i + 1}.  {name}  -  {score} pts"
        _blit_centered(screen, line, 26, WHITE, (w // 2, top + 34 + i * 20))


def draw_main_menu(screen: Surface, options: tuple[str, ...], selected: int,
                   highscores: list[dict[str, Any]]) -> None:
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

def blur(surface: Surface, factor: int = 12) -> Surface:
    """Return a blurred copy: shrink then enlarge with smoothing."""

    w, h = surface.get_size()
    small = transform.smoothscale(surface,
                                  (max(1, w // factor), max(1, h // factor)))
    return transform.smoothscale(small, (w, h))


def draw_pause_menu(context: Context,
                    options: tuple[str, ...], selected: int, 
                    interface: str) -> None:
    s = context.screen
    b = context.backdrop
    PANEL_W = 420
    FRAME_W = PANEL_W - 60
    w, h = s.get_size()
    t = time.get_ticks() / 1000
    s.blit(b, (0, 0))

    veil = Surface((w, h), SRCALPHA)
    veil.fill((0, 0, 0, 5))
    s.blit(veil, (0, 0))

    panel = Rect(0, 0, PANEL_W, 140 + len(options) * 58)
    panel.center = (w // 2, h // 2)
    draw.rect(s, BACKGROUND, panel, border_radius=18)
    draw.rect(s, BLUE, panel, width=3, border_radius=18)

    _blit_centered(s, interface, 64, YELLOW, (w // 2, panel.top + 50))
    for i, text in enumerate(options):
        _draw_option(s, text, (w // 2, panel.top + 120 + i * 58),
                     i == selected, t, FRAME_W)

def draw_controls_menu(context: Context, options: dict[str, str]) -> None:
    s = context.screen
    b = context.backdrop
    PANEL_W = 420
    w, h = s.get_size()
    s.blit(b, (0, 0))

    veil = Surface((w, h), SRCALPHA)
    veil.fill((0, 0, 0, 5))
    s.blit(veil, (0, 0))

    panel = Rect(0, 0, PANEL_W, 140 + len(options) * 38)
    panel.center = (w // 2, h // 2)
    draw.rect(s, BACKGROUND, panel, border_radius=18)
    draw.rect(s, BLUE, panel, width=3, border_radius=18)

    _blit_centered(s, "KEYS", 64, YELLOW, (w // 2, panel.top + 50))
    for i, (key, value) in enumerate(options.items()):
        midleft = (panel.left + 30, panel.top + 120 + i * 38)
        midright = (panel.right - 30, panel.top + 120 + i * 38)
        _blit_left(s, key, 24, YELLOW, midleft)
        _blit_right(s, value, 24, YELLOW, midright)

def draw_rules_menu(context: Context,
                    options: list[str]) -> None:
    s = context.screen
    b = context.backdrop
    PANEL_W = 420
    w, h = s.get_size()
    s.blit(b, (0, 0))

    veil = Surface((w, h), SRCALPHA)
    veil.fill((0, 0, 0, 5))
    s.blit(veil, (0, 0))

    panel = Rect(0, 0, PANEL_W, 140 + len(options) * 58)
    panel.center = (w // 2, h // 2)
    draw.rect(s, BACKGROUND, panel, border_radius=18)
    draw.rect(s, BLUE, panel, width=3, border_radius=18)

    _blit_centered(s, "RULES", 64, YELLOW, (w // 2, panel.top + 50))
    for i, rule in enumerate(options):
        midleft = (panel.left + 30, panel.top + 120 + i * 30)
        _blit_left(s, rule, 24, YELLOW, midleft)

def draw_end(context: Context, fade: float,
             name: str, font: font.Font) -> None:
    s = context.screen
    b = context.backdrop
    score = context.result.score
    win = context.result.won
    w, h = s.get_size()
    fade = max(0.0, min(fade, 1.0))

    s.blit(b, (0, 0))
    veil = Surface((w, h), SRCALPHA)
    veil.fill((0, 0, 0, int(255 * fade)))
    s.blit(veil, (0, 0))
    title = transform.scale(END["you_win" if win else "game_over"], (400, 100))
    s.blit(title, title.get_rect(center=(w // 2, h // 4)))

    if fade < 1.0:
        return
    center_y = h // 2

    score_font = font.render(f"SCORE  {score}", True, TEXT_COLOR)
    s.blit(score_font,
                score_font.get_rect(center=(w // 2, center_y - 60)))

    label = font.render("ENTER YOUR NAME", True, TEXT_COLOR)
    s.blit(label, label.get_rect(center=(w // 2, center_y - 20)))

    bar = Rect((0, 0), INPUT_BAR_SIZE)
    bar.center = (w // 2, center_y + 30)
    draw.rect(s, TEXT_COLOR, bar, 2)

    text = font.render(name, True, TEXT_COLOR)
    s.blit(text, text.get_rect(center=bar.center))
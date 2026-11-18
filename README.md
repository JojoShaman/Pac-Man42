*This project has been created as part of the 42 curriculum by tmattela, srosu.*

# Pac-Man

> *Ghosts! More ghosts!* — a complete, playable Pac-Man written in Python, with generated mazes, ten levels, four ghosts with their own behaviour, a persistent highscore table and a cheat mode for peer review.

## Description

The goal of this project is to recreate the classic arcade game **Pac-Man** with a modern Python code base: object-oriented, fully type-hinted, configurable through a file, robust to bad input (no crash, no traceback), and packaged so that it can be installed and launched from a public game platform.

Overview of the game:

- The player moves through a maze, eats every **pacgum** to finish the level, and keeps score and lives from one level to the next.
- **Super-pacgums** sit in the four corners of the maze. Eating one makes the ghosts edible for a short time.
- **Four ghosts** (Blinky, Pinky, Inky and Clyde) start in the four corners and chase the player, each with its own target.
- The game has **10 levels**, each with a time limit. The first level uses a fixed seed (reproducible), the following ones use random seeds.
- Mazes are **not written by us**: they come from an external *A-Maze-ing* package assigned by the school (see [Maze Generation](#maze-generation)).
- A **persistent top 10** is displayed in the main menu, and the player enters their name at the end of every game (win or lose).
- A **cheat mode** helps reviewers test every feature quickly.

## Instructions

### Requirements

- Python **3.10 or later**
- [`uv`](https://docs.astral.sh/uv/) (or `pip`) to install the dependencies
- The assigned maze generator wheel, `mazegenerator-2.1.0-py3-none-any.whl`, installed by `make install`
- Main dependencies: `pygame` (window, drawing, input) and `platformdirs` (location of the highscore file)

### Installation and execution

```bash
make install        # install the dependencies, including the maze generator wheel
make run            # launch the game with the default configuration file
make debug          # launch the game under pdb
make lint           # flake8 + mypy (mandatory flags)
make lint-strict    # flake8 + mypy --strict
make clean          # remove __pycache__, .mypy_cache, ...
```

The program takes **exactly one argument**: the path to a JSON configuration file.

```bash
make run ARGS=config.json
# or, with uv
uv run python3 pac-man.py config.json
```

Every error (missing file, unreadable file, invalid value, missing key) is reported with a clear message, never with a Python traceback.

### Controls

| Key | Action |
|---|---|
| Arrow keys, `W A S D` (`Z Q S D` on AZERTY) | Move the player / navigate the menus |
| `Enter` or `Space` | Select a menu entry |
| `Esc` | Pause (in game) / go back (in sub-menus) |
| `S`, `I`, `F`, `L`, `Space` | Cheat mode actions (only when cheat mode is on, see [Cheat mode](#cheat-mode)) |

### Game loop

`Main menu` → `Start Game` → `Win or Lose` → `Enter your name` → `Back to the main menu`

The pause menu offers *Resume*, *Instructions* and *Main Menu*. While the game is paused, the game is not updated, so the level timer stops.

### Public build

A free, unlisted build of the game is available on <platform and URL of the build>.

## Configuration

The configuration file is **JSON with comments**: every line starting with `#` (after optional leading spaces) is ignored. Every key is optional: a missing or invalid value is replaced by its default (or clamped to the nearest valid value), a clear message is logged, and the game continues. Unknown keys are ignored.

| Key | Type | Default | Rule |
|---|---|---|---|
| `highscore_filename` | string | `highscores.json` | File name only (no path separator). The file is stored in the user's data folder. |
| `levels` | list of `{width, height}` | 10 default levels | Exactly 10 levels are used: missing ones are filled with default levels, extra ones are ignored. An invalid level is replaced by a default one without affecting the others. |
| `levels[].width`, `levels[].height` | integer | per level | 10 to 50 cells. The cell size in pixels is computed to fit the window. |
| `lives` | integer | `3` | 1 to 5 |
| `pacgums` | integer | `42` | At least 10. The upper bound is the number of free corridor cells, known only once the maze is generated: the value is clamped at generation time and a message is logged. |
| `points_per_pacgum` | integer | `10` | Positive, at most 1 000 |
| `points_per_super_pacgum` | integer | `50` | Positive, at most 5 000 |
| `points_per_ghost` | integer | `200` | Positive, at most 20 000 |
| `seed` | integer | `42` | Positive. Used for the **first level only**; the next levels use random seeds. |
| `level_max_time` | integer (seconds) | `90` | 30 to 600 |
| `cheat_mode` | boolean | `false` | `true` or `false` only (no string, no integer) |

Integer keys explicitly reject booleans: in Python `True` and `False` are instances of `int`, so a plain `isinstance` check would accept them.

Example:

```text
# Pac-Man configuration
{
    "highscore_filename": "highscores.json",
    # Missing levels are filled with default ones
    "levels": [
        {"width": 15, "height": 15},
        {"width": 20, "height": 15},
        {"width": 25, "height": 20}
    ],
    "lives": 3,
    "pacgums": 42,
    "points_per_pacgum": 10,
    "points_per_super_pacgum": 50,
    "points_per_ghost": 200,
    "seed": 42,
    "level_max_time": 90,
    "cheat_mode": false
}
```

### How the file is loaded

`load_config(content)` runs the following pipeline and never raises on bad content:

1. Remove the comment lines.
2. Parse the JSON. If it is invalid, log a message and use the default configuration.
3. Check that the root is an object, otherwise use the default configuration.
4. Validate each key independently (`_validate_int`, `_validate_bool`, `_validate_filename`, `_validate_levels`). On error, log a message and keep the default value of that key only.
5. Ignore unknown keys.
6. Build the `Config` dataclass.

The configuration may be modified during the defense: every value above can be changed without touching the code.

## Highscore

**How it works.** The top 10 is stored in a JSON file, in the user's data folder given by `platformdirs` (so it works on any OS and never inside the repository). The file name comes from the configuration. Each entry looks like `{"name": "Sydney", "score": 1200}`. Highscores are loaded when the game starts, displayed in the main menu (and in the *View Highscores* screen), and saved when a game ends.

**Why this design.**

- A JSON file is simple, human-readable, and needs no dependency.
- Storing it in the user's data folder keeps the repository clean and survives re-installations of the game.
- Saving to a temporary file then calling `os.replace` makes the write atomic: if the game crashes while saving, only the temporary file is affected and the previous highscores stay intact.

**Robustness.**

- Missing file or invalid JSON: the game starts with an empty list.
- Corrupted entry (name too long, negative or non-integer score, wrong shape): only that entry is dropped.
- Name entry: at most 10 characters, letters, digits and spaces only. Forbidden characters and the 11th character are blocked while typing. The name is stripped and an empty name is refused.
- Ties: the oldest score is ranked first.
- Only the 10 best scores are kept.

## Maze Generation

The mazes are generated by the **assigned A-Maze-ing package** (`mazegenerator` 2.1.0), used **as is, without any modification**. It is installed from a wheel, and it is re-installed during peer review, so the game only relies on its public interface. Our code adapts to the package, never the opposite.

**The loader.** Only one module, `maze_loader.py`, knows the package. It exposes:

```python
def process_maze(width: int, height: int, seed: int) -> Grid
```

- The generator is called with `perfect=False` (mazes with loops and almost no dead ends, which is what Pac-Man needs) and with the requested dimensions and seed. Its standard output is silenced, because it prints a warning for small mazes.
- The raw output is a matrix of integers from 0 to 15. Each integer is a bitmask of the walls of the cell: `N = 1`, `E = 2`, `S = 4`, `W = 8` (a bit set to 1 means a wall).
- The loader converts it into a `Grid` of `Cell` objects. `Cell.has_wall(direction)` answers whether there is a wall on a given side, and `Direction` (an `IntFlag`) provides the bit, the `(dx, dy)` offset and the opposite of each direction. The rest of the game never manipulates raw integers.

**Validation.** Before returning a `Grid`, the loader checks the package output:

- the dimensions are the requested ones and every value is an integer between 0 and 15;
- walls are consistent between neighbours (a wall seen from one cell is also seen from the other one);
- every open cell is reachable from the others, in particular the four corners.

**Error handling.** Any failure (exception from the package or invalid output) is turned into a single `MazeError`. The game then retries with default parameters; if that fails too, a clear message is displayed and the game exits cleanly, without traceback.

**Seeds.** The first level uses `config.seed`; each following level draws a random seed that is **stored by level index and logged**, so that any maze can be reproduced and going back to a previous level gives the same maze.

**The "42" pattern.** The package draws a "42" in the centre of mazes that are large enough (width of 14 cells and height of 10 cells or more). Its cells are completely closed (value 15) and unreachable, so they are excluded from the placement of pacgums and from the spawn position. Because this pattern can cover the centre cell depending on the dimensions, the player spawns on the open cell closest to the centre.

## Implementation

**Movement.** Entities (player and ghosts) share an abstract `Entity` class. Positions are continuous (cells per second × `dt`), which makes movement smooth. When a step crosses the centre of a cell, the entity is snapped exactly on that centre and asks `choose_direction()` where to go next (Template Method pattern: `Entity` defines the movement, each subclass decides the direction). The player buffers the wanted direction until it becomes possible and can always turn around. `dt` is capped at 0.05 s so that a frame hitch can never make an entity jump over a wall.

**Level setup.** For each level, `Game` generates the grid, places the player, puts a super-pacgum and a ghost in each corner, and picks `config.pacgums` pacgums **without replacement** among the open cells, excluding the corners, the "42" cells and the player's spawn. The count is clamped (with a log message) when there are fewer free cells than requested.

**Ghosts.** Each ghost has a mode (`WAITING`, `CHASE`, `EDIBLE`, `EATEN`). At each cell centre, a ghost picks, among the free directions, the one whose neighbouring cell is the closest to its target (greedy, like the original game, which keeps the game playable). Targets in `CHASE` mode: Blinky targets the player; Pinky targets 4 cells ahead of the player; Inky uses the vector from Blinky to 2 cells ahead of the player, doubled; Clyde targets the player when far and his own corner when close. In `EDIBLE` mode the ghost runs away from the player. Ghosts leave their corner one after another, and an eaten ghost respawns in its corner after a delay. When 10% or less of the pacgums remain, Blinky speeds up.

**Rules.** A ghost touching the player in `CHASE` mode costs a life and sends everybody back to the corners; touching an `EDIBLE` ghost scores `points_per_ghost`. The level is completed when all pacgums and super-pacgums are eaten. Score and lives are kept between levels. The game ends on victory (all levels done) or when no life is left, then the player enters a name for the highscore.

**Time limit.** <describe what happens when the level timer reaches zero>.

**HUD.** The score, the remaining lives, the current level and the remaining time are always visible during the game.

### Cheat mode

Enabled with `"cheat_mode": true` in the configuration (and from the settings). It lets a reviewer test every feature quickly:

| Key | Effect |
|---|---|
| `S` | Skip the level (win it immediately) |
| `I` | Invincibility (no life lost) |
| `F` | Freeze the ghosts |
| `L` | Add extra lives |
| `Space` | Increase the player's speed |

## General Software Architecture

### Modules

```text
pac-man.py                 entry point: parses the command line, runs the App
src/
├── cli.py                 command line: exactly one argument, reads the config file
├── config.py              Config / Level dataclasses, load_config and its validators
├── context.py             data shared by every screen: the Config and the last GameResult
├── direction.py           Direction (IntFlag): bit, offset, opposite
├── game.py                Game: levels, seeds, pacgums, score, lives, timer, collisions
├── app.py                 App: main loop and stack of states
├── states/                one class per screen
│   ├── state.py           State (abstract base class) and StateName (enum)
│   ├── main_menu.py, playing.py, pause.py, instructions.py, end.py, ...
├── maze/
│   ├── maze_loader.py     the only module that knows the assigned package
│   └── grid.py            Grid and Cell
├── entities/              Entity, Player, Ghost (+ the four ghosts)
└── rendering/             all the drawing functions (maze, entities, HUD, menus)
```

### How the pieces fit together

```text
pac-man.py ─► cli ─► config.load_config ─► Context(config, result)
     │
     └─► App (main loop, stack of states)
            ├── MainMenu ──► Highscores / Instructions / Settings
            ├── Playing ──► Game ──► Player, Ghosts, pacgums
            │                 └──► maze_loader ──► mazegenerator (assigned package)
            ├── PauseMenu ──► Instructions ──► Rules / Control keys
            └── End (game over / victory) ──► highscores
```

### The state machine

Each screen is a `State` with three methods:

- `handle_input(events)`: reads the keys of this screen and stores the player's intentions;
- `update(dt) -> StateName | None`: acts on them and returns the screen it wants to go to, or `None` to stay;
- `render(screen, font)`: draws the screen (through the functions of the `rendering` package) and never changes anything.

A state never creates or imports another screen: it only returns a **name** from the `StateName` enum. `App` is the only place that knows every screen class, which avoids circular imports and keeps each screen independent. `App` keeps a **stack** of states and only the one on top is active:

- *overlay* screens (pause menu, instructions, rules, control keys) are **pushed** on top of the current one;
- `StateName.BACK` **pops** the top screen and shows the previous one again, unchanged;
- any other request **replaces** the whole stack with a fresh state.

This is why the pause menu resumes the very same `Playing` instance (the game, the score and the timer are untouched), and why *Back* from *Rules* returns to *Instructions*, then to wherever *Instructions* was opened from.

The `Context` object, shared by all the screens, holds the configuration and the result of the last game (`GameResult`: score, victory or defeat, grid), which `Playing` writes and the end screen reads.

### Main loop

For every frame: compute `dt` (capped), read the events, call `handle_input`, `update` and `render` on the active state, flip the display, then apply the requested transition if any. The same loop runs for every screen; only the active state changes. The update chain during a game is `App` → `Playing.update(dt)` → `Game.update(dt, intents)` → `Player.update(...)` and `Ghost.update(...)`. `Game` knows nothing about keys, screens or drawing, so it can be tested without a window.

## Project Management

The project was developed by two people in a shared Git repository, with feature branches merged regularly, and a design document written together before coding (requirements, architecture, open questions).

All the management documents are in [`<project_management_directory>/`](<project_management_directory>/): timeline, progress tracking, risk analysis, team organisation, acceptance test plan and blocking points.

- **Team organisation:** who did what, how decisions were made, how conflicts were handled.
- **Tools:** Git and GitHub (branches, merges), a design document, a Makefile for the common tasks, `flake8` and `mypy` for quality.

## Resources

### References

- [pygame documentation](https://www.pygame.org/docs/)
- [Python documentation](https://docs.python.org/3/) — `argparse`, `dataclasses`, `enum`, `json`, `pathlib`, `abc`
- [`platformdirs`](https://platformdirs.readthedocs.io/)
- [`uv`](https://docs.astral.sh/uv/), [`flake8`](https://flake8.pycqa.org/), [`mypy`](https://mypy.readthedocs.io/)
- *The Pac-Man Dossier*, by Jamey Pittman — behaviour of the original ghosts: <https://pacman.holenet.info/>
- *Game Programming Patterns*, by Robert Nystrom — [State](https://gameprogrammingpatterns.com/state.html) and [Game Loop](https://gameprogrammingpatterns.com/game-loop.html)

### Use of AI

AI (Claude) was used as a tutor and reviewer, never as a replacement for understanding. All the code was read, tested and can be explained by the authors.

- **Explanations of concepts:** bitmask encoding of the walls, `IntFlag`, dataclasses, `Enum`, circular imports, a state machine with a stack of states.
- **Design discussions:** the structure of the maze loader (what to validate and why), the `StateName` mechanism and the stack of states, how to share the end-of-game result between screens.
- **Code review and debugging:** finding bugs in our code (a missing import, inverted comprehension order, the neighbour test in the wall-consistency check, duplicated pacgums caused by random sampling with replacement, a state recreated at every frame) and explaining their cause.
- **Generated drafts that we adapted:**  the first draft of this README.
- **Not delegated:** the design document, the architecture decisions, the integration of the maze generator, and the testing of the game.


# Pac-Man — Project Management

*Authors: tmattela, Srosu*


---

## 1. Team organisation

### 1.1 Who did what

| Area | tmattela | Srosu |
|---|---|---|
| Design document (architecture, config, highscore, ghosts, UI) | ✔ (together) | ✔ (together) |
| Maze: integration of the assigned package, `Grid` / `Cell` / `Direction`, validation, level seeds | ✔ | |
| Pacgums and super-pacgums (placement, scoring, level progression) | ✔ | |
| HUD, menus (main, pause, instructions, rules, keys), end screen | ✔ | |
| State machine (`StateName`, stack of states, transitions, `Context`) | ✔ | |
| Entities: `Entity`, `Player`, ghosts (`Blinky`, `Pinky`, `Inky`, `Clyde`) and their rendering | | ✔ |
| Algorithms of all the ghosts | | ✔ |
| Collision logic | | ✔ |
| Highscore system (load, validate, atomic save) | | ✔ |
| Pygame main loop and global architecture | | ✔ |
| Configuration file and command line |  | ✔ |
| Makefile, linting (flake8 / mypy), docstrings | ✔ |  |
| README | ✔ |  |
| Build and Deployment |  | ✔ |


### 1.2 How decisions were made

- The architecture was agreed **before coding**, in a shared design document.
- Day-to-day decisions: **chat sessions**.
- Disagreements and how they were settled: **Not many, quick discussion and common agreement**.

### 1.3 Workflow

- One shared Git repository, feature branches (e.g. `test/states`, `context`, `test/highscore`, `Entities`, `Ghosts`), merged regularly into the main branch.
- Merge conflicts were resolved with the editor's three-way merge view, after checking both sides' intent.
- A Kanban board was used to track tasks (screenshot in this directory).

---

## 2. Timeline and progress

### 2.1 Planned phases vs. actual

| Phase | Planned |
|---|---|
| Design document | Done |
| Maze generation and loader | Done |
| Entities and player movement | Done |
| Ghosts and collisions | Done |
| States, menus and HUD | Done |
| Game loop integration | Done |
| Highscore | Done |
| tests | Done |
| README and project-management documents | Done |
| Build and deployment (itch.io / Steam) | To do |

### 2.2 Comparison with the plan

The project globally went **faster than planned**. The game loop took less time than expected: once the entities and the states were developed, the integration became natural and logical.

Remaining work at the time of writing: build and deployment, final testing, README and documents.

---

## 3. Project analysis and technical choices

| Choice | Reason | Alternative considered |
|---|---|---|
| **pygame** for window, drawing and input | Simple, well documented, enough for a 2D game | Other graphics library. Compatibility with the "MLX-equivalent" constraint of the subject|
| **Assigned maze package used as-is** (`perfect=False`) | Required by the subject; loops and few dead ends suit Pac-Man | Writing our own generator (not allowed) |
| Single loader module (`maze_loader.py`) with validation | Isolates the package; errors become a clean `MazeError` | Direct use of the package everywhere |
| `Grid` / `Cell` / `Direction` abstractions | The rest of the code never touches raw bitmasks | Raw integer matrix |
| **State machine** with `StateName` enum and a **stack** of states | No circular imports; pause resumes the exact same game | Direct references between screens |
| `Game` logic separated from rendering | Game can be reasoned about and tested without a window | Logic inside draw functions |
| Continuous coordinates, snapping on cell centres | Smooth movement and exact turning decisions | Cell-by-cell movement |
| Per-level seeds, first from config, others random but stored | Reproducible levels | Fully random each time |
| JSON highscore in the user data folder, atomic write | Human-readable, survives crashes, no repo pollution | SQLite, file in the repository |
| Configuration validated key by key with defaults | One bad value never blocks the game | All-or-nothing configuration |

---

## 4. Risk analysis

*(Probability / impact: L = low, M = medium, H = high.)*

| # | Risk | P | I | Mitigation | Outcome |
|---|---|---|---|---|---|
| R1 | The graphics library does not satisfy the "MLX-equivalent" constraint | M | H | Discuss with the pair, read the subject, ask the staff | Use of Pygame|
| R2 | The assigned maze package returns unexpected data (e.g. the "42" pattern blocks the spawn) | M | H | Validate the output, exclude closed cells from items, choose a safe spawn | Handled in the loader and item placement |
| R3 | Invalid configuration or corrupted files crash the game | H | H | Per-key validation, defaults, clamping, clear messages, backup of corrupted highscore | Mostly handled, hardening in progress |
| R4 | Integration problems between two developers' code (circular imports, diverging architecture) | H | M | Design document first, `StateName` mechanism, shared `Context` | Happened (circular imports), solved |
| R5 | Git conflicts and diverging branches | M | M | Small feature branches, regular merges, review of conflicts | Happened, solved |
| R6 | Performance on large mazes (50×50) | L | M | Cache the maze surface, cap `dt` | Handled |
| R7 | Deployment takes longer than expected (account, fees, review delays) | M | M | Prefer a free platform (itch.io) with a draft/restricted page, start early | Updated on itch.io |
| R8 | Time lost on polishing instead of mandatory features | M | M | Prioritise subject requirements, then extras | Done |

---

## 5. Acceptance test plan

Tests were performed **manually** by playing the game and by feeding deliberately wrong configurations.

| ID | Feature | Scenario | Expected |
|---|---|---|---|
| T1 | Command line | No argument / two arguments / missing file | Clear message, no traceback |
| T2 | Config | Comments, unknown key, wrong types, out-of-range values | Default or clamped value, message logged, game starts |
| T3 | Config | Invalid JSON, empty file, root is not an object | Defaults used, game starts |
| T4 | Maze | Same seed twice; levels 1 to 10; sizes 10×10 and 50×50 | Same maze for the same seed; all levels playable |
| T5 | Movement | Turning in corridors, walls, U-turn | Player never crosses a wall; buffered turns work |
| T6 | Pacgums | Eat every pacgum | Score increases, pacgum disappears, level ends when none left |
| T7 | Super-pacgums | Eat in a corner | Ghosts become edible, then return to normal |
| T8 | Ghosts | Contact in chase / edible mode | Life lost / ghost eaten and respawned |
| T9 | Level time limit | Let the timer reach zero | Game over |
| T10 | Lives | Lose all lives | Game over screen |
| T11 | Victory | Clear level 10 | Victory screen |
| T12 | Pause | Pause, instructions, resume | Game and timer frozen, same state resumed |
| T13 | Highscore | Enter name, restart, corrupt the file | Top 10 persists; corrupted file does not crash |
| T14 | Name entry | Empty, too long, forbidden characters | Refused or blocked |
| T15 | Cheat mode | Each cheat key with `cheat_mode` on and off | Works only when enabled |
| T16 | Quality | `make lint` (flake8 and mypy with the mandatory flags) | No error |

---

## 6. Bugs found and fixed

| ID | Bug | Cause | Fix |
|---|---|---|---|
| B1 | Some pacgums were not eaten or counted | Sampled with replacement (duplicates) and frame-time spikes | `random.sample` (no duplicates), `dt` capped at 0.05 s |
| B2 | `'Game' object has no attribute 'player'` | Pacgums initialised before the player existed | Create the player first |
| B3 | `font not initialized` | Fonts created before `pygame.init()` | Lazy `get_font` with a cache |
| B4 | `ImportError: attempted relative import with no known parent package` | A module of the package run as a script | Run through the entry point |
| B5 | Maze not redrawn after a level change | Maze surface cached without checking the grid | Cache keyed on grid identity |
| B6 | End screen recreated every frame, value lost | New instance built at each transition | Reuse the instance, return `None` to stay |
| B7 | `Item "None" ... has no attribute` (mypy) | Optional attributes not narrowed | Narrow once in the factory and pass the result |
| B8 | Maze consistency check wrong | Compared a cell with itself; wrong bounds in the reachability search | Rewrote `is_consistent` and `reachable_from` |
| B9 | Circular imports between screens | Screens importing each other | Screens return a `StateName`; `App` is the only one building states |
| B10 | Items and spawn on closed "42" cells | The generator closes those cells completely | Exclude cells with all four walls from item placement |



---

## 7. Blocking points and conflicts

| Point | Description | Resolution |
|---|---|---|
| Circular imports between screens | Direct references between states made the modules depend on each other | `StateName` enum and a central `App` |
| Passing data between screens | The end screen needed the score and the result | Shared `Context` with a `GameResult` |
| Git: divergent branches and merges | Two people working on branches that diverged, conflicts between `context` and `test/highscore` | Merge with the three-way editor, review each conflict |
| Graphics constraint | The subject asks for MLX-equivalent functions, which pygame drawing helpers do not match | **[? decision]** |
| The "42" pattern in the maze | Spawn and items could land on closed cells | Exclusion in item placement, safe spawn |
| Disagreements inside the team | None | None |

---

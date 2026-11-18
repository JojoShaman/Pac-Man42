PAC-MAN - 42 project
====================

LAUNCH
  Linux : double-click PacMan, or run ./PacMan from a terminal.
          If it does not start, run: chmod +x PacMan
  macOS : the game is not signed by Apple. If macOS blocks it, run:
          xattr -dr com.apple.quarantine <folder>
          or allow it in System Settings > Privacy & Security.

CONTROLS
  Up              Arrow up / W / Z
  Left            Arrow left / A / Q
  Down            Arrow down / S
  Right           Arrow right / D
  Esc             Pause / Resume
  Enter           Validate in menus

CHEAT KEYS
  N               Next level
  P               Previous level
  +               Add 1 life
  -               Remove 1 life
  1               Immortality (press again to disable)
  2               Super speed (press again to disable)
  3               Freeze ghosts (press again to unfreeze)

RULES
  Eat every pac-gum to clear the level.
  Super pac-gums make ghosts edible for a few seconds.
  Eat an edible ghost for bonus points.
  A ghost touching you costs one life.
  Each level has a time limit.
  When time runs out, it's game over.
  Lose all your lives and it's game over.
  Clear all 10 levels to win.

CONFIGURATION
  Edit config.json, next to the executable. Lines starting with #
  are comments. Missing or invalid values fall back to their default,
  out-of-range values are clamped. If the file is missing or is not
  valid JSON, the game starts with the default configuration.

  Key                      Default  Range
  lives                    3        1 - 5
  pacgums                  42       10 - 1000
  points_per_pacgum        10       0 - 1000
  points_per_super_pacgum  50       0 - 5000
  points_per_ghost         200      0 - 20000
  level_max_time           90       30 - 600 (seconds)
  seed                     42       positive integer (first level only)
  highscore_filename       highscore.json - file name only, no path
  levels                   10 levels, each with width / height (10 - 50)

HIGHSCORES
  The top 10 is saved in your user data folder:
  Linux : ~/.local/share/[PacMan]/
  macOS : ~/Library/Application Support/[PacMan]/
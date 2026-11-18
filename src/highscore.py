import json
import os
import re
import sys
from pathlib import Path
from typing import Any
from platformdirs import user_data_path
from .context import Context
import logging

def get_highscore_path(filename: str) -> Path:
    """Return the highscore file path in the user data folder."""
    folder = user_data_path("PacMan")
    folder.mkdir(parents=True, exist_ok=True)
    return Path(folder / filename)


def _validate_highscore_content(
        scores: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """Drop invalid and duplicate entries"""
    def _sort_highscores() -> list[dict[str, Any]]:
        """Sort by score (descending) and keep the top 10."""
        hs = sorted(
            _validate_scores(),
            key=lambda player: player["score"],
            reverse=True)
        return hs

    def _remove_duplicates() -> list[dict[str, Any]]:
        """Remove entries sharing the same name, return the 10 best sorted."""
        seen: set[Any] = set()
        unique: list[dict[str, Any]] = []
        for entry in _sort_highscores():
            key = entry.get("name")
            if key in seen:
                continue
            seen.add(key)
            unique.append(entry)
        return unique[:10]

    def _validate_scores() -> list[dict[str, Any]]:
        """Keep entries with a valid name (1-10 alnum/space) and score."""
        ret = []
        for player in scores:
            if (not re.fullmatch(r"[A-Za-z0-9 ]{1,10}", player["name"])
                    or player["score"] > sys.maxsize):
                continue
            ret.append(player)
        return ret
    return _remove_duplicates()


def load_highscore(context: Context) -> None:
    """Load the highscores into the context; back up a corrupted file."""
    highscores: list[dict[str, Any]] = []
    bak_path = context.file_path.with_name(context.file_path.name + ".bak")
    try:
        with open(context.file_path, "r", encoding="utf-8") as f:
            highscores = json.load(f)
            context.highscores = _validate_highscore_content(highscores)
    except ValueError as e:
        os.replace(context.file_path, bak_path)
        logging.error(e)
        logging.warning("saved backup to:", bak_path)
    except OSError as e:
        logging.error(e)


def new_score(context: Context, new_: dict[str, Any]) -> None:
    """Add a score and save the top 10 atomically (.tmp then replace)."""
    context.highscores.append(new_)
    tmp_path = context.file_path.with_name(context.file_path.name + ".tmp")
    with open(tmp_path, "w") as f:
        json.dump(
            _validate_highscore_content(context.highscores),
            f, indent=2)
    os.replace(tmp_path, context.file_path)

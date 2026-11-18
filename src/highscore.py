from platformdirs import user_data_path
from .context import Context
import json
from typing import Any
from pathlib import Path
import os
import sys
import re

def get_highscore_path(filename: str) -> Path:
    folder = user_data_path("PacMan")
    folder.mkdir(parents=True, exist_ok=True)
    return folder / filename


def _validate_highscore_content(scores: list[dict[str, Any]]) -> list[dict[str, Any]]:
    def _sort_highscores() -> list[dict[str, Any]]:
        hs = sorted(
            _remove_duplicates(),
            key=lambda player: player["score"],
            reverse=True)
        return hs[:10]

    def _remove_duplicates() -> list[dict[str, Any]]:
        seen: set[tuple[Any, Any]] = set()
        unique: list[dict[str, Any]] = []
        for entry in _validate_scores():
            key = (entry.get("name"), entry.get("score"))
            if key in seen:
                continue
            seen.add(key)
            unique.append(entry)
        return unique

    def _validate_scores() -> list[dict[str, Any]]:
        ret = []
        for player in scores:
            if not re.fullmatch(r"[A-Za-z0-9]{1,10}", player["name"]) or player["score"] > sys.maxsize:
                continue
            ret.append(player)
        return ret
    return _sort_highscores()

def load_highscore(context: Context) -> None:
    try:
        with open(context.file_path, "r", encoding="utf-8") as f:
            highscores: list[dict[str, Any]] = json.load(f)
        context.highscores = _validate_highscore_content(highscores)
    except ValueError as e:
        print(e)
    except OSError as e:
        print(e)

def new_score(context: Context, new_: dict[str, Any]) -> None:
    new_hs: list[dict[str, Any]] = []
    context.highscores.append(new_)
    tmp_path = context.file_path.with_name(context.file_path.name + ".tmp")
    with open(tmp_path, "w") as f:
        json.dump(
            _validate_highscore_content(context.highscores),
            f, indent=2)
    os.replace(tmp_path, context.file_path)
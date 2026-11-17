from platformdirs import user_data_path
from .context import Context
import json
from typing import Any
from pathlib import Path
import os

def get_highscore_path(filename: str) -> Path:
    folder = user_data_path("PacMan")
    folder.mkdir(parents=True, exist_ok=True)
    return folder / filename

def load_highscore(context: Context) -> None:
    try:
        with open(context.file_path, "r", encoding="utf-8") as f:
            highscores = json.load(f)
        context.highscores = highscores
    except ValueError as e:
        print(e)
    except OSError as e:
        print(e)

def new_score(context: Context, new_: dict[str, Any]) -> None:
    new_hs: list[dict[str, Any]] = []
    if context.highscores:
        for player in context.highscores:
            if new_ not in new_hs and new_["score"] > player["score"]:
                new_hs.append(new_)
            new_hs.append(player)
    if len(new_hs) < 10 and new_ not in new_hs:
        new_hs.append(new_)
    tmp_path = context.file_path.with_name(context.file_path.name + ".tmp")
    with open(tmp_path, "w") as f:
        json.dump(new_hs, f, indent=2)
    os.replace(tmp_path, context.file_path)
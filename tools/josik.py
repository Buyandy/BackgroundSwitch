import json
from os import getcwd


def get_setting() -> dict:
    path: str = "data/setting.json"
    with open(path, "r") as file:
        data = json.load(file)
        return data

def save_setting(data: dict) -> None:
    path: str = "data/setting.json"
    with open(path, "w") as file:
        json.dump(data, file, indent=2, ensure_ascii=False)


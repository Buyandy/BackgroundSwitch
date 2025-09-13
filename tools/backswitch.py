import ctypes
from os import listdir
from random import randint
import tools.josik as josik

path_image: str = ""

def _ready() -> None:
    global path_image
    path_image = josik.get_setting()["main_path"]


def changeBack(path: str):
    ctypes.windll.user32.SystemParametersInfoW(20, 0, path , 0)


def get_files() -> list:
    return listdir(path_image)


def randomChangeBack() -> str:
    images: list = get_files()
    randimag: str = images[randint(0, len(images)-1)]
    changeBack(path_image+"/"+randimag)
    return randimag


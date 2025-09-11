import ctypes
from os import listdir
from random import randint

PATH_IMAGE: str = "C:/Users/Buyandy/Pictures/AnimeBackgrounds"

def changeBack(path: str):
    ctypes.windll.user32.SystemParametersInfoW(20, 0, path , 0)

def get_files() -> list:
    return listdir(PATH_IMAGE)

def randomChangeBack() -> str:
    images: list = get_files()
    randimag: str = images[randint(0, len(images)-1)]
    changeBack(PATH_IMAGE+"/"+randimag)
    return randimag


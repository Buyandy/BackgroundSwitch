from PIL import Image
import PIL
from os import getcwd
import tools.josik as josik

current_image_path: str = ""


def _ready() -> None:
    global current_image_path
    data = josik.get_setting()
    current_image_path = data["current_image_path"]
    

def currentImage(path):
    global current_image_path
    data = josik.get_setting()
    data["current_image_path"] = path
    josik.save_setting(data)
    current_image_path = path

# Сформирование имения под тип фильтра
def createName(path: str, name_filter: str) -> str:
    file_name: str = path.split("/")[-1]
    new_name: str = name_filter+"_"+file_name
    return new_name


# Для сохранения изображении
def saveImage(image, name_filter: str) -> str:
    name = createName(current_image_path, name_filter)
    image.save("outputImages/"+name)
    currentImage(str(getcwd())+"/"+"outputImages/"+name)
    return str(getcwd())+"/"+"outputImages/"+name




# _________ Внизу все фильтры _________



def editInGray() -> str:
    image = Image.open(current_image_path)
    gray_image = image.convert("L")
    save_path: str = saveImage(gray_image, "GRAY")
    return save_path







ALL_FILTERS: dict = {
    "Gray": editInGray,
}
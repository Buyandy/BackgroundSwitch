from PIL import Image
import PIL
from os import getcwd

current_image_path: str = ""




def currentImage(path):
    global current_image_path
    current_image_path = path

# Сформирование имения под тип фильтра
def createName(path: str, name_filter: str) -> str:
    file_name: str = path.split("/")[-1]
    new_name: str = name_filter+"_"+file_name
    return new_name


# Для сохранения изображении
def saveImage(image, path: str, name_filter: str) -> str:
    name = createName(path, name_filter)
    image.save("outputImages/"+name)
    return "outputImages/"+name




# _________ Внизу все фильтры _________



def editInGray() -> str:
    image = Image.open(current_image_path)
    gray_image = image.convert("L")
    save_path: str = str(getcwd())+"/"+saveImage(gray_image, current_image_path, "GRAY")
    print(save_path)
    return save_path


ALL_FILTERS: dict = {
    "Gray": editInGray,
}
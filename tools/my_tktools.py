from tools.backswitch import randomChangeBack
from PIL import Image, ImageDraw



def on_button_click(label):
    """
    Вызывается при нажатии кнопки. 
    Изменяет текст метки (label), чтобы отразить изменение обоев, 
    используя результат функции randomChangeBack().
    """
    out_text: str = randomChangeBack()
    label.config(text=f"Обои сменились на {out_text}")



def create_image():
    # Простая иконка (можно заменить на свою)
    image = Image.new('RGB', (64, 64), color=(0, 120, 215))
    d = ImageDraw.Draw(image)
    d.rectangle((16, 16, 48, 48), fill=(255, 255, 255))
    return image
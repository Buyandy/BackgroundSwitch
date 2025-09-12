from tools.backswitch import randomChangeBack, changeBack, PATH_IMAGE
from PIL import Image, ImageDraw, ImageTk
from tkinter import filedialog, messagebox
import tkinter as tk
import ctypes
from tools.editImage import currentImage

import win32gui
import win32.lib.win32con as win32con



def hide_console():
    the_program_to_hide = win32gui.GetForegroundWindow()
    win32gui.ShowWindow(the_program_to_hide , win32con.SW_HIDE)




def show_image(image_frame, file_path):
    
    if file_path:
        # Очищаем предыдущее изображение
        for widget in image_frame.winfo_children():
            widget.destroy()
        
        # Загружаем новое изображение
        image = Image.open(file_path)
        image.thumbnail((600, 400))  # Масштабируем
        photo = ImageTk.PhotoImage(image)
        
        # Создаем Label внутри frame
        img_label = tk.Label(image_frame, image=photo)
        img_label.pack(pady=10)
        img_label.mainloop()
        
        
    

     


# изменение текста выводящие смену обои, принимаеться сам label и название обои
def message_from_label(label, name):
     label.config(text=f"Обои сменились на {name}")


def on_button_click(label, image_frame):
    """
    Вызывается при нажатии кнопки. 
    Изменяет текст метки (label), чтобы отразить изменение обоев, 
    используя результат функции randomChangeBack().
    """
    out_text: str = randomChangeBack()
    message_from_label(label, out_text)
    currentImage(PATH_IMAGE+"/"+out_text)
    show_image(image_frame, PATH_IMAGE+"/"+out_text)



def create_image():
    # Простая иконка (можно заменить на свою)
    image = Image.new('RGB', (64, 64), color=(0, 120, 215))
    d = ImageDraw.Draw(image)
    d.rectangle((16, 16, 48, 48), fill=(255, 255, 255))
    return image


# выбор файла и изменения
def choose_files(label, image_frame):
        file: str = filedialog.askopenfilename(title="Выберите фон", filetypes=[
             ("Фото", "*.jpeg *.jpg *.png")], initialdir=PATH_IMAGE)
        if file:
            def check_type(): # функция для проверки типа файла на фото
                file_type: str = file.split(".")[-1]
                right_types: list[str] = ["jpg", "jpeg", "png"]
                for i in right_types:
                     if i == file_type:
                          return True
                return False


            if check_type():
                file_name: str = file.split("/")[-1]
                changeBack(file)
                message_from_label(label, file_name)
                currentImage(file)
                show_image(image_frame, file)
            else:
                 messagebox.showerror("еррор?", "Не тот тип файла! \nДоступны только (jpeg, jpg, png)!")




def minimize_all_windows(root):
    # Отправляем команду "Свернуть все"
    ctypes.windll.user32.keybd_event(0x5B, 0, 0, 0)  # Win
    ctypes.windll.user32.keybd_event(0x44, 0, 0, 0)  # D
    ctypes.windll.user32.keybd_event(0x44, 0, 2, 0)  # Release D
    ctypes.windll.user32.keybd_event(0x5B, 0, 2, 0)  # Release Win
    root.iconify()
    root.iconify()
    root.iconify()
    root.iconify()
    root.deiconify()
    root.deiconify()
    root.deiconify()
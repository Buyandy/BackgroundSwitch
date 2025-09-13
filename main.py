import tkinter as tk
from tkinter import ttk
from tools.backswitch import randomChangeBack, changeBack
import tools.my_tktools as mytools
import tools.editImage as editImage
from sys import argv


# Новое:
import threading
import pystray

class Button(ttk.Button):
    pass



#  Глобальные переменные!

is_open_edit_root: bool = False # Открыт ли окно редактора фото






def _ready(image_frame, root) -> None:
    
    changeBack(editImage.current_image_path)
    

    # ЭТА КОМАНДА ВСЕГДА ДОЛЖЕН БЫТЬ ВНИЗУ!!!!!!!!!!!!!!!!!!!
    mytools.show_image(image_frame, editImage.current_image_path)



def main():

    # Скрывает консоль при передачи аргумента --no-console--
    if len(argv) > 1:
        print(argv)
        if argv[1] == "--no-console--":
            mytools.hide_console()



    editImage._ready()# Старт файла editImage.py


    root = tk.Tk()
    root.title("Просто сменщик обоев")
    root.geometry("800x600")
    root.resizable(False, False)

    label = ttk.Label(root, text="Сменьщик обоев!")
    label.pack(pady=5)

    # Создание новой области для размещения фото
    
    image_frame = tk.Frame(root, relief="ridge", width=600, height=300, bg="#636363")
    image_frame.pack(pady=20, padx=20, fill="both", expand=True)
    image_frame.pack_propagate(False)
    image_frame.update_idletasks()
    image_frame.update()

    style = ttk.Style()
    style.theme_use("vista")

    

    

    # Кнопка для смены обоев, вызывает функцию из mytools и обновляет label
    button = Button(root, text="Сменить обои", command=lambda: mytools.on_button_click(label, image_frame))
    button.pack(padx=10, side=tk.RIGHT)

   # Кнопка для выбора файлов
    file_button = Button(root, text="Выбрать файлы", 
                             command=lambda:mytools.choose_files(label, image_frame))# Кнопка вызывающий выбор файлов
    file_button.pack(padx=10, pady=30, side=tk.RIGHT)

    # Кнопка перехода к рабочему столу (свернуть все окна)
    roll_button = Button(root, text="Свергнуть все!", command=lambda:mytools.minimize_all_windows(root))
    roll_button.pack(padx=10, side=tk.RIGHT)


    
    
    
    def edit_button_click(): # Функция для открытия нового окна для редактора фото
        global is_open_edit_root
        if not is_open_edit_root:
            is_open_edit_root = True
            edit_root = tk.Toplevel(root)
            edit_root.title("Редактор фото")
            edit_root.geometry("400x300")
            edit_root.resizable(False, False)
            edit_root.focus_set()

            def destroy_window():
                global is_open_edit_root
                is_open_edit_root = False
                edit_root.destroy()
            
            edit_root.protocol('WM_DELETE_WINDOW', destroy_window)


            def show_selected(): # Для показа что выбрал юзер когда нажал применить
                selected = listbox.curselection()
                if selected:
                    index = selected[0]
                    item = listbox.get(index)
                    print(f"Выбрано: {item}")
                    path = editImage.ALL_FILTERS[item]()
                    changeBack(path)
                    mytools.show_image(image_frame, path)
                    
                else:
                    print("Ничего не выбрано")

            # Создание и редактирования области для списка
            list_frame = ttk.LabelFrame(edit_root, text="Список элементов", padding=2)
            list_frame.pack(pady=20, padx=20, fill=tk.BOTH, expand=True)
            scrollbar = ttk.Scrollbar(list_frame)
            scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
            listbox = tk.Listbox(list_frame, yscrollcommand=scrollbar.set, height=8)
            listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
            scrollbar.config(command=listbox.yview)

            # Создание кнопок
            button = Button(edit_root, text="Применить", command=show_selected)
            button.pack(padx=10, pady=20, side=tk.RIGHT)

            button2 = Button(edit_root, text="Выход", command=destroy_window)
            button2.pack(padx=10, pady=20, side=tk.RIGHT)


            # Добавления элементов в созданный список
            items = editImage.ALL_FILTERS.keys()

            for item in items:
                listbox.insert(tk.END, item)

            edit_root.mainloop()





    # Кнопка для наложения фильтра в фото
    edit_button = Button(root, text="Редактировать", command=edit_button_click)
    edit_button.pack(padx=10, side=tk.LEFT)





    # --- Свернуть в трей ---
    def hide_window():
        root.withdraw()
        show_tray_icon()

    def show_window(icon=None, item=None):
        root.deiconify()
        if icon:
            icon.stop()

    def show_tray_icon():
        icon = pystray.Icon("name", mytools.create_image(), "Сменщик обоев", menu=pystray.Menu(
            pystray.MenuItem("Открыть", show_window),
            pystray.MenuItem("Выход", lambda icon, item: (icon.stop(), root.destroy()))
        ))
        threading.Thread(target=icon.run, daemon=True).start()

    # Добавим кнопку "Свернуть в трей"
    #tray_button = ttk.Button(root, text="Свернуть в трей", command=hide_window)
    #tray_button.pack(pady=10)
    root.protocol('WM_DELETE_WINDOW', hide_window)  # При закрытии - в трей


 
    



    _ready(image_frame, root) # Старт main.py

    root.mainloop()

if __name__ == "__main__":
    main()
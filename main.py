import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from tools import backswitch
import tools.my_tktools as mytools
import tools.editImage as editImage
from sys import argv
import tools.josik as josik



# Новое:
import threading
import pystray

class Button(ttk.Button):
    pass



#  Глобальные переменные!

is_open_edit_root: bool = False # Открыт ли окно редактора фото






def _ready(image_frame, root) -> None: # Cтартовая команда

    backswitch.changeBack(editImage.current_image_path)
    

    # ЭТА КОМАНДА ВСЕГДА ДОЛЖЕН БЫТЬ ВНИЗУ!!!!!!!!!!!!!!!!!!!
    mytools.show_image(image_frame, editImage.current_image_path)



def main():
    backswitch._ready(messagebox.showwarning)# Старт файла backswitch.py
    editImage._ready()# Старт файла editImage.py
    



    # Скрывает консоль при передачи аргумента --no-console--
    if len(argv) > 1:
        print(argv)
        if argv[1] == "--no-console--":# При первом аргументе
            mytools.hide_console()
    # ------------------------------------------------------





    # ---- СТАРТОВЫЕ НАСТРОЙКИ ПРИЛОЖЕНИЯ ----
    root = tk.Tk()
    root.title("Просто сменщик обоев")
    root.geometry("800x600")
    root.resizable(False, False)
    label = ttk.Label(root, text="Сменьщик обоев!")
    label.pack(pady=5)
    style = ttk.Style()
    style.theme_use("vista")
    # ----------------------------------------



    # ---- Создание новой области для размещения фото ----
    image_frame = tk.Frame(root, relief="ridge", width=600, height=300, bg="#636363")
    image_frame.pack(pady=20, padx=20, fill="both", expand=True)
    image_frame.pack_propagate(False)
    image_frame.update_idletasks()
    image_frame.update()
    # ----------------------------------------------------




  

    

# Внизу все кнопки, и функции которые вызываються ими находяться в отдельном файле my_tktools.py
  
#------------------------------------------------------------------------------------
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
#--------------------------------------------------------------------------------------

    
    
    # ---- СОЗДАНИЕ РЕДАКТОРА ----
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
                    backswitch.changeBack(path)
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

    
    edit_button = Button(root, text="Редактировать", command=edit_button_click)# Кнопка для наложения фильтра в фото
    edit_button.pack(padx=10, side=tk.LEFT)
    # ----------------------------


    # ---- СОЗДАНИЕ НАСТРОЙКИ ----
    def setting_button_click():

        # Вспомогательные функции для создание обьектов
        def new_frame() -> ttk.Frame:# Создать область
            frame = ttk.Frame(setting_root, relief="groove", padding=5)
            frame.pack(pady=10, fill=tk.X)
            return frame
        

        def new_label_info(text: str) -> ttk.Label:# Создать текст описывающий область
            label = ttk.Label(frame1, text=text)
            label.pack(padx=5, pady=5)
            return label
        

        def new_button(text: str, func) -> ttk.Button:# Создать кнопку
            button = ttk.Button(frame1, text=text, command=func)
            button.pack(side="left", padx=5)
            return button
        

        def new_label(text: str) -> ttk.Label:# Создать текст описывающий функцию раздела настройки
            label = ttk.Label(frame1, text=text)
            label.pack(side=tk.LEFT, padx=5)
            return label
        # --------------------------------------------------------------------

        setting_root = tk.Toplevel(root)
        setting_root.geometry("500x500")
        setting_root.resizable(False, False)
        setting_root.grab_set()
        setting_root.focus_set()

        # Получения данных из файла настройки
        data: dict = josik.get_setting()


        # 1 строка
        def on_click_btn1():
            path = mytools.choose_dir()
            data = josik.get_setting()
            data["main_path"] = path
            backswitch.path_image = path
            josik.save_setting(data)
            lbl1.config(text=path)
        frame1 = new_frame()
        lbl = new_label_info("Главная директория содержащий фоны")
        btn1 = new_button("Выбрать", on_click_btn1)
        lbl1 = new_label(backswitch.path_image)

        # 2 line

        
        setting_root.mainloop()
    

    setting_button = Button(root, text="Настройки", command=setting_button_click)
    setting_button.pack(padx=10, side=tk.LEFT)
    # ----------------------------





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

    if len(argv) > 1:
        if argv[1] == "--no-console--":
            root.protocol('WM_DELETE_WINDOW', hide_window)  # При закрытии - в трей
    # -----------------------


 
    



    _ready(image_frame, root) # Старт main.py
    root.mainloop()



if __name__ == "__main__":
    main()
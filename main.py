import tkinter as tk
from tkinter import ttk
from tools.backswitch import randomChangeBack, changeBack
import tools.my_tktools as mytools
import tools.editImage as editImage

# Новое:
import threading
import pystray





def main():
    root = tk.Tk()
    root.title("Просто сменщик обоев")
    root.geometry("800x600")
    root.resizable(False, False)

    label = ttk.Label(root, text="Привет, Tkinter!")
    label.pack(pady=5)

    # Создание новой области для размещения фото
    
    image_frame = ttk.Frame(root, relief="ridge", width=600, height=300)
    image_frame.pack(pady=20, padx=20, fill="both", expand=True)
    image_frame.pack_propagate(False)
    image_frame.update_idletasks()
    image_frame.update()

    style = ttk.Style()
    style.theme_use("vista")



    

    # Кнопка для смены обоев, вызывает функцию из mytools и обновляет label
    button = ttk.Button(root, text="Сменить обои", command=lambda: mytools.on_button_click(label, image_frame))
    button.pack(padx=10, side=tk.RIGHT)

   # Кнопка для выбора файлов
    file_button = ttk.Button(root, text="Выбрать файлы", 
                             command=lambda:mytools.choose_files(label, image_frame))# Кнопка вызывающий выбор файлов
    file_button.pack(padx=10, pady=30, side=tk.RIGHT)

    # Кнопка перехода к рабочему столу (свернуть все окна)
    roll_button = ttk.Button(root, text="Свергнуть все!", command=lambda:mytools.minimize_all_windows(root))
    roll_button.pack(padx=10, side=tk.RIGHT)



    def edit_button_click():
        edit_root = tk.Toplevel(root)
        edit_root.title("Редактор фото")
        edit_root.geometry("400x300")
        edit_root.resizable(False, False)


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
        button = ttk.Button(edit_root, text="Применить", command=show_selected)
        button.pack(padx=10, pady=20, side=tk.RIGHT)

        button2 = ttk.Button(edit_root, text="Выход", command=edit_root.destroy)
        button2.pack(padx=10, pady=20, side=tk.RIGHT)


        # Добавления элементов в созданный список
        items = editImage.ALL_FILTERS.keys()

        for item in items:
            listbox.insert(tk.END, item)

        edit_root.mainloop()





    # Кнопка для наложения фильтра в фото
    edit_button = ttk.Button(root, text="Редактировать", command=edit_button_click)
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
    #root.protocol('WM_DELETE_WINDOW', hide_window)  # При закрытии - в трей


 
    





    root.mainloop()

if __name__ == "__main__":
    main()
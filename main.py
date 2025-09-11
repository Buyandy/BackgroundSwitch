import tkinter as tk
from tkinter import ttk
from tools.backswitch import randomChangeBack
import tools.my_tktools as mytools

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
    image_frame = tk.Frame(root, relief="sunken", bd=2, bg="black", width=600, height=400)
    image_frame.pack(pady=20, padx=20, fill="both", expand=True)
    image_frame.pack_propagate(False)

    style = ttk.Style()
    style.theme_use("vista")



    

    # Кнопка для смены обоев, вызывает функцию из mytools и обновляет label
    button = ttk.Button(root, text="Сменить обои", command=lambda: mytools.on_button_click(label, image_frame))
    button.pack(pady=10, side=tk.RIGHT)

   # Кнопка для выбора файлов
    file_button = ttk.Button(root, text="Выбрать файлы", 
                             command=lambda:mytools.choose_files(label, image_frame))# Кнопка вызывающий выбор файлов
    file_button.pack(padx=20, pady=20, side=tk.RIGHT)

    # Кнопка перехода к рабочему столу (свернуть все окна)
    roll_button = ttk.Button(root, text="Свергнуть все!", command=mytools.minimize_all_windows)
    roll_button.pack(padx=10, side=tk.RIGHT)






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
import tkinter as tk
from tkinter import ttk
from tools.backswitch import randomChangeBack
import tools.my_tktools as mytools

# Новое:
import threading
import pystray
from tkinter import filedialog




def main():
    root = tk.Tk()
    root.title("Просто сменщик обоев")
    root.geometry("300x200")
    root.resizable(False, False)

    style = ttk.Style()
    style.theme_use("vista")

    label = ttk.Label(root, text="Привет, Tkinter!")
    label.pack(pady=20)

    

    # Кнопка для смены обоев, вызывает функцию из mytools и обновляет label
    button = ttk.Button(root, text="Сменить обои", command=lambda: mytools.on_button_click(label))
    button.pack(pady=10)

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


    # Кнопка для выбора файлов
    def choose_files():
        files = filedialog.askopenfilenames(title="Выберите файлы")
        if files:
            label.config(text=f"Выбрано файлов: {len(files)}")

    file_button = ttk.Button(root, text="Выбрать файлы", command=choose_files)
    file_button.pack(pady=10)



    root.mainloop()

if __name__ == "__main__":
    main()
import ctypes

def minimize_all_windows():
    # Отправляем команду "Свернуть все"
    ctypes.windll.user32.keybd_event(0x5B, 0, 0, 0)  # Win
    ctypes.windll.user32.keybd_event(0x44, 0, 0, 0)  # D
    ctypes.windll.user32.keybd_event(0x44, 0, 2, 0)  # Release D
    ctypes.windll.user32.keybd_event(0x5B, 0, 2, 0)  # Release Win

minimize_all_windows()
import threading
import time
import ctypes
from pynput import keyboard
import tkinter as tk
from tkinter import ttk


class KnightOnlineMacro:
    def __init__(self, root):
        self.root = root
        self.keyboard_controller = keyboard.Controller()
        self.attack_thread = threading.Thread(target=self.attack, daemon=True)
        self.minor_thread = threading.Thread(target=self.minor, daemon=True)
        self.listener_keyboard = keyboard.Listener(on_press=self.on_press, on_release=self.on_release)
        self.listener_keyboard.start()

        # GUI Components
        self.canvas = tk.Canvas(self.root, width=100, height=100)
        self.circle = self.canvas.create_oval(20, 20, 80, 80, fill='red')  # Başlangıçta kırmızı
        self.canvas.pack()

        self.always_on_top_var = tk.BooleanVar()
        self.always_on_top_check = ttk.Checkbutton(self.root, text="Always on top", variable=self.always_on_top_var,
                                                   command=self.update_always_on_top)
        self.always_on_top_check.pack()

        # Caps Lock durumunu sürekli kontrol et
        self.update_circle_color()

    def attack(self):
        while self.caps_lock_state() != 0:
            skill_keys = ['1', '2', '3', '4', '5', '6', '7']
            for key in skill_keys:
                if not self.caps_lock_state() != 0:
                    break
                self.keyboard_controller.press(key)
                time.sleep(0.01)
                self.keyboard_controller.release(key)
                time.sleep(0.01)
                for _ in range(2):
                    if not self.caps_lock_state() != 0:
                        break
                    self.keyboard_controller.press('r')
                    time.sleep(0.01)
                    self.keyboard_controller.release('r')
                time.sleep(0.01)
                self.keyboard_controller.press(key)
                time.sleep(0.01)
                self.keyboard_controller.release(key)
                time.sleep(0.01)
                self.keyboard_controller.press('r')
                time.sleep(0.01)
                self.keyboard_controller.release('r')
            time.sleep(0.1)
            if not self.caps_lock_state() != 0:
                break

    def minor(self):
        while self.caps_lock_state() != 0:
            for minor_key in ['8', '9', '0', '9']:
                self.keyboard_controller.press(minor_key)
                time.sleep(0.01)
                self.keyboard_controller.release(minor_key)

            time.sleep(0.05)
            if not self.caps_lock_state() != 0:
                break

    def on_press(self, key):
        if key == keyboard.Key.caps_lock:
            if not self.attack_thread.is_alive():
                self.attack_thread = threading.Thread(target=self.attack, daemon=True)
                self.attack_thread.start()
            if not self.minor_thread.is_alive():
                self.minor_thread = threading.Thread(target=self.minor, daemon=True)
                self.minor_thread.start()

    def on_release(self, key):
        pass

    def update_circle_color(self):
        if self.caps_lock_state() != 0:
            self.canvas.itemconfig(self.circle, fill='green')
        else:
            self.canvas.itemconfig(self.circle, fill='red')
        self.root.after(100, self.update_circle_color)

    def update_always_on_top(self):
        if self.always_on_top_var.get():
            self.root.attributes('-topmost', 1)
        else:
            self.root.attributes('-topmost', 0)

    def caps_lock_state(self):
        hllDll = ctypes.WinDLL("User32.dll")
        VK_CAPITAL = 0x14
        return hllDll.GetKeyState(VK_CAPITAL)


if __name__ == "__main__":
    root = tk.Tk()
    root.title("Knight Online Macro GUI")
    root.geometry("200x150")  # Pencere boyutunu ayarla
    app = KnightOnlineMacro(root)
    root.mainloop()

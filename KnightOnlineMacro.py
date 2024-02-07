import ctypes
import threading
import time
import tkinter as tk
from tkinter import ttk
from pynput import keyboard

import pyautogui
import time
import threading
import ctypes
from PIL import Image
import pyautogui as py

class KnightOnlineMacro:
    def __init__(self, root):
        self.root = root
        self.character_class = tk.StringVar()
        self.character_class.set("Asas")  # Varsayılan olarak Asas seçili
        self.pot_thread = threading.Thread(target=self.hp_mp_bas, daemon=True)
        self.attack_thread = threading.Thread(target=self.attack, daemon=True)
        self.minor_thread = threading.Thread(target=self.minor, daemon=True)
        self.keyboard_controller = keyboard.Controller()
        self.listener_keyboard = keyboard.Listener(on_press=self.on_press)
        self.listener_keyboard.start()

        # GUI Components
        self.setup_gui()

        # Thread Initialization
        self.thread = None

    hpx = 167
    hpy = 46
    mpx = 92
    mpy = 60

    def hp_mp_bas(self):
        while self.caps_lock_state() != 0:
            time.sleep(3)
            canr, cang, canb, = py.pixel(self.hpx, self.hpy)
            manar, manag, manab = py.pixel(self.mpx, self.mpy)

            if canr < 10:
                self.keyboard_controller.press('7')
                time.sleep(0.03)
                self.keyboard_controller.release('7')
            if manab < 10:
                self.keyboard_controller.press('8')
                time.sleep(0.03)
                self.keyboard_controller.release('8')

    def setup_gui(self):
        self.canvas = tk.Canvas(self.root, width=100, height=100)
        self.circle = self.canvas.create_oval(20, 20, 80, 80, fill='red')  # Başlangıçta kırmızı
        self.canvas.pack()

        self.always_on_top_var = tk.BooleanVar()
        self.always_on_top_check = ttk.Checkbutton(self.root, text="Always on top", variable=self.always_on_top_var,
                                                   command=self.update_always_on_top)
        self.always_on_top_check.pack()

        # Character Class Radio Buttons
        classes_frame = tk.Frame(self.root)
        classes_frame.pack()
        ttk.Radiobutton(classes_frame, text="Asas", variable=self.character_class, value="Asas").pack(side=tk.LEFT)
        ttk.Radiobutton(classes_frame, text="BP/Warrior", variable=self.character_class, value="BP/Warrior").pack(
            side=tk.LEFT)
        ttk.Radiobutton(classes_frame, text="Okçu", variable=self.character_class, value="Okçu").pack(side=tk.LEFT)

        self.update_circle_color()

    def attack(self):
        while self.caps_lock_state() != 0:
            if self.character_class.get() == "Asas":
                self.asas_attack()
            elif self.character_class.get() == "BP/Warrior":
                self.melee_attack()
            elif self.character_class.get() == "Okçu":
                self.archer_attack()
            time.sleep(0.1)

    def asas_attack(self):
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
            if self.character_class.get() == "Asas":
                if not self.minor_thread.is_alive():
                    self.minor_thread = threading.Thread(target=self.minor, daemon=True)
                    self.minor_thread.start()
            else:
                self.pot_thread = threading.Thread(target=self.hp_mp_bas(), daemon=True)
                self.pot_thread.start()
            if not self.attack_thread.is_alive():
                self.attack_thread = threading.Thread(target=self.attack, daemon=True)
                self.attack_thread.start()

    def melee_attack(self):
        while self.caps_lock_state() != 0:
            for minor_key in ['2', '2', 'r', 'r']:
                self.keyboard_controller.press(minor_key)
                time.sleep(0.01)
                self.keyboard_controller.release(minor_key)

            time.sleep(0.05)
            if not self.caps_lock_state() != 0:
                break

    def archer_attack(self):
        while self.caps_lock_state() != 0:
            for minor_key in ['2', 'w', '3', 'w']:
                self.keyboard_controller.press(minor_key)
                time.sleep(0.05)
                self.keyboard_controller.release(minor_key)
                if minor_key == "w":
                    time.sleep(0.1)
                else:
                    time.sleep(0.4)
            if not self.caps_lock_state() != 0:
                break

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

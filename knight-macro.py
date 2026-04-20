"""Knight Online için yardımcı uygulama."""
import ctypes
import threading
import time
import tkinter as tk
from tkinter import messagebox, ttk

from pynput import keyboard
import pyautogui as py


class KnightOnlineMacro:
    """Knight Online Macro uygulaması."""

    def __init__(self, root):
        self.root = root
        self.root.title("Knight Online Macro GUI")
        self.root.geometry("430x480")

        self.keyboard_controller = keyboard.Controller()
        self.listener_keyboard = keyboard.Listener(on_press=self.on_press)
        self.listener_keyboard.start()

        # Çalışma durumları
        self.running = threading.Event()
        self.stop_event = threading.Event()

        # Thread referansları
        self.attack_thread = None
        self.pot_thread = None
        self.minor_thread = None

        # Seçimler
        self.character_class = tk.StringVar(value="Asas")
        self.always_on_top_var = tk.BooleanVar(value=True)

        # HP/MP piksel ve tuş ayarları
        self.hp_x = tk.IntVar(value=167)
        self.hp_y = tk.IntVar(value=46)
        self.mp_x = tk.IntVar(value=92)
        self.mp_y = tk.IntVar(value=60)
        self.hp_key = tk.StringVar(value="7")
        self.mp_key = tk.StringVar(value="8")

        self.setup_gui()
        self.update_always_on_top()
        self.update_circle_color()
        self.sync_from_caps_lock()

        self.root.protocol("WM_DELETE_WINDOW", self.on_close)

    @staticmethod
    def caps_lock_state():
        """Caps Lock durumunu döndürür."""
        hll_dll = ctypes.WinDLL("User32.dll")
        return hll_dll.GetKeyState(0x14)

    def setup_gui(self):
        """Arayüzü oluşturur."""
        style = ttk.Style()
        style.configure("Card.TLabelframe", padding=8)

        main = ttk.Frame(self.root, padding=12)
        main.pack(fill="both", expand=True)

        status_frame = ttk.LabelFrame(main, text="Durum", style="Card.TLabelframe")
        status_frame.pack(fill="x", pady=(0, 8))

        self.canvas = tk.Canvas(status_frame, width=42, height=42, highlightthickness=0)
        self.circle = self.canvas.create_oval(4, 4, 38, 38, fill="red")
        self.canvas.pack(side="left", padx=(0, 8))

        self.status_label = ttk.Label(status_frame, text="Macro Pasif (Caps Lock: OFF)")
        self.status_label.pack(side="left", anchor="w")

        options_frame = ttk.LabelFrame(main, text="Genel", style="Card.TLabelframe")
        options_frame.pack(fill="x", pady=8)

        ttk.Checkbutton(
            options_frame,
            text="Her zaman üstte",
            variable=self.always_on_top_var,
            command=self.update_always_on_top,
        ).pack(anchor="w")

        ttk.Label(options_frame, text="Job Seçimi:").pack(anchor="w", pady=(8, 0))
        class_row = ttk.Frame(options_frame)
        class_row.pack(fill="x", pady=(4, 0))
        ttk.Radiobutton(class_row, text="Asas", variable=self.character_class, value="Asas").pack(side="left")
        ttk.Radiobutton(class_row, text="BP/Warrior", variable=self.character_class, value="BP/Warrior").pack(side="left", padx=8)
        ttk.Radiobutton(class_row, text="Okçu", variable=self.character_class, value="Okçu").pack(side="left")

        pot_frame = ttk.LabelFrame(main, text="HP / MP Ayarları", style="Card.TLabelframe")
        pot_frame.pack(fill="x", pady=8)

        grid = ttk.Frame(pot_frame)
        grid.pack(fill="x")

        ttk.Label(grid, text="HP X").grid(row=0, column=0, sticky="w")
        ttk.Entry(grid, textvariable=self.hp_x, width=7).grid(row=0, column=1, padx=4)
        ttk.Label(grid, text="HP Y").grid(row=0, column=2, sticky="w")
        ttk.Entry(grid, textvariable=self.hp_y, width=7).grid(row=0, column=3, padx=4)
        ttk.Label(grid, text="HP Tuş").grid(row=0, column=4, sticky="w")
        ttk.Entry(grid, textvariable=self.hp_key, width=7).grid(row=0, column=5, padx=4)

        ttk.Label(grid, text="MP X").grid(row=1, column=0, sticky="w", pady=(6, 0))
        ttk.Entry(grid, textvariable=self.mp_x, width=7).grid(row=1, column=1, padx=4, pady=(6, 0))
        ttk.Label(grid, text="MP Y").grid(row=1, column=2, sticky="w", pady=(6, 0))
        ttk.Entry(grid, textvariable=self.mp_y, width=7).grid(row=1, column=3, padx=4, pady=(6, 0))
        ttk.Label(grid, text="MP Tuş").grid(row=1, column=4, sticky="w", pady=(6, 0))
        ttk.Entry(grid, textvariable=self.mp_key, width=7).grid(row=1, column=5, padx=4, pady=(6, 0))

        capture_row = ttk.Frame(pot_frame)
        capture_row.pack(fill="x", pady=(8, 0))

        ttk.Button(capture_row, text="HP Pikseli Mouse'dan Al", command=self.capture_hp_pixel).pack(side="left")
        ttk.Button(capture_row, text="MP Pikseli Mouse'dan Al", command=self.capture_mp_pixel).pack(side="left", padx=8)

        ttk.Label(
            main,
            text="Caps Lock ON => Macro başlar | Caps Lock OFF => Macro durur",
            foreground="#666",
        ).pack(anchor="w", pady=(10, 0))

    def update_always_on_top(self):
        self.root.attributes("-topmost", 1 if self.always_on_top_var.get() else 0)

    def update_circle_color(self):
        running = self.running.is_set()
        self.canvas.itemconfig(self.circle, fill="green" if running else "red")
        self.status_label.config(
            text=f"Macro {'Aktif' if running else 'Pasif'} (Caps Lock: {'ON' if self.caps_lock_state() else 'OFF'})"
        )
        self.root.after(100, self.update_circle_color)

    def sync_from_caps_lock(self):
        """Caps Lock durumuna göre threadleri başlatır/durdurur."""
        if self.caps_lock_state() != 0:
            self.start_macro()
        else:
            self.stop_macro()
        self.root.after(250, self.sync_from_caps_lock)

    def on_press(self, key):
        if key == keyboard.Key.caps_lock:
            # Donanım tuşu ile manuel toggle sonrası hızlı senkron
            self.root.after(50, self.sync_from_caps_lock)

    def start_macro(self):
        if self.running.is_set():
            return
        self.running.set()
        self.stop_event.clear()

        self.attack_thread = threading.Thread(target=self.attack_loop, daemon=True)
        self.attack_thread.start()

        self.pot_thread = threading.Thread(target=self.hp_mp_bas, daemon=True)
        self.pot_thread.start()

        if self.character_class.get() == "Asas":
            self.minor_thread = threading.Thread(target=self.minor, daemon=True)
            self.minor_thread.start()

    def stop_macro(self):
        if not self.running.is_set():
            return
        self.running.clear()
        self.stop_event.set()

    def on_close(self):
        self.stop_macro()
        self.listener_keyboard.stop()
        self.root.destroy()

    def read_pixel_intensity(self, x, y):
        pixel = py.pixel(x, y)
        return pixel[0] if isinstance(pixel, tuple) else pixel

    def hp_mp_bas(self):
        while self.running.is_set() and not self.stop_event.is_set():
            time.sleep(0.2)
            try:
                can_r = self.read_pixel_intensity(self.hp_x.get(), self.hp_y.get())
                mana_b = self.read_pixel_intensity(self.mp_x.get(), self.mp_y.get())
            except Exception:
                continue

            hp_key = self.hp_key.get().strip()[:1]
            mp_key = self.mp_key.get().strip()[:1]

            if hp_key and can_r < 10:
                self.press_key(hp_key)
            if mp_key and mana_b < 10:
                self.press_key(mp_key)

    def attack_loop(self):
        while self.running.is_set() and not self.stop_event.is_set():
            character = self.character_class.get()
            if character == "Asas":
                self.asas_attack_cycle()
            elif character == "BP/Warrior":
                self.melee_attack_cycle()
            elif character == "Okçu":
                self.archer_attack_cycle()
            time.sleep(0.05)

    def press_key(self, key_value, hold=0.01):
        if not self.running.is_set() or self.stop_event.is_set():
            return
        self.keyboard_controller.press(key_value)
        time.sleep(hold)
        self.keyboard_controller.release(key_value)

    # Aşağıdaki saldırı sıraları mevcut davranış bozulmasın diye korunmuştur.
    def asas_attack_cycle(self):
        skill_keys = ["1", "2", "3", "4", "5", "6", "7"]
        for key in skill_keys:
            if not self.running.is_set() or self.stop_event.is_set() or self.character_class.get() != "Asas":
                return
            self.press_key(key)
            time.sleep(0.01)
            for _ in range(2):
                if not self.running.is_set() or self.stop_event.is_set() or self.character_class.get() != "Asas":
                    return
                self.press_key("r")
            time.sleep(0.01)
            self.press_key(key)
            time.sleep(0.01)
            self.press_key("r")
        time.sleep(0.1)

    def melee_attack_cycle(self):
        for key in ["2", "2", "r", "r"]:
            if not self.running.is_set() or self.stop_event.is_set() or self.character_class.get() != "BP/Warrior":
                return
            self.press_key(key)
        time.sleep(0.05)

    def archer_attack_cycle(self):
        for key in ["2", "w", "3", "w"]:
            if not self.running.is_set() or self.stop_event.is_set() or self.character_class.get() != "Okçu":
                return
            self.press_key(key, hold=0.05)
            time.sleep(0.1 if key == "w" else 0.4)

    def minor(self):
        while self.running.is_set() and not self.stop_event.is_set() and self.character_class.get() == "Asas":
            for minor_key in ["8", "9", "0", "9"]:
                if not self.running.is_set() or self.stop_event.is_set() or self.character_class.get() != "Asas":
                    return
                self.press_key(minor_key)
            time.sleep(0.05)

    def capture_hp_pixel(self):
        self.capture_pixel(self.hp_x, self.hp_y, "HP")

    def capture_mp_pixel(self):
        self.capture_pixel(self.mp_x, self.mp_y, "MP")

    def capture_pixel(self, x_var, y_var, name):
        self.root.iconify()
        messagebox.showinfo(
            "Piksel Seçimi",
            f"{name} için mouse imlecini hedef bara getir. 2 saniye sonra konum alınacak.",
        )
        time.sleep(2)
        x, y = py.position()
        x_var.set(int(x))
        y_var.set(int(y))
        self.root.deiconify()
        self.root.lift()


if __name__ == "__main__":
    root = tk.Tk()
    KnightOnlineMacro(root)
    root.mainloop()

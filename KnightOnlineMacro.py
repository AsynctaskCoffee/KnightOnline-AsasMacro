import threading
import time
import ctypes
from pynput import keyboard


class KnightOnlineMacro:
    def __init__(self):
        self.keyboard_controller = keyboard.Controller()
        self.attack_thread = threading.Thread(target=self.attack, daemon=True)
        self.minor_thread = threading.Thread(target=self.minor, daemon=True)
        self.listener_keyboard = keyboard.Listener(on_press=self.on_press, on_release=self.on_release)
        self.listener_keyboard.start()
        print("Program başlatıldı. Caps Lock açıkken otomatik saldırı ve minor aktif, kapalıyken pasif.")

    def attack(self):
        while caps_lock_state() != 0:
            skill_keys = ['1', '2', '3', '4', '5', '6', '7']
            for key in skill_keys:
                if not caps_lock_state() != 0:
                    break
                self.keyboard_controller.press(key)
                time.sleep(0.01)
                self.keyboard_controller.release(key)
                time.sleep(0.01)
                for _ in range(2):
                    if not caps_lock_state() != 0:
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
            if not caps_lock_state() != 0:
                break

    def minor(self):
        while caps_lock_state() != 0:
            for minor_key in ['8', '9', '0', '9']:
                self.keyboard_controller.press(minor_key)
                time.sleep(0.01)
                self.keyboard_controller.release(minor_key)

            time.sleep(0.05)

            if not caps_lock_state() != 0:
                break

    def on_press(self, key):
        if key == keyboard.Key.caps_lock:  # Assuming you want to start the threads with caps lock
            if not self.attack_thread.is_alive():
                self.attack_thread = threading.Thread(target=self.attack, daemon=True)  # Create a new thread
                self.attack_thread.start()
            if not self.minor_thread.is_alive():
                self.minor_thread = threading.Thread(target=self.minor, daemon=True)  # Create a new thread
                self.minor_thread.start()

    def on_release(self, key):
        return


def caps_lock_state():
    hllDll = ctypes.WinDLL("User32.dll")
    VK_CAPITAL = 0x14
    return hllDll.GetKeyState(VK_CAPITAL)


if __name__ == "__main__":
    macro = KnightOnlineMacro()
    macro.listener_keyboard.join()

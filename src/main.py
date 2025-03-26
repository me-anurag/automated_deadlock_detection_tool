# src/main.py
import tkinter as tk
import os
from gui import DeadlockDetectionGUI
from sound_manager import SoundManager

if __name__ == "__main__":
    base_dir = os.path.dirname(os.path.abspath(__file__))
    allocate_sound_path = os.path.join(base_dir, "..", "assets", "allocate_sound.wav")  # Updated path
    request_sound_path = os.path.join(base_dir, "..", "assets", "request_sound.wav")   # Updated path

    sound_manager = SoundManager(allocate_sound_path, request_sound_path)

    main_window = tk.Tk()
    app = DeadlockDetectionGUI(main_window, sound_manager)
    main_window.mainloop()
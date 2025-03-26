# src/main.py
import tkinter as tk
import os
from gui import DeadlockDetectionGUI  # Remove "src." since we're in the src/ directory
from sound_manager import SoundManager  # Remove "src." since we're in the src/ directory

if __name__ == "__main__":
    base_dir = os.path.dirname(os.path.abspath(__file__))
    allocate_sound_path = os.path.join(base_dir, "..", "allocate_sound.wav")
    request_sound_path = os.path.join(base_dir, "..", "request_sound.wav")

    sound_manager = SoundManager(allocate_sound_path, request_sound_path)

    main_window = tk.Tk()
    app = DeadlockDetectionGUI(main_window, sound_manager)
    main_window.mainloop()
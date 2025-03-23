import tkinter as tk
from tkinter import ttk

class DeadlockDetectionGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Automated Deadlock Detection Tool")
        self.root.geometry("500x300")

        # Background Mode
        self.is_dark_mode = False
        self.root.configure(bg="white")

        # Title Label
        self.title_label = tk.Label(root, text="Automated Deadlock Detection Tool", font=("Arial", 16, "bold"), bg="white")
        self.title_label.pack(pady=20)

        # Buttons for Detection Modes
        self.single_instance_button = tk.Button(root, text="Single-Instance Detection", font=("Arial", 12), 
                                                command=self.open_single_instance)
        self.single_instance_button.pack(pady=10)

        self.multi_instance_button = tk.Button(root, text="Multi-Instance Detection", font=("Arial", 12), 
                                               command=self.open_multi_instance)
        self.multi_instance_button.pack(pady=10)

        # Background Mode Toggle
        self.mode_switch = ttk.Checkbutton(root, text="Dark Mode", command=self.toggle_mode)
        self.mode_switch.pack(pady=20)

    def toggle_mode(self):
        if self.is_dark_mode:
            self.root.configure(bg="white")
            self.title_label.config(bg="white", fg="black")
            self.is_dark_mode = False
        else:
            self.root.configure(bg="black")
            self.title_label.config(bg="black", fg="white")
            self.is_dark_mode = True

    def open_single_instance(self):
        # Open a new window for Single-Instance Detection
        single_window = tk.Toplevel(self.root)
        single_window.title("Single-Instance Deadlock Detection")
        single_window.geometry("400x300")

        label = tk.Label(single_window, text="Single-Instance Detection Page", font=("Arial", 14, "bold"))
        label.pack(pady=20)

        close_button = tk.Button(single_window, text="Close", command=single_window.destroy)
        close_button.pack(pady=10)

    def open_multi_instance(self):
        # Open a new window for Multi-Instance Detection
        multi_window = tk.Toplevel(self.root)
        multi_window.title("Multi-Instance Deadlock Detection")
        multi_window.geometry("400x300")

        label = tk.Label(multi_window, text="Multi-Instance Detection Page", font=("Arial", 14, "bold"))
        label.pack(pady=20)

        close_button = tk.Button(multi_window, text="Close", command=multi_window.destroy)
        close_button.pack(pady=10)

# Run the GUI
if __name__ == "__main__":
    root = tk.Tk()
    app = DeadlockDetectionGUI(root)
    root.mainloop()

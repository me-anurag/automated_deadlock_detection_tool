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
        """Toggle between dark and light mode."""
        if self.is_dark_mode:
            self.root.configure(bg="white")
            self.title_label.config(bg="white", fg="black")
            self.is_dark_mode = False
        else:
            self.root.configure(bg="black")
            self.title_label.config(bg="black", fg="white")
            self.is_dark_mode = True

    def open_single_instance(self):
        """Open a new window for Single-Instance Detection."""
        single_window = tk.Toplevel(self.root)
        single_window.title("Single-Instance Resource Detection")
        single_window.geometry("500x400")

        # Input Fields
        tk.Label(single_window, text="Enter number of processes:", font=("Arial", 12)).pack(pady=5)
        process_entry = tk.Entry(single_window)
        process_entry.pack(pady=5)

        tk.Label(single_window, text="Enter number of resources:", font=("Arial", 12)).pack(pady=5)
        resource_entry = tk.Entry(single_window)
        resource_entry.pack(pady=5)

        # Submit Button
        submit_button = tk.Button(single_window, text="Generate Canvas", font=("Arial", 12),
                                  command=lambda: self.generate_canvas(single_window, process_entry, resource_entry))
        submit_button.pack(pady=10)

    def generate_canvas(self, window, process_entry, resource_entry):
        """Generate a canvas with emojis representing processes and resources."""
        try:
            num_processes = int(process_entry.get())
            num_resources = int(resource_entry.get())
        except ValueError:
            return  # Ignore invalid inputs

        # Create Canvas
        canvas = tk.Canvas(window, width=400, height=250, bg="lightgray")
        canvas.pack(pady=10)

        # Display Processes as Emojis
        process_emoji = "🤖"
        resource_emoji = "🖥️"
        
        for i in range(num_processes):
            canvas.create_text(50 + i * 80, 50, text=f"P{i+1} {process_emoji}", font=("Arial", 14))

        for i in range(num_resources):
            canvas.create_text(50 + i * 80, 150, text=f"R{i+1} {resource_emoji}", font=("Arial", 14))

    def open_multi_instance(self):
        print("Opening Multi-Instance Resource Detection...")
        # TODO: Implement navigation to Multi-Instance Detection Page

# Run the GUI
if __name__ == "__main__":
    root = tk.Tk()
    app = DeadlockDetectionGUI(root)
    root.mainloop()



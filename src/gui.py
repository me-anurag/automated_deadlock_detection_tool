# src/gui.py
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import tkinter.font as tkfont
from deadlock_algo import DeadlockDetector
from visualization import GraphVisualizer  # Import the new visualization module

class DeadlockDetectionGUI:
    def __init__(self, window, sound_manager):
        self.window = window
        self.sound_manager = sound_manager
        self.window.title("Deadlock Detection Tool")
        self.window.geometry("500x400")
        self.window.minsize(400, 300)

        self.dark_mode_on = False
        self.detect_button_animated = False
        self.message_shown_in_detection = False
        self.status_after_id = None

        # Main window background
        self.background_canvas = tk.Canvas(self.window, highlightthickness=0)
        self.background_canvas.pack(fill="both", expand=True)
        self.add_gradient(self.background_canvas, "#A3BFFA", "#F3F4F6", 500, 400)

        # Title and subtitle
        self.title_text = tk.Label(self.background_canvas, text="Deadlock Detection Tool", 
                                   font=("Helvetica", 20, "bold"), bg="#A3BFFA", fg="#2E3A59")
        self.title_text.place(relx=0.5, rely=0.15, anchor="center")
        self.title_text.configure(fg="#A3BFFA")
        self.fade_in_title(0)

        self.subtitle_text = tk.Label(self.background_canvas, text="Choose a detection mode to begin!", 
                                      font=("Helvetica", 12), bg="#A3BFFA", fg="#2E3A59")
        self.subtitle_text.place(relx=0.5, rely=0.25, anchor="center")

        # Gear animation
        self.gear_label = tk.Label(self.background_canvas, text="⚙️", font=("Helvetica", 24), 
                                   bg="#A3BFFA", fg="#2E3A59")
        self.gear_label.place(relx=0.5, rely=0.35, anchor="center")
        self.rotate_gear(0)

        # Buttons for single and multi-instance detection
        self.button_font = tkfont.Font(family="Helvetica", size=14)

        self.button_single_frame = tk.Frame(self.background_canvas, bg="#4CAF50", bd=2, relief="raised")
        self.button_single_frame.place(relx=0.5, rely=0.5, anchor="center")
        self.button_single_label = tk.Label(self.button_single_frame, text="Single-Instance Detection", 
                                            font=self.button_font, bg="#4CAF50", fg="white", padx=10, pady=5)
        self.button_single_label.pack()
        self.button_single_frame.bind("<Button-1>", lambda e: self.open_single_window())
        self.button_single_label.bind("<Button-1>", lambda e: self.open_single_window())
        self.button_single_frame.bind("<Enter>", lambda e: self.button_single_frame.config(bg="#45A049"))
        self.button_single_frame.bind("<Leave>", lambda e: self.button_single_frame.config(bg="#4CAF50"))
        self.button_single_label.bind("<Enter>", lambda e: self.button_single_frame.config(bg="#45A049"))
        self.button_single_label.bind("<Leave>", lambda e: self.button_single_frame.config(bg="#4CAF50"))

        self.button_multi_frame = tk.Frame(self.background_canvas, bg="#2196F3", bd=2, relief="raised")
        self.button_multi_frame.place(relx=0.5, rely=0.6, anchor="center")
        self.button_multi_label = tk.Label(self.button_multi_frame, text="Multi-Instance Detection", 
                                           font=self.button_font, bg="#2196F3", fg="white", padx=10, pady=5)
        self.button_multi_label.pack()
        self.button_multi_frame.bind("<Button-1>", lambda e: self.open_multi_window())
        self.button_multi_label.bind("<Button-1>", lambda e: self.open_multi_window())
        self.button_multi_frame.bind("<Enter>", lambda e: self.button_multi_frame.config(bg="#1E88E5"))
        self.button_multi_frame.bind("<Leave>", lambda e: self.button_multi_frame.config(bg="#2196F3"))
        self.button_multi_label.bind("<Enter>", lambda e: self.button_multi_frame.config(bg="#1E88E5"))
        self.button_multi_label.bind("<Leave>", lambda e: self.button_multi_frame.config(bg="#2196F3"))

        # Mode selection (dark mode, sound)
        self.mode_frame = tk.Frame(self.background_canvas, bg="#A3BFFA")
        self.mode_frame.place(relx=0.5, rely=0.75, anchor="center")

        self.dark_mode_checkbox = ttk.Checkbutton(self.mode_frame, text="Dark Mode", command=self.switch_mode)
        self.dark_mode_checkbox.pack(side=tk.LEFT, padx=10)
        self.dark_mode_checkbox.bind("<Enter>", lambda e: self.dark_mode_checkbox.config(text="Dark Mode 🌙"))
        self.dark_mode_checkbox.bind("<Leave>", lambda e: self.dark_mode_checkbox.config(text="Dark Mode"))

        self.sound_checkbox = ttk.Checkbutton(self.mode_frame, text="Sound On" if self.sound_manager.sounds_loaded else "Sound Off", 
                                             command=self.toggle_sound)
        self.sound_checkbox.pack(side=tk.LEFT, padx=10)

        self.resources_held = {}
        self.resources_wanted = {}

        self.window.bind("<Configure>", self.on_window_resize)
        self.on_window_resize(None)

    def toggle_sound(self):
        sound_on = self.sound_manager.toggle_sound()
        self.sound_checkbox.config(text="Sound On" if sound_on else "Sound Off")

    def on_window_resize(self, event):
        new_width = self.window.winfo_width()
        new_height = self.window.winfo_height()

        self.background_canvas.config(width=new_width, height=new_height)
        self.background_canvas.delete("all")
        if self.dark_mode_on:
            self.add_gradient(self.background_canvas, "#2E3A59", "#121212", new_width, new_height)
        else:
            self.add_gradient(self.background_canvas, "#A3BFFA", "#F3F4F6", new_width, new_height)

        title_font_size = max(16, min(30, int(new_width / 25)))
        subtitle_font_size = max(10, min(18, int(new_width / 40)))
        button_font_size = max(12, min(20, int(new_width / 35)))
        gear_font_size = max(20, min(40, int(new_width / 20)))

        self.title_text.config(font=("Helvetica", title_font_size, "bold"))
        self.subtitle_text.config(font=("Helvetica", subtitle_font_size))
        self.button_font.configure(size=button_font_size)

        if hasattr(self, "gear_label") and self.gear_label.winfo_exists():
            self.gear_label.config(font=("Helvetica", gear_font_size))

    def add_gradient(self, canvas, color_start, color_end, width, height):
        steps = 20
        for i in range(steps):
            r1 = int(color_start[1:3], 16)
            g1 = int(color_start[3:5], 16)
            b1 = int(color_start[5:7], 16)
            r2 = int(color_end[1:3], 16)
            g2 = int(color_end[3:5], 16)
            b2 = int(color_end[5:7], 16)
            r = int(r1 + (r2 - r1) * i / steps)
            g = int(g1 + (g2 - g1) * i / steps)
            b = int(b1 + (b2 - b1) * i / steps)
            color = f"#{r:02x}{g:02x}{b:02x}"
            y_start = i * (height / steps)
            y_end = (i + 1) * (height / steps)
            canvas.create_rectangle(0, y_start, width, y_end, fill=color, outline="")

    def fade_in_title(self, step):
        if step <= 20:
            r1, g1, b1 = 163, 191, 250
            r2, g2, b2 = 46, 58, 89
            r = int(r1 + (r2 - r1) * step / 20)
            g = int(g1 + (g2 - g1) * step / 20)
            b = int(b1 + (b2 - b1) * step / 20)
            color = f"#{r:02x}{g:02x}{b:02x}"
            self.title_text.configure(fg=color)
            self.window.after(50, self.fade_in_title, step + 1)
        else:
            self.title_text.configure(fg="#2E3A59")

    def rotate_gear(self, step):
        if step < 8:
            gear_positions = ["⚙️", "⚙️", "⚙️", "⚙️", "⚙️", "⚙️", "⚙️", "⚙️"]
            self.gear_label.configure(text=gear_positions[step % 8])
            self.window.after(100, self.rotate_gear, step + 1)
        else:
            self.gear_label.destroy()
            delattr(self, "gear_label")

    def switch_mode(self):
        if self.dark_mode_on:
            self.background_canvas.delete("all")
            new_width = self.window.winfo_width()
            new_height = self.window.winfo_height()
            self.add_gradient(self.background_canvas, "#A3BFFA", "#F3F4F6", new_width, new_height)
            self.title_text.config(bg="#A3BFFA", fg="#2E3A59")
            self.subtitle_text.config(bg="#A3BFFA", fg="#2E3A59")
            self.button_single_frame.config(bg="#4CAF50")
            self.button_single_label.config(bg="#4CAF50")
            self.button_multi_frame.config(bg="#2196F3")
            self.button_multi_label.config(bg="#2196F3")
            self.mode_frame.config(bg="#A3BFFA")
            self.dark_mode_on = False
        else:
            self.background_canvas.delete("all")
            new_width = self.window.winfo_width()
            new_height = self.window.winfo_height()
            self.add_gradient(self.background_canvas, "#2E3A59", "#121212", new_width, new_height)
            self.title_text.config(bg="#2E3A59", fg="#A3BFFA")
            self.subtitle_text.config(bg="#2E3A59", fg="#A3BFFA")
            self.button_single_frame.config(bg="#66BB6A")
            self.button_single_label.config(bg="#66BB6A")
            self.button_multi_frame.config(bg="#42A5F5")
            self.button_multi_label.config(bg="#42A5F5")
            self.mode_frame.config(bg="#2E3A59")
            self.dark_mode_on = True

        if hasattr(self, 'new_window') and self.new_window.winfo_exists():
            self.update_single_window_theme()

    def update_single_window_theme(self):
        if self.dark_mode_on:
            self.new_window.config(bg="#121212")
            self.input_area.config(bg="#2E3A59")
            for widget in self.input_area.winfo_children():
                if isinstance(widget, tk.Label):
                    widget.config(bg="#2E3A59", fg="#A3BFFA")
                elif isinstance(widget, tk.Button):
                    widget.config(bg="#42A5F5", fg="white")
            if hasattr(self, 'left_canvas'):
                self.left_canvas.config(bg="#2E3A59")
                self.left_inner_area.config(bg="#2E3A59")
                self.left_canvas.delete("all")
                self.left_canvas.create_text(100, 20, text="Allocations", font=("Arial", 12, "bold"), fill="#A3BFFA")
                self.show_allocations()
            if hasattr(self, 'right_canvas'):
                self.right_canvas.config(bg="#2E3A59")
                self.right_inner_area.config(bg="#2E3A59")
                self.right_canvas.delete("all")
                self.right_canvas.create_text(100, 20, text="Requests", font=("Arial", 12, "bold"), fill="#A3BFFA")
                self.show_requests()
            if hasattr(self, 'status_label'):
                self.status_label.config(bg="#121212", fg="#A3BFFA")
                self.status_frame.config(bg="#121212")
            if hasattr(self, 'finish_frame'):
                self.finish_frame.config(bg="#121212")
            if hasattr(self, 'button_finish'):
                self.button_finish.config(bg="#42A5F5", fg="white")
            if hasattr(self, 'detect_frame'):
                self.detect_frame.config(bg="#121212")
            if hasattr(self, 'button_detect_deadlock'):
                self.button_detect_deadlock.config(bg="#D32F2F", fg="white")
            if hasattr(self, 'restart_frame'):
                self.restart_frame.config(bg="#121212")
            if hasattr(self, 'button_restart'):
                self.button_restart.config(bg="#42A5F5", fg="white")
        else:
            self.new_window.config(bg="white")
            self.input_area.config(bg="white")
            for widget in self.input_area.winfo_children():
                if isinstance(widget, tk.Label):
                    widget.config(bg="white", fg="#2E3A59")
                elif isinstance(widget, tk.Button):
                    widget.config(bg="#D3D3D3", fg="black")
            if hasattr(self, 'left_canvas'):
                self.left_canvas.config(bg="#E6F0FA")
                self.left_inner_area.config(bg="#E6F0FA")
                self.left_canvas.delete("all")
                self.left_canvas.create_text(100, 20, text="Allocations", font=("Arial", 12, "bold"), fill="#2E3A59")
                self.show_allocations()
            if hasattr(self, 'right_canvas'):
                self.right_canvas.config(bg="#E6F0FA")
                self.right_inner_area.config(bg="#E6F0FA")
                self.right_canvas.delete("all")
                self.right_canvas.create_text(100, 20, text="Requests", font=("Arial", 12, "bold"), fill="#2E3A59")
                self.show_requests()
            if hasattr(self, 'status_label'):
                self.status_label.config(bg="white", fg="#2E3A59")
                self.status_frame.config(bg="white")
            if hasattr(self, 'finish_frame'):
                self.finish_frame.config(bg="white")
            if hasattr(self, 'detect_frame'):
                self.detect_frame.config(bg="white")
            if hasattr(self, 'button_detect_deadlock'):
                self.button_detect_deadlock.config(bg="red", fg="white")
            if hasattr(self, 'restart_frame'):
                self.restart_frame.config(bg="white")
            if hasattr(self, 'button_restart'):
                self.button_restart.config(bg="#D3D3D3", fg="black")

        if hasattr(self, 'center_canvas'):
            self.on_single_window_resize(None)

    def open_single_window(self):
        self.new_window = tk.Toplevel(self.window)
        self.new_window.title("Single-Instance Detection")
        self.new_window.geometry("1000x700")
        self.new_window.grab_set()

        if self.dark_mode_on:
            self.new_window.config(bg="#121212")
        else:
            self.new_window.config(bg="white")

        self.input_area = tk.Frame(self.new_window)
        self.input_area.pack(pady=10)
        if self.dark_mode_on:
            self.input_area.config(bg="#2E3A59")
        else:
            self.input_area.config(bg="white")

        label_processes = tk.Label(self.input_area, text="Processes:", font=("Arial", 12))
        label_processes.pack(side=tk.LEFT, padx=5)
        self.entry_processes = tk.Entry(self.input_area, width=5)
        self.entry_processes.pack(side=tk.LEFT, padx=5)

        label_resources = tk.Label(self.input_area, text="Resources:", font=("Arial", 12))
        label_resources.pack(side=tk.LEFT, padx=5)
        self.entry_resources = tk.Entry(self.input_area, width=5)
        self.entry_resources.pack(side=tk.LEFT, padx=5)

        button_create = tk.Button(self.input_area, text="Create Canvas", font=("Arial", 12),
                                  command=self.make_canvas)
        button_create.pack(side=tk.LEFT, padx=10)

        if self.dark_mode_on:
            label_processes.config(bg="#2E3A59", fg="#A3BFFA")
            label_resources.config(bg="#2E3A59", fg="#A3BFFA")
            button_create.config(bg="#42A5F5", fg="white")
        else:
            label_processes.config(bg="white", fg="#2E3A59")
            label_resources.config(bg="white", fg="#2E3A59")
            button_create.config(bg="#D3D3D3", fg="black")

    def open_multi_window(self):
        self.new_window = tk.Toplevel(self.window)
        self.new_window.title("Multi-Instance Detection")
        self.new_window.geometry("1000x700")
        self.new_window.grab_set()

        if self.dark_mode_on:
            self.new_window.config(bg="#121212")
        else:
            self.new_window.config(bg="white")

        self.input_area = tk.Frame(self.new_window)
        self.input_area.pack(pady=10)
        if self.dark_mode_on:
            self.input_area.config(bg="#2E3A59")
        else:
            self.input_area.config(bg="white")

        label_processes = tk.Label(self.input_area, text="Processes:", font=("Arial", 12))
        label_processes.pack(side=tk.LEFT, padx=5)
        self.entry_processes = tk.Entry(self.input_area, width=5)
        self.entry_processes.pack(side=tk.LEFT, padx=5)

        label_resources = tk.Label(self.input_area, text="Resources:", font=("Arial", 12))
        label_resources.pack(side=tk.LEFT, padx=5)
        self.entry_resources = tk.Entry(self.input_area, width=5)
        self.entry_resources.pack(side=tk.LEFT, padx=5)

        label_instances = tk.Label(self.input_area, text="Instances per Resource:", font=("Arial", 12))
        label_instances.pack(side=tk.LEFT, padx=5)
        self.entry_instances = tk.Entry(self.input_area, width=5)
        self.entry_instances.pack(side=tk.LEFT, padx=5)

        button_create = tk.Button(self.input_area, text="Create Canvas", font=("Arial", 12),
                                  command=self.make_multi_canvas)
        button_create.pack(side=tk.LEFT, padx=10)

        if self.dark_mode_on:
            label_processes.config(bg="#2E3A59", fg="#A3BFFA")
            label_resources.config(bg="#2E3A59", fg="#A3BFFA")
            label_instances.config(bg="#2E3A59", fg="#A3BFFA")
            button_create.config(bg="#42A5F5", fg="white")
        else:
            label_processes.config(bg="white", fg="#2E3A59")
            label_resources.config(bg="white", fg="#2E3A59")
            label_instances.config(bg="white", fg="#2E3A59")
            button_create.config(bg="#D3D3D3", fg="black")

    def make_canvas(self):
        print("make_canvas called")
        try:
            self.total_processes = int(self.entry_processes.get())
            self.total_resources = int(self.entry_resources.get())
            print(f"Processes: {self.total_processes}, Resources: {self.total_resources}")
            if self.total_processes <= 0 or self.total_resources <= 0:
                messagebox.showerror("Error", "Please enter positive numbers.", parent=self.new_window)
                return
            if self.total_processes > 10 or self.total_resources > 10:
                messagebox.showerror("Error", "Maximum 10 processes and resources allowed.", parent=self.new_window)
                return
        except ValueError:
            messagebox.showerror("Error", "Please enter valid numbers.", parent=self.new_window)
            return

        print("Validation passed, creating UI elements")
        try:
            self.entry_processes.config(state="disabled")
            self.entry_resources.config(state="disabled")

            self.button_undo = tk.Button(self.input_area, text="Undo", font=("Arial", 12),
                                         command=self.undo_last_action)
            self.button_undo.pack(side=tk.LEFT, padx=5)

            self.button_reset = tk.Button(self.input_area, text="Reset", font=("Arial", 12),
                                          command=self.reset_everything)
            self.button_reset.pack(side=tk.LEFT, padx=5)

            if self.dark_mode_on:
                self.button_undo.config(bg="#42A5F5", fg="white")
                self.button_reset.config(bg="#42A5F5", fg="white")
            else:
                self.button_undo.config(bg="#D3D3D3", fg="black")
                self.button_reset.config(bg="#D3D3D3", fg="black")

            self.main_area = tk.Frame(self.new_window)  # Store main_area as an instance variable
            self.main_area.pack(pady=10, fill=tk.BOTH, expand=True)

            self.left_area = tk.Frame(self.main_area, width=200)
            self.left_area.pack(side=tk.LEFT, fill=tk.Y)
            self.left_canvas = tk.Canvas(self.left_area, width=200)
            self.left_scroll = tk.Scrollbar(self.left_area, orient=tk.VERTICAL, command=self.left_canvas.yview)
            self.left_scroll.pack(side=tk.RIGHT, fill=tk.Y)
            self.left_canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
            self.left_canvas.configure(yscrollcommand=self.left_scroll.set)
            self.left_inner_area = tk.Frame(self.left_canvas)
            self.left_canvas.create_window((0, 0), window=self.left_inner_area, anchor="nw")
            self.left_inner_area.bind("<Configure>", lambda event: self.left_canvas.configure(scrollregion=self.left_canvas.bbox("all")))
            if self.dark_mode_on:
                self.left_canvas.config(bg="#2E3A59")
                self.left_inner_area.config(bg="#2E3A59")
                self.left_canvas.create_text(100, 20, text="Allocations", font=("Arial", 12, "bold"), fill="#A3BFFA")
            else:
                self.left_canvas.config(bg="#E6F0FA")
                self.left_inner_area.config(bg="#E6F0FA")
                self.left_canvas.create_text(100, 20, text="Allocations", font=("Arial", 12, "bold"), fill="#2E3A59")

            self.center_canvas = tk.Canvas(self.main_area)
            self.center_canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
            self.add_gradient(self.center_canvas, "#A3BFFA", "#F3F4F6", 500, 500)
            self.center_canvas.create_text(250, 20, text="Drag and Drop", font=("Arial", 12, "bold"), fill="#2E3A59")

            self.right_area = tk.Frame(self.main_area, width=200)
            self.right_area.pack(side=tk.LEFT, fill=tk.Y)
            self.right_canvas = tk.Canvas(self.right_area, width=200)
            self.right_scroll = tk.Scrollbar(self.right_area, orient=tk.VERTICAL, command=self.right_canvas.yview)
            self.right_scroll.pack(side=tk.RIGHT, fill=tk.Y)
            self.right_canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
            self.right_canvas.configure(yscrollcommand=self.right_scroll.set)
            self.right_inner_area = tk.Frame(self.right_canvas)
            self.right_canvas.create_window((0, 0), window=self.right_inner_area, anchor="nw")
            self.right_inner_area.bind("<Configure>", lambda event: self.right_canvas.configure(scrollregion=self.right_canvas.bbox("all")))
            if self.dark_mode_on:
                self.right_canvas.config(bg="#2E3A59")
                self.right_inner_area.config(bg="#2E3A59")
                self.right_canvas.create_text(100, 20, text="Requests", font=("Arial", 12, "bold"), fill="#A3BFFA")
            else:
                self.right_canvas.config(bg="#E6F0FA")
                self.right_inner_area.config(bg="#E6F0FA")
                self.right_canvas.create_text(100, 20, text="Requests", font=("Arial", 12, "bold"), fill="#2E3A59")

            self.main_canvas = self.center_canvas

            self.left_part_width = 200
            self.right_part_width = 200

            self.resize_timer = None
            self.new_window.bind("<Configure>", self.debounced_resize)
            self.update_center_part_width()

            self.resources_held = {}
            self.resources_wanted = {}
            for i in range(self.total_processes):
                process_name = "P" + str(i + 1)
                self.resources_held[process_name] = []
                self.resources_wanted[process_name] = []

            self.process_icon = "🤖"
            self.resource_icon = "🖥️"

            self.process_locations = {}
            self.resource_locations = {}
            self.process_items = {}
            self.resource_items = {}
            self.allocation_labels = []
            self.request_labels = []
            self.history_of_actions = []

            self.phase = "allocation"
            print("Calling show_allocation_phase")
            self.show_allocation_phase(self.total_processes, self.total_resources)

            self.finish_frame = tk.Frame(self.new_window)
            self.finish_frame.pack(pady=5)
            if self.dark_mode_on:
                self.finish_frame.config(bg="#121212")
            else:
                self.finish_frame.config(bg="white")

            self.button_finish = tk.Button(self.finish_frame, text="Finish Allocation", font=("Arial", 12),
                                           command=self.go_to_request_phase)
            self.button_finish.pack()
            if self.dark_mode_on:
                self.button_finish.config(bg="#42A5F5", fg="white")
            else:
                self.button_finish.config(bg="#D3D3D3", fg="black")

            self.detect_frame = tk.Frame(self.new_window)
            self.button_detect_deadlock = tk.Button(self.detect_frame, text="Detect Deadlock", font=("Arial", 14, "bold"),
                                                    bg="red", fg="white", command=self.detect_deadlock)
            self.button_detect_deadlock.pack(fill=tk.X, expand=True)
            self.detect_frame.pack_forget()
            if self.dark_mode_on:
                self.detect_frame.config(bg="#121212")
                self.button_detect_deadlock.config(bg="#D32F2F", fg="white")
            else:
                self.detect_frame.config(bg="white")

            self.status_frame = tk.Frame(self.new_window)
            self.status_frame.pack(pady=5)
            if self.dark_mode_on:
                self.status_frame.config(bg="#121212")
            else:
                self.status_frame.config(bg="white")
            self.status_label = tk.Label(self.status_frame, text="", font=("Arial", 12))
            self.status_label.pack()
            if self.dark_mode_on:
                self.status_label.config(bg="#121212", fg="#A3BFFA")
            else:
                self.status_label.config(bg="white", fg="#2E3A59")

            print("make_canvas completed successfully")
        except Exception as e:
            print(f"Error in make_canvas: {e}")
            messagebox.showerror("Error", f"Failed to create canvas: {e}", parent=self.new_window)

    def make_multi_canvas(self):
        print("make_multi_canvas called")
        try:
            self.total_processes = int(self.entry_processes.get())
            self.total_resources = int(self.entry_resources.get())
            self.instances_per_resource = int(self.entry_instances.get())
            print(f"Processes: {self.total_processes}, Resources: {self.total_resources}, Instances: {self.instances_per_resource}")
            if self.total_processes <= 0 or self.total_resources <= 0 or self.instances_per_resource <= 0:
                messagebox.showerror("Error", "Please enter positive numbers.", parent=self.new_window)
                return
            if self.total_processes > 10 or self.total_resources > 10 or self.instances_per_resource > 10:
                messagebox.showerror("Error", "Maximum 10 processes, resources, and instances allowed.", parent=self.new_window)
                return
        except ValueError:
            messagebox.showerror("Error", "Please enter valid numbers.", parent=self.new_window)
            return

        print("Validation passed, creating UI elements for multi-instance detection")
        try:
            self.entry_processes.config(state="disabled")
            self.entry_resources.config(state="disabled")
            self.entry_instances.config(state="disabled")

            self.button_undo = tk.Button(self.input_area, text="Undo", font=("Arial", 12),
                                         command=self.undo_last_action)
            self.button_undo.pack(side=tk.LEFT, padx=5)

            self.button_reset = tk.Button(self.input_area, text="Reset", font=("Arial", 12),
                                          command=self.reset_everything)
            self.button_reset.pack(side=tk.LEFT, padx=5)

            if self.dark_mode_on:
                self.button_undo.config(bg="#42A5F5", fg="white")
                self.button_reset.config(bg="#42A5F5", fg="white")
            else:
                self.button_undo.config(bg="#D3D3D3", fg="black")
                self.button_reset.config(bg="#D3D3D3", fg="black")

            self.main_area = tk.Frame(self.new_window)
            self.main_area.pack(pady=10, fill=tk.BOTH, expand=True)

            self.left_area = tk.Frame(self.main_area, width=200)
            self.left_area.pack(side=tk.LEFT, fill=tk.Y)
            self.left_canvas = tk.Canvas(self.left_area, width=200)
            self.left_scroll = tk.Scrollbar(self.left_area, orient=tk.VERTICAL, command=self.left_canvas.yview)
            self.left_scroll.pack(side=tk.RIGHT, fill=tk.Y)
            self.left_canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
            self.left_canvas.configure(yscrollcommand=self.left_scroll.set)
            self.left_inner_area = tk.Frame(self.left_canvas)
            self.left_canvas.create_window((0, 0), window=self.left_inner_area, anchor="nw")
            self.left_inner_area.bind("<Configure>", lambda event: self.left_canvas.configure(scrollregion=self.left_canvas.bbox("all")))
            if self.dark_mode_on:
                self.left_canvas.config(bg="#2E3A59")
                self.left_inner_area.config(bg="#2E3A59")
                self.left_canvas.create_text(100, 20, text="Allocations", font=("Arial", 12, "bold"), fill="#A3BFFA")
            else:
                self.left_canvas.config(bg="#E6F0FA")
                self.left_inner_area.config(bg="#E6F0FA")
                self.left_canvas.create_text(100, 20, text="Allocations", font=("Arial", 12, "bold"), fill="#2E3A59")

            self.center_canvas = tk.Canvas(self.main_area)
            self.center_canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
            self.add_gradient(self.center_canvas, "#A3BFFA", "#F3F4F6", 500, 500)
            self.center_canvas.create_text(250, 20, text="Drag and Drop", font=("Arial", 12, "bold"), fill="#2E3A59")

            self.right_area = tk.Frame(self.main_area, width=200)
            self.right_area.pack(side=tk.LEFT, fill=tk.Y)
            self.right_canvas = tk.Canvas(self.right_area, width=200)
            self.right_scroll = tk.Scrollbar(self.right_area, orient=tk.VERTICAL, command=self.right_canvas.yview)
            self.right_scroll.pack(side=tk.RIGHT, fill=tk.Y)
            self.right_canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
            self.right_canvas.configure(yscrollcommand=self.right_scroll.set)
            self.right_inner_area = tk.Frame(self.right_canvas)
            self.right_canvas.create_window((0, 0), window=self.right_inner_area, anchor="nw")
            self.right_inner_area.bind("<Configure>", lambda event: self.right_canvas.configure(scrollregion=self.right_canvas.bbox("all")))
            if self.dark_mode_on:
                self.right_canvas.config(bg="#2E3A59")
                self.right_inner_area.config(bg="#2E3A59")
                self.right_canvas.create_text(100, 20, text="Requests", font=("Arial", 12, "bold"), fill="#A3BFFA")
            else:
                self.right_canvas.config(bg="#E6F0FA")
                self.right_inner_area.config(bg="#E6F0FA")
                self.right_canvas.create_text(100, 20, text="Requests", font=("Arial", 12, "bold"), fill="#2E3A59")

            self.main_canvas = self.center_canvas

            self.left_part_width = 200
            self.right_part_width = 200

            self.resize_timer = None
            self.new_window.bind("<Configure>", self.debounced_resize)
            self.update_center_part_width()

            self.resources_held = {}
            self.resources_wanted = {}
            self.resource_instances = {}
            for i in range(self.total_processes):
                process_name = "P" + str(i + 1)
                self.resources_held[process_name] = []
                self.resources_wanted[process_name] = []
            for i in range(self.total_resources):
                resource_name = "R" + str(i + 1)
                self.resource_instances[resource_name] = self.instances_per_resource

            self.process_icon = "🤖"
            self.resource_icon = "🖥️"

            self.process_locations = {}
            self.resource_locations = {}
            self.process_items = {}
            self.resource_items = {}
            self.allocation_labels = []
            self.request_labels = []
            self.history_of_actions = []

            self.phase = "allocation"
            print("Calling show_allocation_phase for multi-instance")
            self.show_allocation_phase(self.total_processes, self.total_resources)

            self.finish_frame = tk.Frame(self.new_window)
            self.finish_frame.pack(pady=5)
            if self.dark_mode_on:
                self.finish_frame.config(bg="#121212")
            else:
                self.finish_frame.config(bg="white")

            self.button_finish = tk.Button(self.finish_frame, text="Finish Allocation", font=("Arial", 12),
                                           command=self.go_to_request_phase)
            self.button_finish.pack()
            if self.dark_mode_on:
                self.button_finish.config(bg="#42A5F5", fg="white")
            else:
                self.button_finish.config(bg="#D3D3D3", fg="black")

            self.detect_frame = tk.Frame(self.new_window)
            self.button_detect_deadlock = tk.Button(self.detect_frame, text="Detect Deadlock", font=("Arial", 14, "bold"),
                                                    bg="red", fg="white", command=self.detect_deadlock)
            self.button_detect_deadlock.pack(fill=tk.X, expand=True)
            self.detect_frame.pack_forget()
            if self.dark_mode_on:
                self.detect_frame.config(bg="#121212")
                self.button_detect_deadlock.config(bg="#D32F2F", fg="white")
            else:
                self.detect_frame.config(bg="white")

            self.status_frame = tk.Frame(self.new_window)
            self.status_frame.pack(pady=5)
            if self.dark_mode_on:
                self.status_frame.config(bg="#121212")
            else:
                self.status_frame.config(bg="white")
            self.status_label = tk.Label(self.status_frame, text="", font=("Arial", 12))
            self.status_label.pack()
            if self.dark_mode_on:
                self.status_label.config(bg="#121212", fg="#A3BFFA")
            else:
                self.status_label.config(bg="white", fg="#2E3A59")

            print("make_multi_canvas completed successfully")
        except Exception as e:
            print(f"Error in make_multi_canvas: {e}")
            messagebox.showerror("Error", f"Failed to create canvas: {e}", parent=self.new_window)

    def debounced_resize(self, event):
        if self.resize_timer is not None:
            self.new_window.after_cancel(self.resize_timer)
        self.resize_timer = self.new_window.after(100, lambda: self.on_single_window_resize(event))

    def update_center_part_width(self):
        self.center_part_width = self.center_canvas.winfo_width()
        if self.center_part_width < 300:
            self.center_part_width = 300

    def on_single_window_resize(self, event):
        self.update_center_part_width()
        
        new_width = self.center_canvas.winfo_width()
        new_height = self.center_canvas.winfo_height()
        self.center_canvas.delete("all")
        if self.dark_mode_on:
            self.add_gradient(self.center_canvas, "#2E3A59", "#121212", new_width, new_height)
            self.center_canvas.create_text(new_width / 2, 20, text="Drag and Drop" if self.phase != "detection" else "Final State", 
                                          font=("Arial", 12, "bold"), fill="#A3BFFA")
        else:
            self.add_gradient(self.center_canvas, "#A3BFFA", "#F3F4F6", new_width, new_height)
            self.center_canvas.create_text(new_width / 2, 20, text="Drag and Drop" if self.phase != "detection" else "Final State", 
                                          font=("Arial", 12, "bold"), fill="#2E3A59")
        
        if self.phase == "allocation":
            self.show_allocation_phase(self.total_processes, self.total_resources)
        elif self.phase == "request":
            num_processes = len(self.resources_held)
            all_resources = set()
            for resources in self.resources_held.values():
                for r in resources:
                    all_resources.add(r)
            for resources in self.resources_wanted.values():
                for r in resources:
                    all_resources.add(r)
            num_resources = len(all_resources)
            self.show_request_phase(num_processes, num_resources)
        elif self.phase == "detection":
            self.finish_all()

    def show_status(self, message):
        if self.status_after_id is not None:
            self.status_label.after_cancel(self.status_after_id)
            self.status_after_id = None

        self.status_label.config(text=message)
        self.status_after_id = self.status_label.after(3000, lambda: self.status_label.config(text=""))

    def animate_detect_button(self):
        if not self.detect_button_animated:
            self.detect_frame.pack(pady=5, fill=tk.X, side=tk.BOTTOM)
            self.button_detect_deadlock.pack(fill=tk.X, expand=True)
            self.detect_button_animated = True

    def detect_deadlock(self):
        # Hide the center canvas and show the visualization
        self.center_canvas.pack_forget()

        detector = DeadlockDetector(self.resources_held, self.resources_wanted, self.total_resources)
        has_deadlock, message = detector.detect_deadlock()

        # Create the graph visualizer
        self.graph_visualizer = GraphVisualizer(self.main_area, self.resources_held, self.resources_wanted,
                                                self.total_processes, self.total_resources, self.dark_mode_on)

        involved_processes = set()
        if has_deadlock:
            self.show_status(f"Warning: {message}")
            for line in message.split('\n'):
                if "involved in deadlock" in line:
                    for proc in self.resources_held.keys():
                        if proc in line:
                            involved_processes.add(proc)
            for proc in involved_processes:
                if proc in self.process_items:
                    self.main_canvas.itemconfig(self.process_items[proc], fill="red")
        else:
            self.show_status(f"Info: {message}")

        # Draw the graph with the appropriate background color and highlight deadlock
        self.graph_visualizer.draw_graph(has_deadlock, involved_processes if has_deadlock else None)

        # Add the Restart button
        self.restart_frame = tk.Frame(self.new_window)
        self.restart_frame.pack(pady=5)
        self.button_restart = tk.Button(self.restart_frame, text="Restart", font=("Arial", 14, "bold"),
                                        command=self.reset_everything)
        self.button_restart.pack(fill=tk.X, expand=True)
        if self.dark_mode_on:
            self.restart_frame.config(bg="#121212")
            self.button_restart.config(bg="#42A5F5", fg="white")
        else:
            self.restart_frame.config(bg="white")
            self.button_restart.config(bg="#D3D3D3", fg="black")

        # Disable the Detect Deadlock button to prevent multiple visualizations
        self.button_detect_deadlock.config(state="disabled")

    def reset_everything(self):
        # Destroy the visualization if it exists
        if hasattr(self, 'graph_visualizer'):
            self.graph_visualizer.destroy()
            del self.graph_visualizer

        # Destroy the restart button
        if hasattr(self, 'restart_frame'):
            self.restart_frame.destroy()
            del self.restart_frame
            del self.button_restart

        # Re-enable the Detect Deadlock button
        self.button_detect_deadlock.config(state="normal")

        # Show the center canvas again
        self.center_canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.resources_held = {}
        self.resources_wanted = {}
        for i in range(self.total_processes):
            process_name = "P" + str(i + 1)
            self.resources_held[process_name] = []
            self.resources_wanted[process_name] = []
        if hasattr(self, 'resource_instances'):
            for i in range(self.total_resources):
                resource_name = "R" + str(i + 1)
                self.resource_instances[resource_name] = self.instances_per_resource

        self.history_of_actions = []
        self.phase = "allocation"
        self.detect_button_animated = False
        self.message_shown_in_detection = False

        for label in self.left_inner_area.winfo_children():
            label.destroy()
        for label in self.right_inner_area.winfo_children():
            label.destroy()
        self.allocation_labels = []
        self.request_labels = []

        self.process_locations = {}
        self.resource_locations = {}
        self.process_items = {}
        self.resource_items = {}
        self.main_canvas.delete("all")
        new_width = self.main_canvas.winfo_width()
        new_height = self.main_canvas.winfo_height()
        if self.dark_mode_on:
            self.add_gradient(self.main_canvas, "#2E3A59", "#121212", new_width, new_height)
            self.main_canvas.create_text(new_width / 2, 20, text="Drag and Drop", font=("Arial", 12, "bold"), fill="#A3BFFA")
        else:
            self.add_gradient(self.main_canvas, "#A3BFFA", "#F3F4F6", new_width, new_height)
            self.main_canvas.create_text(new_width / 2, 20, text="Drag and Drop", font=("Arial", 12, "bold"), fill="#2E3A59")

        self.show_allocation_phase(self.total_processes, self.total_resources)
        self.button_finish.config(text="Finish Allocation", command=self.go_to_request_phase)
        self.button_finish.pack()
        self.finish_frame.pack(pady=5)
        self.detect_frame.pack_forget()
        self.show_status("")

    def show_allocation_phase(self, num_processes, num_resources):
        print(f"show_allocation_phase called with {num_processes} processes, {num_resources} resources")
        self.main_canvas.delete("all")
        new_width = self.main_canvas.winfo_width()
        new_height = self.main_canvas.winfo_height()
        if self.dark_mode_on:
            self.add_gradient(self.main_canvas, "#2E3A59", "#121212", new_width, new_height)
            self.main_canvas.create_text(new_width / 2, 20, text="Drag and Drop", font=("Arial", 12, "bold"), fill="#A3BFFA")
        else:
            self.add_gradient(self.main_canvas, "#A3BFFA", "#F3F4F6", new_width, new_height)
            self.main_canvas.create_text(new_width / 2, 20, text="Drag and Drop", font=("Arial", 12, "bold"), fill="#2E3A59")
        self.center_items = []

        self.process_items = {}
        self.resource_items = {}

        if num_processes > 0:
            space_between = min(80, (self.center_part_width - 100) / num_processes)
            for i in range(num_processes):
                process_name = "P" + str(i + 1)
                x_position = 50 + i * space_between
                y_position = 100
                fill_color = "#A3BFFA" if self.dark_mode_on else "#1A3C34"
                process_text = self.main_canvas.create_text(x_position, y_position, text=f"{process_name} {self.process_icon}", 
                                                           font=("Arial", 14), tags=process_name, fill=fill_color)
                self.process_locations[process_name] = (x_position, y_position)
                self.process_items[process_name] = process_text
                self.center_items.append(process_text)
                self.main_canvas.tag_unbind(process_name, "<Button-1>")
                self.main_canvas.tag_unbind(process_name, "<B1-Motion>")
                self.main_canvas.tag_unbind(process_name, "<ButtonRelease-1>")
                self.main_canvas.tag_bind(process_name, "<Motion>", lambda event, p=process_name: self.show_info(event, p))

        if num_resources > 0:
            space_between = min(80, (self.center_part_width - 100) / num_resources)
            for i in range(num_resources):
                resource_name = "R" + str(i + 1)
                if not hasattr(self, 'resource_instances'):
                    allocated = False
                    for proc in self.resources_held:
                        if resource_name in self.resources_held[proc]:
                            allocated = True
                            break
                    if not allocated:
                        x_position = 50 + i * space_between
                        y_position = 200
                        fill_color = "#A3BFFA" if self.dark_mode_on else "#1A3C34"
                        resource_text = self.main_canvas.create_text(x_position, y_position, text=f"{resource_name} {self.resource_icon}", 
                                                                    font=("Arial", 14), tags=resource_name, fill=fill_color)
                        self.resource_locations[resource_name] = (x_position, y_position)
                        self.resource_items[resource_name] = resource_text
                        self.center_items.append(resource_text)
                        self.main_canvas.tag_bind(resource_name, "<Button-1>", lambda event, r=resource_name: self.start_dragging(event, r))
                        self.main_canvas.tag_bind(resource_name, "<B1-Motion>", lambda event, r=resource_name: self.drag_item(event, r))
                        self.main_canvas.tag_bind(resource_name, "<ButtonRelease-1>", lambda event, r=resource_name: self.drop_for_allocation(event, r))
                        self.main_canvas.tag_bind(resource_name, "<Motion>", lambda event, r=resource_name: self.show_info(event, r))
                else:
                    x_position = 50 + i * space_between
                    y_position = 200
                    fill_color = "#A3BFFA" if self.dark_mode_on else "#1A3C34"
                    instance_count = self.resource_instances[resource_name]
                    resource_text = self.main_canvas.create_text(x_position, y_position, 
                                                                text=f"{resource_name} {self.resource_icon} ({instance_count})", 
                                                                font=("Arial", 14), tags=resource_name, fill=fill_color)
                    self.resource_locations[resource_name] = (x_position, y_position)
                    self.resource_items[resource_name] = resource_text
                    self.center_items.append(resource_text)
                    if instance_count > 0:
                        self.main_canvas.tag_bind(resource_name, "<Button-1>", lambda event, r=resource_name: self.start_dragging(event, r))
                        self.main_canvas.tag_bind(resource_name, "<B1-Motion>", lambda event, r=resource_name: self.drag_item(event, r))
                        self.main_canvas.tag_bind(resource_name, "<ButtonRelease-1>", lambda event, r=resource_name: self.drop_for_allocation(event, r))
                    self.main_canvas.tag_bind(resource_name, "<Motion>", lambda event, r=resource_name: self.show_info(event, r))
        print("show_allocation_phase completed")

    def show_request_phase(self, num_processes, num_resources):
        print(f"show_request_phase called with {num_processes} processes, {num_resources} resources")
        self.main_canvas.delete("all")
        new_width = self.main_canvas.winfo_width()
        new_height = self.main_canvas.winfo_height()
        if self.dark_mode_on:
            self.add_gradient(self.main_canvas, "#2E3A59", "#121212", new_width, new_height)
            self.main_canvas.create_text(new_width / 2, 20, text="Drag and Drop", font=("Arial", 12, "bold"), fill="#A3BFFA")
        else:
            self.add_gradient(self.main_canvas, "#A3BFFA", "#F3F4F6", new_width, new_height)
            self.main_canvas.create_text(new_width / 2, 20, text="Drag and Drop", font=("Arial", 12, "bold"), fill="#2E3A59")
        self.center_items = []

        self.process_items = {}
        self.resource_items = {}

        if num_processes > 0:
            space_between = min(80, (self.center_part_width - 100) / num_processes)
            for i in range(num_processes):
                process_name = "P" + str(i + 1)
                requested = False
                if process_name in self.resources_wanted and self.resources_wanted[process_name]:
                    requested = True
                if not requested:
                    x_position = 50 + i * space_between
                    y_position = 100
                    fill_color = "#A3BFFA" if self.dark_mode_on else "#1A3C34"
                    process_text = self.main_canvas.create_text(x_position, y_position, text=f"{process_name} {self.process_icon}", 
                                                               font=("Arial", 14), tags=process_name, fill=fill_color)
                    self.process_locations[process_name] = (x_position, y_position)
                    self.process_items[process_name] = process_text
                    self.center_items.append(process_text)
                    self.main_canvas.tag_bind(process_name, "<Button-1>", lambda event, p=process_name: self.start_dragging(event, p))
                    self.main_canvas.tag_bind(process_name, "<B1-Motion>", lambda event, p=process_name: self.drag_item(event, p))
                    self.main_canvas.tag_bind(process_name, "<ButtonRelease-1>", lambda event, p=process_name: self.drop_for_request(event, p))
                    self.main_canvas.tag_bind(process_name, "<Motion>", lambda event, p=process_name: self.show_info(event, p))

        if num_resources > 0:
            space_between = min(80, (self.center_part_width - 100) / num_resources)
            allocated_resources = []
            for process in self.resources_held:
                for resource in self.resources_held[process]:
                    allocated_resources.append(resource)
            for i in range(num_resources):
                resource_name = "R" + str(i + 1)
                x_position = 50 + i * space_between
                y_position = 200
                if resource_name in allocated_resources:
                    color = "red"
                else:
                    color = "green"
                fill_color = "#A3BFFA" if self.dark_mode_on else color
                if hasattr(self, 'resource_instances'):
                    instance_count = self.resource_instances[resource_name]
                    resource_text = self.main_canvas.create_text(x_position, y_position, 
                                                                text=f"{resource_name} {self.resource_icon} ({instance_count})", 
                                                                font=("Arial", 14), tags=resource_name, fill=fill_color)
                else:
                    resource_text = self.main_canvas.create_text(x_position, y_position, 
                                                                text=f"{resource_name} {self.resource_icon}", 
                                                                font=("Arial", 14), tags=resource_name, fill=fill_color)
                self.resource_locations[resource_name] = (x_position, y_position)
                self.resource_items[resource_name] = resource_text
                self.center_items.append(resource_text)
                self.main_canvas.tag_unbind(resource_name, "<Button-1>")
                self.main_canvas.tag_unbind(resource_name, "<B1-Motion>")
                self.main_canvas.tag_unbind(resource_name, "<ButtonRelease-1>")
                self.main_canvas.tag_bind(resource_name, "<Motion>", lambda event, r=resource_name: self.show_info(event, r))
        print("show_request_phase completed")

    def show_info(self, event, item):
        x = event.x
        y = event.y
        if hasattr(self, "tooltip"):
            self.tooltip.destroy()

        if item.startswith("P"):
            process = item
            held = self.resources_held.get(process, [])
            wanted = self.resources_wanted.get(process, [])
            tooltip_text = f"{process}: Holds {held}, Requests {wanted}"
        else:
            resource = item
            holder = None
            for proc in self.resources_held:
                if resource in self.resources_held[proc]:
                    holder = proc
                    break
            requesters = []
            for proc in self.resources_wanted:
                if resource in self.resources_wanted[proc]:
                    requesters.append(proc)
            if hasattr(self, 'resource_instances'):
                instances = self.resource_instances.get(resource, 0)
                tooltip_text = f"{resource}: Held by {holder if holder else 'None'}, Requested by {requesters}, Instances: {instances}"
            else:
                tooltip_text = f"{resource}: Held by {holder if holder else 'None'}, Requested by {requesters}"

        self.tooltip = tk.Toplevel(self.main_canvas)
        self.tooltip.wm_overrideredirect(True)
        self.tooltip.wm_geometry(f"+{self.main_canvas.winfo_rootx() + x + 20}+{self.main_canvas.winfo_rooty() + y}")
        label = tk.Label(self.tooltip, text=tooltip_text, background="yellow", relief="solid", borderwidth=1)
        label.pack()
        self.main_canvas.bind("<Leave>", lambda e: self.hide_info())

    def hide_info(self):
        if hasattr(self, "tooltip"):
            self.tooltip.destroy()
            del self.tooltip

    def start_dragging(self, event, item):
        self.item_being_dragged = item
        self.start_x = event.x
        self.start_y = event.y

    def drag_item(self, event, item):
        dx = event.x - self.start_x
        dy = event.y - self.start_y
        self.main_canvas.move(item, dx, dy)
        self.start_x = event.x
        self.start_y = event.y
        if item.startswith("P"):
            old_x, old_y = self.process_locations[item]
            self.process_locations[item] = (old_x + dx, old_y + dy)
        else:
            old_x, old_y = self.resource_locations[item]
            self.resource_locations[item] = (old_x + dx, old_y + dy)

    def drop_for_allocation(self, event, resource):
        drop_x = event.x
        drop_y = event.y
        target_process = None

        for process in self.process_locations:
            px, py = self.process_locations[process]
            if abs(drop_x - px) < 40 and abs(drop_y - py) < 40:
                target_process = process
                break

        if target_process:
            if not hasattr(self, 'resource_instances'):
                for proc in self.resources_held:
                    if resource in self.resources_held[proc]:
                        messagebox.showerror("Error", f"{resource} is already allocated to {proc}.", parent=self.new_window)
                        self.reset_resource_position(resource)
                        return
            else:
                if self.resource_instances[resource] <= 0:
                    messagebox.showerror("Error", f"No instances of {resource} available.", parent=self.new_window)
                    self.reset_resource_position(resource)
                    return

            self.resources_held[target_process].append(resource)
            if hasattr(self, 'resource_instances'):
                self.resource_instances[resource] -= 1
            self.history_of_actions.append(("allocation", target_process, resource))
            self.sound_manager.play_allocate_sound()
            self.show_allocations()
            self.show_allocation_phase(self.total_processes, self.total_resources)
        else:
            self.reset_resource_position(resource)

    def drop_for_request(self, event, process):
        drop_x = event.x
        drop_y = event.y
        target_resource = None

        for resource in self.resource_locations:
            rx, ry = self.resource_locations[resource]
            if abs(drop_x - rx) < 40 and abs(drop_y - ry) < 40:
                target_resource = resource
                break

        if target_resource:
            if target_resource in self.resources_held[process]:
                messagebox.showerror("Error", f"{process} already holds {target_resource}.", parent=self.new_window)
                self.reset_process_position(process)
                return
            if target_resource in self.resources_wanted[process]:
                messagebox.showerror("Error", f"{process} already requested {target_resource}.", parent=self.new_window)
                self.reset_process_position(process)
                return

            self.resources_wanted[process].append(target_resource)
            self.history_of_actions.append(("request", process, target_resource))
            self.sound_manager.play_request_sound()
            self.show_requests()
            self.show_request_phase(self.total_processes, self.total_resources)
        else:
            self.reset_process_position(process)

    def reset_resource_position(self, resource):
        if resource in self.resource_items:
            space_between = min(80, (self.center_part_width - 100) / self.total_resources)
            original_x = 50 + (int(resource[1:]) - 1) * space_between
            original_y = 200
            self.main_canvas.coords(self.resource_items[resource], original_x, original_y)
            self.resource_locations[resource] = (original_x, original_y)

    def reset_process_position(self, process):
        if process in self.process_items:
            space_between = min(80, (self.center_part_width - 100) / self.total_processes)
            original_x = 50 + (int(process[1:]) - 1) * space_between
            original_y = 100
            self.main_canvas.coords(self.process_items[process], original_x, original_y)
            self.process_locations[process] = (original_x, original_y)

    def show_allocations(self):
        for widget in self.left_inner_area.winfo_children():
            widget.destroy()
        self.allocation_labels = []

        for process in self.resources_held:
            for resource in self.resources_held[process]:
                text = f"{self.process_icon} <------- {self.resource_icon} ({process} <- {resource})"
                label = tk.Label(self.left_inner_area, text=text, font=("Arial", 10))
                label.pack(anchor="center", pady=5)
                self.allocation_labels.append(label)
                if self.dark_mode_on:
                    label.config(bg="#2E3A59", fg="#A3BFFA")
                else:
                    label.config(bg="#E6F0FA", fg="#2E3A59")

        self.left_inner_area.update_idletasks()
        self.left_canvas.configure(scrollregion=self.left_canvas.bbox("all"))

    def show_requests(self):
        for widget in self.right_inner_area.winfo_children():
            widget.destroy()
        self.request_labels = []

        for process in self.resources_wanted:
            for resource in self.resources_wanted[process]:
                text = f"{self.process_icon} -------> {self.resource_icon} ({process} -> {resource})"
                label = tk.Label(self.right_inner_area, text=text, font=("Arial", 10))
                label.pack(anchor="center", pady=5)
                self.request_labels.append(label)
                if self.dark_mode_on:
                    label.config(bg="#2E3A59", fg="#A3BFFA")
                else:
                    label.config(bg="#E6F0FA", fg="#2E3A59")

        self.right_inner_area.update_idletasks()
        self.right_canvas.configure(scrollregion=self.right_canvas.bbox("all"))

    def undo_last_action(self):
        if not self.history_of_actions:
            self.show_status("Info: Nothing to undo.")
            return

        action_type, process, resource = self.history_of_actions.pop()
        if action_type == "allocation":
            self.resources_held[process].remove(resource)
            if hasattr(self, 'resource_instances'):
                self.resource_instances[resource] += 1
            self.show_allocations()
            self.show_allocation_phase(self.total_processes, self.total_resources)
        else:
            self.resources_wanted[process].remove(resource)
            self.show_requests()
            self.show_request_phase(self.total_processes, self.total_resources)

        has_requests = any(self.resources_wanted[process] for process in self.resources_wanted)
        has_allocations = any(self.resources_held[process] for process in self.resources_held)

        if self.phase == "detection":
            if not has_requests and not has_allocations:
                self.phase = "allocation"
                self.button_finish.config(text="Finish Allocation", command=self.go_to_request_phase)
                self.button_finish.pack()
                self.finish_frame.pack(pady=5)
                self.detect_frame.pack_forget()
                self.detect_button_animated = False
                self.message_shown_in_detection = False
                self.show_allocation_phase(self.total_processes, self.total_resources)
            else:
                self.phase = "request"
                self.button_finish.config(text="Finish Request Allocation", command=self.finish_all)
                self.button_finish.pack()
                self.finish_frame.pack(pady=5)
                self.detect_frame.pack_forget()
                self.detect_button_animated = False
                self.message_shown_in_detection = False
                self.show_request_phase(self.total_processes, self.total_resources)
        elif self.phase == "request":
            if not has_requests:
                self.phase = "allocation"
                self.button_finish.config(text="Finish Allocation", command=self.go_to_request_phase)
                self.button_finish.pack()
                self.finish_frame.pack(pady=5)
                self.show_allocation_phase(self.total_processes, self.total_resources)
            else:
                self.show_request_phase(self.total_processes, self.total_resources)

    def go_to_request_phase(self):
        self.phase = "request"
        num_processes = len(self.resources_held)
        all_resources = set()
        for resources in self.resources_held.values():
            for r in resources:
                all_resources.add(r)
        for resources in self.resources_wanted.values():
            for r in resources:
                all_resources.add(r)
        num_resources = len(all_resources)
        self.show_request_phase(num_processes, num_resources)
        self.button_finish.config(text="Finish Request Allocation", command=self.finish_all)

    def finish_all(self):
        self.phase = "detection"
        self.main_canvas.delete("all")
        new_width = self.main_canvas.winfo_width()
        new_height = self.main_canvas.winfo_height()
        if self.dark_mode_on:
            self.add_gradient(self.main_canvas, "#2E3A59", "#121212", new_width, new_height)
            self.main_canvas.create_text(new_width / 2, 20, text="Final State", font=("Arial", 12, "bold"), fill="#A3BFFA")
        else:
            self.add_gradient(self.main_canvas, "#A3BFFA", "#F3F4F6", new_width, new_height)
            self.main_canvas.create_text(new_width / 2, 20, text="Final State", font=("Arial", 12, "bold"), fill="#2E3A59")
        self.center_items = []

        space_between = min(80, (self.center_part_width - 100) / self.total_processes)
        for i in range(self.total_processes):
            process_name = "P" + str(i + 1)
            x_position = 50 + i * space_between
            y_position = 100
            fill_color = "#A3BFFA" if self.dark_mode_on else "#1A3C34"
            process_text = self.main_canvas.create_text(x_position, y_position, text=f"{process_name} {self.process_icon}", 
                                                       font=("Arial", 14), tags=process_name, fill=fill_color)
            self.process_locations[process_name] = (x_position, y_position)
            self.process_items[process_name] = process_text
            self.center_items.append(process_text)
            self.main_canvas.tag_bind(process_name, "<Motion>", lambda event, p=process_name: self.show_info(event, p))

        space_between = min(80, (self.center_part_width - 100) / self.total_resources)
        allocated_resources = []
        for process in self.resources_held:
            for resource in self.resources_held[process]:
                allocated_resources.append(resource)
        for i in range(self.total_resources):
            resource_name = "R" + str(i + 1)
            x_position = 50 + i * space_between
            y_position = 200
            if resource_name in allocated_resources:
                color = "red"
            else:
                color = "green"
            fill_color = "#A3BFFA" if self.dark_mode_on else color
            if hasattr(self, 'resource_instances'):
                instance_count = self.resource_instances[resource_name]
                resource_text = self.main_canvas.create_text(x_position, y_position, 
                                                            text=f"{resource_name} {self.resource_icon} ({instance_count})", 
                                                            font=("Arial", 14), tags=resource_name, fill=fill_color)
            else:
                resource_text = self.main_canvas.create_text(x_position, y_position, 
                                                            text=f"{resource_name} {self.resource_icon}", 
                                                            font=("Arial", 14), tags=resource_name, fill=fill_color)
            self.resource_locations[resource_name] = (x_position, y_position)
            self.resource_items[resource_name] = resource_text
            self.center_items.append(resource_text)
            self.main_canvas.tag_bind(resource_name, "<Motion>", lambda event, r=resource_name: self.show_info(event, r))

        for widget in self.left_inner_area.winfo_children():
            widget.destroy()
        for widget in self.right_inner_area.winfo_children():
            widget.destroy()
        self.allocation_labels = []
        self.request_labels = []

        label_alloc = tk.Label(self.left_inner_area, text="Final Allocations", font=("Arial", 12, "bold"))
        label_alloc.pack(anchor="center", pady=5)
        if self.dark_mode_on:
            label_alloc.config(bg="#2E3A59", fg="#A3BFFA")
        else:
            label_alloc.config(bg="#E6F0FA", fg="#2E3A59")
        for process in self.resources_held:
            for resource in self.resources_held[process]:
                text = f"{self.process_icon} <------- {self.resource_icon} ({process} <- {resource})"
                label = tk.Label(self.left_inner_area, text=text, font=("Arial", 10))
                label.pack(anchor="center", pady=5)
                self.allocation_labels.append(label)
                if self.dark_mode_on:
                    label.config(bg="#2E3A59", fg="#A3BFFA")
                else:
                    label.config(bg="#E6F0FA", fg="#2E3A59")

        label_req = tk.Label(self.right_inner_area, text="Final Requests", font=("Arial", 12, "bold"))
        label_req.pack(anchor="center", pady=5)
        if self.dark_mode_on:
            label_req.config(bg="#2E3A59", fg="#A3BFFA")
        else:
            label_req.config(bg="#E6F0FA", fg="#2E3A59")
        for process in self.resources_wanted:
            for resource in self.resources_wanted[process]:
                text = f"{self.process_icon} -------> {self.resource_icon} ({process} -> {resource})"
                label = tk.Label(self.right_inner_area, text=text, font=("Arial", 10))
                label.pack(anchor="center", pady=5)
                self.request_labels.append(label)
                if self.dark_mode_on:
                    label.config(bg="#2E3A59", fg="#A3BFFA")
                else:
                    label.config(bg="#E6F0FA", fg="#2E3A59")

        self.left_inner_area.update_idletasks()
        self.right_inner_area.update_idletasks()
        self.left_canvas.configure(scrollregion=self.left_canvas.bbox("all"))
        self.right_canvas.configure(scrollregion=self.right_canvas.bbox("all"))

        if not self.message_shown_in_detection:
            self.show_status("All phases completed. Ready to detect deadlock.")
            self.message_shown_in_detection = True

        self.finish_frame.pack_forget()
        self.animate_detect_button()
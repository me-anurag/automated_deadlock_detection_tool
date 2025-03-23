import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

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

        # Data structures to store allocations and requests
        self.allocations = {}  # Format: {process: [list of held resources]}
        self.requests = {}    # Format: {process: [list of requested resources]}

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
        single_window.geometry("1000x700")

        # Input Frame to place fields in a single line
        input_frame = tk.Frame(single_window)
        input_frame.pack(pady=10)

        # Input Fields (in a single line)
        tk.Label(input_frame, text="Processes:", font=("Arial", 12)).pack(side=tk.LEFT, padx=5)
        process_entry = tk.Entry(input_frame, width=5)
        process_entry.pack(side=tk.LEFT, padx=5)

        tk.Label(input_frame, text="Resources:", font=("Arial", 12)).pack(side=tk.LEFT, padx=5)
        resource_entry = tk.Entry(input_frame, width=5)
        resource_entry.pack(side=tk.LEFT, padx=5)

        # Create Canvas Button
        create_button = tk.Button(input_frame, text="Create Canvas", font=("Arial", 12),
                                  command=lambda: self.create_canvas(single_window, process_entry, resource_entry))
        create_button.pack(side=tk.LEFT, padx=10)

    def create_canvas(self, window, process_entry, resource_entry):
        """Create a canvas divided into three parts for allocation phase."""
        try:
            num_processes = int(process_entry.get())
            num_resources = int(resource_entry.get())
            if num_processes <= 0 or num_resources <= 0:
                raise ValueError("Numbers must be positive.")
            if num_processes > 10 or num_resources > 10:
                raise ValueError("Maximum 10 processes and resources allowed.")
        except ValueError as e:
            messagebox.showerror("Invalid Input", str(e))
            return

        # Main Frame to hold all canvases
        main_frame = tk.Frame(window)
        main_frame.pack(pady=10, fill=tk.BOTH, expand=True)

        # Left Canvas (Allocations) with Scrollbar
        self.left_frame = tk.Frame(main_frame, width=200, height=500)
        self.left_frame.pack(side=tk.LEFT, fill=tk.Y)
        self.left_canvas = tk.Canvas(self.left_frame, width=200, height=500, bg="lightgray")
        self.left_scrollbar = tk.Scrollbar(self.left_frame, orient=tk.VERTICAL, command=self.left_canvas.yview)
        self.left_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.left_canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.left_canvas.configure(yscrollcommand=self.left_scrollbar.set)
        self.left_inner_frame = tk.Frame(self.left_canvas, bg="lightgray")
        self.left_canvas.create_window((0, 0), window=self.left_inner_frame, anchor="nw")
        self.left_inner_frame.bind("<Configure>", lambda e: self.left_canvas.configure(scrollregion=self.left_canvas.bbox("all")))
        self.left_canvas.create_text(100, 20, text="Allocations", font=("Arial", 12, "bold"))

        # Center Canvas (Drag and Drop)
        self.center_canvas = tk.Canvas(main_frame, width=500, height=500, bg="lightgray")
        self.center_canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.center_canvas.create_text(250, 20, text="Drag and Drop", font=("Arial", 12, "bold"))

        # Right Canvas (Requests) with Scrollbar
        self.right_frame = tk.Frame(main_frame, width=200, height=500)
        self.right_frame.pack(side=tk.LEFT, fill=tk.Y)
        self.right_canvas = tk.Canvas(self.right_frame, width=200, height=500, bg="lightgray")
        self.right_scrollbar = tk.Scrollbar(self.right_frame, orient=tk.VERTICAL, command=self.right_canvas.yview)
        self.right_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.right_canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.right_canvas.configure(yscrollcommand=self.right_scrollbar.set)
        self.right_inner_frame = tk.Frame(self.right_canvas, bg="lightgray")
        self.right_canvas.create_window((0, 0), window=self.right_inner_frame, anchor="nw")
        self.right_inner_frame.bind("<Configure>", lambda e: self.right_canvas.configure(scrollregion=self.right_canvas.bbox("all")))
        self.right_canvas.create_text(100, 20, text="Requests", font=("Arial", 12, "bold"))

        # Use center_canvas as the main canvas for drag-and-drop
        self.canvas = self.center_canvas

        # Divide the canvas into three parts (for reference in positioning)
        self.left_width = 200
        self.center_width = 500
        self.right_width = 200

        # Initialize allocations and requests
        self.allocations = {f"P{i+1}": [] for i in range(num_processes)}
        self.requests = {f"P{i+1}": [] for i in range(num_processes)}

        # Process and Resource Emojis
        self.process_emoji = "🤖"
        self.resource_emoji = "🖥️"

        # Store positions and canvas objects
        self.process_positions = {}
        self.resource_positions = {}
        self.process_objects = {}
        self.resource_objects = {}
        self.allocation_displays = []
        self.request_displays = []
        self.action_history = []

        # Start with allocation phase
        self.phase = "allocation"
        self.display_allocation_phase(num_processes, num_resources)

        # Finish Allocation Button
        self.finish_button = tk.Button(window, text="Finish Allocation", font=("Arial", 12),
                                       command=self.finish_allocation)
        self.finish_button.pack(pady=5)

        # Undo Button
        self.undo_button = tk.Button(window, text="Undo", font=("Arial", 12),
                                     command=self.undo_action)
        self.undo_button.pack(pady=5)

    def display_allocation_phase(self, num_processes, num_resources):
        """Display processes and resources in the center part for allocation phase."""
        # Clear the center part
        if hasattr(self, "center_items"):
            for item in self.center_items:
                self.canvas.delete(item)
        self.center_items = []

        # Display Processes in the center part
        center_start_x = self.left_width
        if num_processes > 0:
            spacing = min(80, (self.center_width - 100) / (num_processes))
            for i in range(num_processes):
                process_id = f"P{i+1}"
                x = center_start_x + 50 + i * spacing - self.left_width
                y = 100
                process_text = self.canvas.create_text(x, y, text=f"{process_id} {self.process_emoji}", font=("Arial", 14), tags=process_id)
                self.process_positions[process_id] = (x, y)
                self.process_objects[process_id] = process_text
                self.center_items.append(process_text)
                # Add tooltip binding
                self.canvas.tag_bind(process_id, "<Motion>", lambda event, p=process_id: self.show_tooltip(event, p))

        # Display Resources in the center part (draggable)
        if num_resources > 0:
            spacing = min(80, (self.center_width - 100) / (num_resources))
            for i in range(num_resources):
                resource_id = f"R{i+1}"
                x = center_start_x + 50 + i * spacing - self.left_width
                y = 200
                resource_text = self.canvas.create_text(x, y, text=f"{resource_id} {self.resource_emoji}", font=("Arial", 14), tags=resource_id)
                self.resource_positions[resource_id] = (x, y)
                self.resource_objects[resource_id] = resource_text
                self.center_items.append(resource_text)
                # Bind drag events for allocation
                self.canvas.tag_bind(resource_id, "<Button-1>", lambda event, r=resource_id: self.start_drag(event, r))
                self.canvas.tag_bind(resource_id, "<B1-Motion>", lambda event, r=resource_id: self.drag(event, r))
                self.canvas.tag_bind(resource_id, "<ButtonRelease-1>", lambda event, r=resource_id: self.drop_allocation(event, r))
                # Add tooltip binding
                self.canvas.tag_bind(resource_id, "<Motion>", lambda event, r=resource_id: self.show_tooltip(event, r))

    def display_request_phase(self, num_processes, num_resources):
        """Display processes and resources in the center part for request phase."""
        # Clear the center part
        for item in self.center_items:
            self.canvas.delete(item)
        self.center_items = []

        # Display Processes in the center part (draggable)
        center_start_x = self.left_width
        if num_processes > 0:
            spacing = min(80, (self.center_width - 100) / (num_processes))
            for i in range(num_processes):
                process_id = f"P{i+1}"
                x = center_start_x + 50 + i * spacing - self.left_width
                y = 100
                process_text = self.canvas.create_text(x, y, text=f"{process_id} {self.process_emoji}", font=("Arial", 14), tags=process_id)
                self.process_positions[process_id] = (x, y)
                self.process_objects[process_id] = process_text
                self.center_items.append(process_text)
                # Bind drag events for request
                self.canvas.tag_bind(process_id, "<Button-1>", lambda event, p=process_id: self.start_drag(event, p))
                self.canvas.tag_bind(process_id, "<B1-Motion>", lambda event, p=process_id: self.drag(event, p))
                self.canvas.tag_bind(process_id, "<ButtonRelease-1>", lambda event, p=process_id: self.drop_request(event, p))
                # Add tooltip binding
                self.canvas.tag_bind(process_id, "<Motion>", lambda event, p=process_id: self.show_tooltip(event, p))

        # Display ALL Resources in the center part (not draggable)
        if num_resources > 0:
            spacing = min(80, (self.center_width - 100) / (num_resources))
            allocated_resources = set(r for resources in self.allocations.values() for r in resources)
            for i in range(num_resources):
                resource_id = f"R{i+1}"
                x = center_start_x + 50 + i * spacing - self.left_width
                y = 200
                fill_color = "red" if resource_id in allocated_resources else "green"
                resource_text = self.canvas.create_text(x, y, text=f"{resource_id} {self.resource_emoji}", font=("Arial", 14), tags=resource_id, fill=fill_color)
                self.resource_positions[resource_id] = (x, y)
                self.resource_objects[resource_id] = resource_text
                self.center_items.append(resource_text)
                # Ensure no drag bindings are applied to resources in request phase
                self.canvas.tag_unbind(resource_id, "<Button-1>")
                self.canvas.tag_unbind(resource_id, "<B1-Motion>")
                self.canvas.tag_unbind(resource_id, "<ButtonRelease-1>")
                # Add tooltip binding
                self.canvas.tag_bind(resource_id, "<Motion>", lambda event, r=resource_id: self.show_tooltip(event, r))

    def show_tooltip(self, event, item):
        """Show a tooltip with the item's state."""
        x, y = event.x, event.y
        if hasattr(self, "tooltip"):
            self.tooltip.destroy()

        if item.startswith("P"):
            process = item
            held_resources = self.allocations.get(process, [])
            requested_resources = self.requests.get(process, [])
            tooltip_text = f"{process}: Holds {held_resources}, Requests {requested_resources}"
        else:
            resource = item
            holder = None
            for proc, resources in self.allocations.items():
                if resource in resources:
                    holder = proc
                    break
            requesters = [proc for proc, reqs in self.requests.items() if resource in reqs]
            tooltip_text = f"{resource}: Held by {holder if holder else 'None'}, Requested by {requesters}"

        self.tooltip = tk.Toplevel(self.canvas)
        self.tooltip.wm_overrideredirect(True)
        self.tooltip.wm_geometry(f"+{self.canvas.winfo_rootx() + x + 20}+{self.canvas.winfo_rooty() + y}")
        label = tk.Label(self.tooltip, text=tooltip_text, background="yellow", relief="solid", borderwidth=1)
        label.pack()
        self.canvas.bind("<Leave>", lambda e: self.hide_tooltip())

    def hide_tooltip(self):
        """Hide the tooltip."""
        if hasattr(self, "tooltip"):
            self.tooltip.destroy()
            del self.tooltip

    def start_drag(self, event, item):
        """Start dragging an item (process or resource)."""
        self.current_item = item
        self.start_x = event.x
        self.start_y = event.y

    def drag(self, event, item):
        """Move the item while dragging."""
        dx = event.x - self.start_x
        dy = event.y - self.start_y
        self.canvas.move(item, dx, dy)
        self.start_x = event.x
        self.start_y = event.y
        # Update position
        if item.startswith("P"):
            self.process_positions[item] = (self.process_positions[item][0] + dx,
                                           self.process_positions[item][1] + dy)
        else:
            self.resource_positions[item] = (self.resource_positions[item][0] + dx,
                                            self.resource_positions[item][1] + dy)

    def drop_allocation(self, event, resource):
        """Handle dropping a resource onto a process (allocation)."""
        drop_x, drop_y = event.x, event.y
        target_process = None

        # Check if the resource was dropped on a process
        for process, (px, py) in self.process_positions.items():
            if abs(drop_x - px) < 40 and abs(drop_y - py) < 40:
                target_process = process
                break

        if target_process:
            # In single-instance mode, a resource can only be allocated to one process
            for proc, resources in self.allocations.items():
                if resource in resources:
                    messagebox.showerror("Invalid Allocation", f"{resource} is already allocated to {proc}.")
                    self.reset_resource_position(resource)
                    return

            # Update allocation
            self.allocations[target_process].append(resource)
            self.action_history.append(("allocation", target_process, resource))
            # Remove the resource icon from the center canvas
            self.canvas.delete(self.resource_objects[resource])
            self.center_items.remove(self.resource_objects[resource])
            del self.resource_objects[resource]
            # Display allocation in the left part
            self.display_allocations()
        else:
            # Reset resource position
            self.reset_resource_position(resource)

    def drop_request(self, event, process):
        """Handle dropping a process onto a resource (request)."""
        drop_x, drop_y = event.x, event.y
        target_resource = None

        # Check if the process was dropped on a resource
        for resource, (rx, ry) in self.resource_positions.items():
            if abs(drop_x - rx) < 40 and abs(drop_y - ry) < 40:
                target_resource = resource
                break

        if target_resource:
            # Debug: Print the current state of allocations for this process
            print(f"Allocations for {process}: {self.allocations[process]}")
            # Check if the current process already holds the resource
            if target_resource in self.allocations[process]:
                messagebox.showerror("Invalid Request", f"{process} already holds {target_resource}.")
                self.reset_process_position(process)
                return
            # Check if the process already requested this resource
            if target_resource in self.requests[process]:
                messagebox.showerror("Invalid Request", f"{process} already requested {target_resource}.")
                self.reset_process_position(process)
                return

            # Update request
            self.requests[process].append(target_resource)
            self.action_history.append(("request", process, target_resource))
            # Remove the process icon from the center canvas
            self.canvas.delete(self.process_objects[process])
            self.center_items.remove(self.process_objects[process])
            del self.process_objects[process]
            # Display request in the right part
            self.display_requests()
        else:
            # Reset process position
            self.reset_process_position(process)

    def reset_resource_position(self, resource):
        """Reset a resource to its original position."""
        if resource in self.resource_objects:
            original_x = self.left_width + 50 + (int(resource[1:]) - 1) * 80 - self.left_width
            original_y = 200
            self.canvas.coords(self.resource_objects[resource], original_x, original_y)
            self.resource_positions[resource] = (original_x, original_y)

    def reset_process_position(self, process):
        """Reset a process to its original position."""
        if process in self.process_objects:
            original_x = self.left_width + 50 + (int(process[1:]) - 1) * 80 - self.left_width
            original_y = 100
            self.canvas.coords(self.process_objects[process], original_x, original_y)
            self.process_positions[process] = (original_x, original_y)

    def display_allocations(self):
        """Display current allocations in the left part of the canvas with scrollbar."""
        # Clear previous allocation displays
        for widget in self.left_inner_frame.winfo_children():
            widget.destroy()
        self.allocation_displays = []

        # Debug: Print the current allocations
        print("Displaying allocations:", self.allocations)

        # Display allocations
        for process, resources in self.allocations.items():
            for resource in resources:
                text = f"{self.process_emoji} <------- {self.resource_emoji} ({process} -> {resource})"
                label = tk.Label(self.left_inner_frame, text=text, font=("Arial", 10), bg="lightgray")
                label.pack(anchor="center", pady=5)  # Use pack instead of place
                self.allocation_displays.append(label)

        # Update the scroll region to include all labels
        self.left_inner_frame.update_idletasks()  # Ensure the frame is updated
        self.left_canvas.configure(scrollregion=self.left_canvas.bbox("all"))

    def display_requests(self):
        """Display current requests in the right part of the canvas with scrollbar."""
        # Clear previous request displays
        for widget in self.right_inner_frame.winfo_children():
            widget.destroy()
        self.request_displays = []

        # Debug: Print the current requests
        print("Displaying requests:", self.requests)

        # Display requests
        for process, resources in self.requests.items():
            for resource in resources:
                text = f"{self.process_emoji} -------> {self.resource_emoji} ({process} -> {resource})"
                label = tk.Label(self.right_inner_frame, text=text, font=("Arial", 10), bg="lightgray")
                label.pack(anchor="center", pady=5)  # Use pack instead of place
                self.request_displays.append(label)

        # Update the scroll region to include all labels
        self.right_inner_frame.update_idletasks()  # Ensure the frame is updated
        self.right_canvas.configure(scrollregion=self.right_canvas.bbox("all"))

    def undo_action(self):
        """Undo the last allocation or request."""
        if not self.action_history:
            messagebox.showinfo("Undo", "No actions to undo.")
            return

        action_type, process, resource = self.action_history.pop()
        if action_type == "allocation":
            self.allocations[process].remove(resource)
            self.display_allocations()
            # Re-display the resource icon on the center canvas
            original_x = self.left_width + 50 + (int(resource[1:]) - 1) * 80 - self.left_width
            original_y = 200
            resource_text = self.canvas.create_text(original_x, original_y, text=f"{resource} {self.resource_emoji}", font=("Arial", 14), tags=resource)
            self.resource_positions[resource] = (original_x, original_y)
            self.resource_objects[resource] = resource_text
            self.center_items.append(resource_text)
            # Re-bind drag events for allocation phase
            if self.phase == "allocation":
                self.canvas.tag_bind(resource, "<Button-1>", lambda event, r=resource: self.start_drag(event, r))
                self.canvas.tag_bind(resource, "<B1-Motion>", lambda event, r=resource: self.drag(event, r))
                self.canvas.tag_bind(resource, "<ButtonRelease-1>", lambda event, r=resource: self.drop_allocation(event, r))
                # Add tooltip binding
                self.canvas.tag_bind(resource, "<Motion>", lambda event, r=resource: self.show_tooltip(event, r))
        else:  # request
            self.requests[process].remove(resource)
            self.display_requests()
            # Re-display the process icon on the center canvas
            original_x = self.left_width + 50 + (int(process[1:]) - 1) * 80 - self.left_width
            original_y = 100
            process_text = self.canvas.create_text(original_x, original_y, text=f"{process} {self.process_emoji}", font=("Arial", 14), tags=process)
            self.process_positions[process] = (original_x, original_y)
            self.process_objects[process] = process_text
            self.center_items.append(process_text)
            # Re-bind drag events for request phase
            if self.phase == "request":
                self.canvas.tag_bind(process, "<Button-1>", lambda event, p=process: self.start_drag(event, p))
                self.canvas.tag_bind(process, "<B1-Motion>", lambda event, p=process: self.drag(event, p))
                self.canvas.tag_bind(process, "<ButtonRelease-1>", lambda event, p=process: self.drop_request(event, p))
                # Add tooltip binding
                self.canvas.tag_bind(process, "<Motion>", lambda event, p=process: self.show_tooltip(event, p))

    def finish_allocation(self):
        """Transition to the request phase."""
        self.phase = "request"
        num_processes = len(self.allocations)
        num_resources = len(set(r for resources in self.allocations.values() for r in resources) | set(r for resources in self.requests.values() for r in resources))
        self.display_request_phase(num_processes, num_resources)
        self.finish_button.config(text="Finish Request Allocation", command=self.finish_request_allocation)

    def finish_request_allocation(self):
        """Finish the request allocation phase and prepare for deadlock detection."""
        print("Allocations:", self.allocations)
        print("Requests:", self.requests)
        messagebox.showinfo("Finished", "Allocation and request phases completed. Check console for details.")

    def open_multi_instance(self):
        print("Opening Multi-Instance Resource Detection...")
        # TODO: Implement navigation to Multi-Instance Detection Page

# Run the GUI
if __name__ == "__main__":
    root = tk.Tk()
    app = DeadlockDetectionGUI(root)
    root.mainloop()
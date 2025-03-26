# src/visualization.py
import tkinter as tk

class GraphVisualizer:
    def __init__(self, parent, resources_held, resources_wanted, total_processes, total_resources, dark_mode_on):
        self.parent = parent
        self.resources_held = resources_held
        self.resources_wanted = resources_wanted
        self.total_processes = total_processes
        self.total_resources = total_resources
        self.dark_mode_on = dark_mode_on

        # Create a frame for the visualization
        self.viz_frame = tk.Frame(self.parent)
        self.viz_frame.pack(pady=10, fill=tk.BOTH, expand=True)

        # Create a canvas for drawing the graph
        self.canvas = tk.Canvas(self.viz_frame, highlightthickness=0)
        self.canvas.pack(fill=tk.BOTH, expand=True)

        # Node positions and sizes
        self.process_nodes = {}
        self.resource_nodes = {}
        self.node_radius = 30
        self.node_spacing = 100

        # Colors
        self.process_color = "#A3BFFA" if self.dark_mode_on else "#1A3C34"
        self.resource_color = "#A3BFFA" if self.dark_mode_on else "#1A3C34"
        self.allocation_edge_color = "blue"
        self.request_edge_color = "orange"
        self.deadlock_color = "red"
        self.default_background = "#2E3A59" if self.dark_mode_on else "#E6F0FA"

        # Initialize the canvas background
        self.canvas.config(bg=self.default_background)

    def draw_graph(self, deadlock_detected, involved_processes=None):
        # Clear the canvas
        self.canvas.delete("all")

        # Set the background color based on deadlock detection
        if deadlock_detected:
            self.canvas.config(bg="red")
        else:
            self.canvas.config(bg="green")

        # Calculate positions for processes and resources
        canvas_width = self.canvas.winfo_width()
        canvas_height = self.canvas.winfo_height()

        # Place processes in a row at the top
        process_y = 100
        process_spacing = min(self.node_spacing, (canvas_width - 2 * self.node_spacing) / max(1, self.total_processes - 1))
        for i in range(self.total_processes):
            process_name = f"P{i+1}"
            x = self.node_spacing + i * process_spacing
            self.process_nodes[process_name] = (x, process_y)
            # Draw process node (circle)
            color = self.deadlock_color if involved_processes and process_name in involved_processes else self.process_color
            self.canvas.create_oval(x - self.node_radius, process_y - self.node_radius,
                                    x + self.node_radius, process_y + self.node_radius,
                                    fill=color, outline="black")
            self.canvas.create_text(x, process_y, text=process_name, font=("Arial", 12, "bold"))

        # Place resources in a row at the bottom
        resource_y = canvas_height - 100
        resource_spacing = min(self.node_spacing, (canvas_width - 2 * self.node_spacing) / max(1, self.total_resources - 1))
        for i in range(self.total_resources):
            resource_name = f"R{i+1}"
            x = self.node_spacing + i * resource_spacing
            self.resource_nodes[resource_name] = (x, resource_y)
            # Draw resource node (rectangle)
            color = self.deadlock_color if involved_processes and any(resource_name in self.resources_held[p] or resource_name in self.resources_wanted[p] for p in involved_processes) else self.resource_color
            self.canvas.create_rectangle(x - self.node_radius, resource_y - self.node_radius,
                                         x + self.node_radius, resource_y + self.node_radius,
                                         fill=color, outline="black")
            self.canvas.create_text(x, resource_y, text=resource_name, font=("Arial", 12, "bold"))

        # Draw allocation edges (resource -> process)
        for process in self.resources_held:
            for resource in self.resources_held[process]:
                if process in self.process_nodes and resource in self.resource_nodes:
                    px, py = self.process_nodes[process]
                    rx, ry = self.resource_nodes[resource]
                    # Draw an arrow from resource to process
                    self.canvas.create_line(rx, ry, px, py, fill=self.allocation_edge_color, arrow=tk.LAST,
                                            width=2 if involved_processes and process in involved_processes else 1)

        # Draw request edges (process -> resource)
        for process in self.resources_wanted:
            for resource in self.resources_wanted[process]:
                if process in self.process_nodes and resource in self.resource_nodes:
                    px, py = self.process_nodes[process]
                    rx, ry = self.resource_nodes[resource]
                    # Draw an arrow from process to resource
                    self.canvas.create_line(px, py, rx, ry, fill=self.request_edge_color, arrow=tk.LAST,
                                            width=2 if involved_processes and process in involved_processes else 1)

    def destroy(self):
        self.viz_frame.destroy()
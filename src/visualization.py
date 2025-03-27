import matplotlib.pyplot as plt
from matplotlib.patches import Circle, Rectangle, FancyArrowPatch
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
import tkinter as tk
import networkx as nx
import numpy as np

def visualize_rag(graph, cycle=None):
    """Visualizes the Resource Allocation Graph (RAG) and Wait-For Graph with vibrant colors, straight solid arrows with arrowheads in the middle, curvy deadlock cycle arrows, and improved labeling.

    Args:
        graph (dict): The RAG as an adjacency list from DeadlockDetector.build_rag().
        cycle (list, optional): List of nodes in the deadlock cycle, if detected.
    """
    # Calculate number of nodes for dynamic scaling
    num_nodes = len(graph)
    num_processes = sum(1 for node in graph if node.startswith("P"))
    num_resources = sum(1 for node in graph if node.startswith("R"))

    # Dynamic figure and window size
    fig_width = max(12, num_nodes * 0.8)
    fig_height = max(6, num_nodes * 0.4)
    window_width = max(1200, int(fig_width * 100))
    window_height = max(800, int(fig_height * 100))

    # Create Tkinter window
    root = tk.Tk()
    root.title("Resource Allocation Graph Visualization")
    root.geometry(f"{window_width}x{window_height}")

    # Set up figure with two subplots
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(fig_width, fig_height), dpi=100)
    fig.suptitle("Deadlock Analysis", fontsize=16, fontweight="bold", y=1.05)

    # --- Helper Function to Adjust Axes Limits ---
    def adjust_axes_limits(ax, positions, padding=0.5):
        if not positions:
            ax.set_xlim(-1, 1)
            ax.set_ylim(-1, 1)
            return
        x_coords, y_coords = zip(*positions.values())
        x_min, x_max = min(x_coords), max(x_coords)
        y_min, y_max = min(y_coords), max(y_coords)
        x_range = x_max - x_min if x_max != x_min else 1
        y_range = y_max - y_min if y_max != y_min else 1
        ax.set_xlim(x_min - padding * x_range, x_max + padding * x_range)
        ax.set_ylim(y_min - padding * y_range, y_max + padding * y_range)

    # --- Helper Function to Draw Straight Arrow with Arrowhead in the Middle ---
    def draw_straight_arrow(ax, start, end, color, label, linestyle="-", zorder=3):
        x1, y1 = start
        x2, y2 = end
        mid_x, mid_y = (x1 + x2) / 2, (y1 + y2) / 2
        # Draw first segment (start to midpoint)
        ax.plot([x1, mid_x], [y1, mid_y], color=color, linestyle=linestyle, linewidth=2, zorder=zorder)
        # Draw second segment with arrowhead at the midpoint
        arrow = FancyArrowPatch((mid_x, mid_y), (x2, y2), color=color, arrowstyle="->", mutation_scale=20, linewidth=2, linestyle=linestyle, zorder=zorder)
        ax.add_patch(arrow)
        # Add label near the midpoint
        label_x, label_y = mid_x, mid_y
        if x1 < x2:  # Rightward arrow
            label_offset = (0, 10)
        else:  # Leftward arrow
            label_offset = (0, -10)
        ax.annotate(label, (label_x, label_y), fontsize=7, color="black", ha="center", va="center",
                    xytext=label_offset, textcoords="offset points", bbox=dict(boxstyle="round,pad=0.3", fc="white", ec="none", alpha=0.8), zorder=4)

    # --- Resource Allocation Graph (RAG) ---
    ax1.set_title("Resource Allocation Graph", fontsize=14, fontweight="bold", pad=15)
    ax1.axis("off")

    # Build NetworkX graph for layout
    G_rag = nx.DiGraph()
    for node, neighbors in graph.items():
        G_rag.add_node(node)
        for neighbor in neighbors:
            G_rag.add_edge(node, neighbor)

    # Use a bipartite layout: processes on the left, resources on the right
    pos_rag = {}
    process_nodes = [node for node in graph if node.startswith("P")]
    resource_nodes = [node for node in graph if node.startswith("R")]

    # Position processes on the left (x=0)
    for i, node in enumerate(process_nodes):
        pos_rag[node] = (0, 1 - (i / max(1, len(process_nodes) - 1)))

    # Position resources on the right (x=1)
    for i, node in enumerate(resource_nodes):
        pos_rag[node] = (1, 1 - (i / max(1, len(resource_nodes) - 1)))

    # Process nodes (circles with glowing aura)
    process_positions = {}
    node_size = 0.05
    for node in process_nodes:
        x, y = pos_rag[node]
        process_positions[node] = (x, y)
        # Glowing aura
        aura = Circle((x, y), node_size * 1.5, fill=True, color="#66B2FF", alpha=0.3, zorder=1)
        ax1.add_patch(aura)
        # Process node
        circle = Circle((x, y), node_size, fill=True, color="#66B2FF", edgecolor="black", linewidth=1.5, zorder=2)
        ax1.add_patch(circle)
        ax1.text(x, y, node, ha="center", va="center", fontsize=10, fontweight="bold", color="white", zorder=3)

    # Resource nodes (rectangles with a dot and glowing aura)
    resource_positions = {}
    for node in resource_nodes:
        x, y = pos_rag[node]
        resource_positions[node] = (x, y)
        # Glowing aura
        aura = Rectangle((x - 0.075, y - 0.045), 0.15, 0.09, fill=True, color="#FF6F61", alpha=0.3, zorder=1)
        ax1.add_patch(aura)
        # Resource node
        rect = Rectangle((x - 0.05, y - 0.03), 0.1, 0.06, fill=True, color="#FF6F61", edgecolor="black", linewidth=1.5, zorder=2)
        ax1.add_patch(rect)
        # Add a dot inside the rectangle to denote single instance
        dot = Circle((x, y), 0.01, fill=True, color="black", zorder=3)
        ax1.add_patch(dot)
        ax1.text(x, y + 0.05, node, ha="center", va="center", fontsize=10, fontweight="bold", color="black", zorder=3)

    # Allocation edges (R -> P, straight solid teal, arrowhead in the middle)
    for resource in resource_nodes:
        for process in graph[resource]:
            rx, ry = resource_positions[resource]
            px, py = process_positions[process]
            draw_straight_arrow(ax1, (rx, ry), (px, py), "#26A69A", f"{process} is holding {resource}", zorder=3)

    # Request edges (P -> R, straight dashed coral, arrowhead in the middle)
    for process in process_nodes:
        for resource in graph[process]:
            px, py = process_positions[process]
            rx, ry = resource_positions[resource]
            draw_straight_arrow(ax1, (px, py), (rx, ry), "#FF6F61", f"{process} is waiting for {resource}", linestyle="--", zorder=3)

    # Highlight deadlock cycle (curvy yellow dashed, lower z-order)
    if cycle:
        for i in range(len(cycle) - 1):
            node1, node2 = cycle[i], cycle[i + 1]
            if node1 in process_positions and node2 in resource_positions:
                px, py = process_positions[node1]
                rx, ry = resource_positions[node2]
                arrow = FancyArrowPatch((px, py), (rx, ry), color="#FFD700", arrowstyle="->", linestyle="--", mutation_scale=25, linewidth=2.5,
                                        connectionstyle="arc3,rad=0.3", zorder=2, alpha=0.7)
                ax1.add_patch(arrow)
            elif node1 in resource_positions and node2 in process_positions:
                rx, ry = resource_positions[node1]
                px, py = process_positions[node2]
                arrow = FancyArrowPatch((rx, ry), (px, py), color="#FFD700", arrowstyle="->", linestyle="--", mutation_scale=25, linewidth=2.5,
                                        connectionstyle="arc3,rad=0.3", zorder=2, alpha=0.7)
                ax1.add_patch(arrow)

    # Adjust RAG axes limits
    all_positions = {**process_positions, **resource_positions}
    adjust_axes_limits(ax1, all_positions, padding=0.3)

    # --- Wait-For Graph ---
    ax2.set_title("Wait-For Graph", fontsize=14, fontweight="bold", pad=15)
    ax2.axis("off")

    # Build wait-for graph
    G_wait = nx.DiGraph()
    process_nodes = [node for node in graph if node.startswith("P")]
    G_wait.add_nodes_from(process_nodes)
    wait_edges = []
    for process in graph:
        if process.startswith("P"):
            for resource in graph[process]:
                for holder in graph[resource]:
                    if holder != process:
                        wait_edges.append((process, holder))
                        G_wait.add_edge(process, holder)

    # Use a circular layout for the Wait-For Graph
    pos_wait = nx.circular_layout(G_wait, scale=1.0)

    # Process nodes (circles with glowing aura)
    wait_positions = {}
    for process in process_nodes:
        x, y = pos_wait[process] if process in pos_wait else (0, 0)
        wait_positions[process] = (x, y)
        # Glowing aura
        aura = Circle((x, y), node_size * 1.5, fill=True, color="#66B2FF", alpha=0.3, zorder=1)
        ax2.add_patch(aura)
        # Process node
        circle = Circle((x, y), node_size, fill=True, color="#66B2FF", edgecolor="black", linewidth=1.5, zorder=2)
        ax2.add_patch(circle)
        ax2.text(x, y, process, ha="center", va="center", fontsize=10, fontweight="bold", color="white", zorder=3)

    # Wait-for edges (straight solid purple, arrowhead in the middle)
    for p1, p2 in wait_edges:
        x1, y1 = wait_positions[p1]
        x2, y2 = wait_positions[p2]
        draw_straight_arrow(ax2, (x1, y1), (x2, y2), "#AB47BC", f"{p1} waits for {p2}", zorder=3)

    # Highlight deadlock cycle in wait-for graph (curvy yellow dashed)
    if cycle:
        process_cycle = [node for node in cycle if node.startswith("P")]
        if len(process_cycle) > 1:
            for i in range(len(process_cycle)):
                p1 = process_cycle[i]
                p2 = process_cycle[(i + 1) % len(process_cycle)]
                if (p1, p2) in wait_edges or (p1, p2) in [(p, q) for p, q in wait_edges]:
                    x1, y1 = wait_positions[p1]
                    x2, y2 = wait_positions[p2]
                    arrow = FancyArrowPatch((x1, y1), (x2, y2), color="#FFD700", arrowstyle="->", linestyle="--", mutation_scale=25, linewidth=2.5,
                                            connectionstyle="arc3,rad=0.3", zorder=2, alpha=0.7)
                    ax2.add_patch(arrow)

    # Adjust Wait-For axes limits
    adjust_axes_limits(ax2, wait_positions, padding=0.3)

    # Add legends
    legend_elements1 = [
        plt.Line2D([0], [0], color="#26A69A", lw=2, label="Allocation (R → P)"),
        plt.Line2D([0], [0], color="#FF6F61", lw=2, ls="--", label="Request (P → R)")
    ]
    if cycle:
        legend_elements1.append(plt.Line2D([0], [0], color="#FFD700", lw=2.5, ls="--", label="Deadlock Cycle"))
    ax1.legend(handles=legend_elements1, loc="upper center", bbox_to_anchor=(0.5, -0.05), fontsize=8, frameon=True, edgecolor="black", facecolor="white")

    legend_elements2 = [plt.Line2D([0], [0], color="#AB47BC", lw=2, label="Wait-For (P → P)")]
    if cycle and len(process_cycle) > 1:
        legend_elements2.append(plt.Line2D([0], [0], color="#FFD700", lw=2.5, ls="--", label="Deadlock Cycle"))
    ax2.legend(handles=legend_elements2, loc="upper center", bbox_to_anchor=(0.5, -0.05), fontsize=8, frameon=True, edgecolor="black", facecolor="white")

    # Adjust layout
    plt.tight_layout(rect=[0, 0, 1, 0.95])

    # Embed in Tkinter with toolbar
    canvas = FigureCanvasTkAgg(fig, master=root)
    canvas.draw()
    canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

    toolbar = NavigationToolbar2Tk(canvas, root)
    toolbar.update()
    toolbar.pack(side=tk.TOP, fill=tk.X)

    # Close button
    close_button = tk.Button(root, text="Close", command=root.destroy, font=("Arial", 12), bg="#D32F2F", fg="white", relief="raised", bd=3)
    close_button.pack(pady=10)
    close_button.bind("<Enter>", lambda e: close_button.config(bg="#B71C1C"))
    close_button.bind("<Leave>", lambda e: close_button.config(bg="#D32F2F"))

    root.mainloop()

if __name__ == "__main__":
    # Sample graph matching the screenshot
    sample_graph = {
        "P1": ["R2"],
        "P2": ["R1"],
        "P3": ["R2"],
        "R1": ["P1"],
        "R2": ["P2"],
        "R3": ["P3"]
    }
    sample_cycle = ["P1", "R2", "P2", "R1", "P1"]
    visualize_rag(sample_graph, sample_cycle)
import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch

def visualize_multi_rag(rag, flat_allocation, need, safe_sequence=None):
    """Visualizes the Resource Allocation Graph (RAG) for a multi-instance system.

    Args:
        rag (dict): Dict mapping nodes (processes/resources) to their neighbors.
        flat_allocation (dict): Flattened allocation matrix for visualization.
        need (dict): Need matrix for determining request edges.
        safe_sequence (list, optional): The safe sequence determined by the deadlock detector.
    """
    print("Visualizing RAG...")  # Debug print
    print("RAG:", rag)
    print("Flat Allocation:", flat_allocation)
    print("Need:", need)
    print("Safe Sequence:", safe_sequence)

    # Create RAG
    G_rag = nx.DiGraph()
    processes = [node for node in rag if node.startswith("P")]
    resources = [node for node in rag if node.startswith("R")]

    print("Processes:", processes)
    print("Resources:", resources)

    # Add nodes
    for p in processes:
        G_rag.add_node(p, type="process")
    for r in resources:
        G_rag.add_node(r, type="resource")

    # Add edges for RAG with instance counts
    for p in processes:
        for r in rag[p]:  # Request edges (P -> R)
            instances_needed = need[p][r]
            if instances_needed > 0:
                G_rag.add_edge(p, r, type="request", instances=instances_needed)
    for r in resources:
        for p in rag[r]:  # Allocation edges (R -> P)
            instances_allocated = flat_allocation[p].count(r)
            if instances_allocated > 0:
                G_rag.add_edge(r, p, type="allocation", instances=instances_allocated)

    # Determine status based on safe sequence
    if safe_sequence:
        status = f"Safe Sequence: {safe_sequence}"
        status_color = "green"
    else:
        status = "No Safe Execution Sequence Found"
        status_color = "orange"

    # Visualization
    fig, ax = plt.subplots(figsize=(8, 6))

    # RAG Visualization
    pos_rag = {}
    for i, r in enumerate(resources):
        pos_rag[r] = (i * 0.5, 1)  # Resources at the top
    for i, p in enumerate(processes):
        pos_rag[p] = (i * 0.5, 0)  # Processes at the bottom

    node_colors_rag = []
    for node in G_rag.nodes():
        if G_rag.nodes[node]["type"] == "process":
            node_colors_rag.append("lightblue")
        else:
            node_colors_rag.append("lightgreen")

    nx.draw_networkx_nodes(G_rag, pos_rag, node_color=node_colors_rag, node_size=500, ax=ax)
    nx.draw_networkx_labels(G_rag, pos_rag, ax=ax)

    for edge in G_rag.edges(data=True):
        src, dst, data = edge
        instances = data["instances"]
        if data["type"] == "request":
            arrow = FancyArrowPatch(
                (pos_rag[src][0], pos_rag[src][1]),
                (pos_rag[dst][0], pos_rag[dst][1]),
                arrowstyle="->",
                color="black",
                mutation_scale=15,
                label=f"R({instances})"
            )
            ax.add_patch(arrow)
            ax.text(
                (pos_rag[src][0] + pos_rag[dst][0]) / 2,
                (pos_rag[src][1] + pos_rag[dst][1]) / 2,
                f"R({instances})",
                fontsize=10,
                color="black"
            )
        else:
            arrow = FancyArrowPatch(
                (pos_rag[src][0], pos_rag[src][1]),
                (pos_rag[dst][0], pos_rag[dst][1]),
                arrowstyle="->",
                color="black",
                mutation_scale=15,
                label=f"H({instances})"
            )
            ax.add_patch(arrow)
            ax.text(
                (pos_rag[src][0] + pos_rag[dst][0]) / 2,
                (pos_rag[src][1] + pos_rag[dst][1]) / 2,
                f"H({instances})",
                fontsize=10,
                color="black"
            )

    ax.set_title("Resource Allocation Graph (Multi-Instance)")
    ax.axis("off")

    # Add legend
    plt.figtext(0.5, 0.95, "Legend", ha="center", fontsize=12, fontweight="bold")
    plt.figtext(0.5, 0.92, "Process  Resource  Held (H)  Request (R)", ha="center", fontsize=10)
    plt.figtext(0.5, 0.89, status, ha="center", fontsize=10, color=status_color)

    plt.tight_layout(rect=[0, 0, 1, 0.88])
    plt.show()
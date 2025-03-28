import matplotlib.pyplot as plt
import networkx as nx
from matplotlib.patches import Rectangle
from matplotlib.lines import Line2D

def compute_safe_sequence(processes, resources_held, resources_wanted):
    """
    Computes a safe execution sequence using a simplified Banker's Algorithm.
    
    Args:
        processes (list): List of process names (e.g., ['P1', 'P2', ...]).
        resources_held (dict): Mapping of processes to held resources.
        resources_wanted (dict): Mapping of processes to requested resources.
    
    Returns:
        list: A safe execution sequence, or None if no safe sequence exists.
    """
    held_resources = set()
    for proc in resources_held:
        held_resources.update(resources_held[proc])
    
    available = set([f"R{i+1}" for i in range(len(held_resources)) if f"R{i+1}" not in held_resources])
    finish = {proc: False for proc in processes}
    safe_sequence = []

    while len(safe_sequence) < len(processes):
        found = False
        for proc in processes:
            if not finish[proc]:
                can_run = True
                for res in resources_wanted[proc]:
                    if res not in available and res not in resources_held[proc]:
                        can_run = False
                        break
                if can_run:
                    safe_sequence.append(proc)
                    available.update(resources_held[proc])
                    finish[proc] = True
                    found = True
        if not found:
            return None
    return safe_sequence

def build_wait_for_graph(resources_held, resources_wanted):
    """
    Builds the Wait-For Graph (WFG) from the RAG.
    
    Args:
        resources_held (dict): Mapping of processes to held resources.
        resources_wanted (dict): Mapping of processes to requested resources.
    
    Returns:
        dict: Adjacency list representing the WFG.
    """
    wfg = {proc: [] for proc in resources_held}
    for p1 in resources_wanted:
        for res in resources_wanted[p1]:
            for p2 in resources_held:
                if res in resources_held[p2] and p1 != p2:
                    wfg[p1].append(p2)
    return wfg

def convert_deadlock_cycle_to_wfg(deadlock_cycle, resources_held, resources_wanted):
    """
    Converts a deadlock cycle from the RAG to a WFG cycle (processes only).
    
    Args:
        deadlock_cycle (list): The deadlock cycle from the RAG.
        resources_held (dict): Mapping of processes to held resources.
        resources_wanted (dict): Mapping of processes to requested resources.
    
    Returns:
        list: A deadlock cycle containing only process nodes.
    """
    if not deadlock_cycle:
        return None
    
    process_cycle = [node for node in deadlock_cycle if node.startswith("P")]
    wfg_cycle = []
    for i in range(len(process_cycle)):
        p1 = process_cycle[i]
        p2 = process_cycle[(i + 1) % len(process_cycle)]
        for res in resources_wanted[p1]:
            if res in resources_held[p2]:
                if p1 not in wfg_cycle:
                    wfg_cycle.append(p1)
                break
    
    if wfg_cycle:
        wfg_cycle.append(wfg_cycle[0])
    
    return wfg_cycle if len(wfg_cycle) > 1 else None

def visualize_rag(rag, resources_held, resources_wanted, deadlock_cycle=None):
    """
    Visualizes the Resource Allocation Graph (RAG) and Wait-For Graph (WFG) side by side.
    
    Args:
        rag (dict): The Resource Allocation Graph as an adjacency list.
        resources_held (dict): Mapping of processes to held resources.
        resources_wanted (dict): Mapping of processes to requested resources.
        deadlock_cycle (list, optional): List of nodes forming a deadlock cycle in the RAG.
    """
    # Create RAG
    G_rag = nx.DiGraph()
    for node in rag:
        G_rag.add_node(node)
        for neighbor in rag[node]:
            G_rag.add_edge(node, neighbor)

    # Build WFG
    wfg = build_wait_for_graph(resources_held, resources_wanted)
    G_wfg = nx.DiGraph()
    for node in wfg:
        G_wfg.add_node(node)
        for neighbor in wfg[node]:
            G_wfg.add_edge(node, neighbor)

    # Convert RAG deadlock cycle to WFG deadlock cycle (processes only)
    wfg_deadlock_cycle = convert_deadlock_cycle_to_wfg(deadlock_cycle, resources_held, resources_wanted)

    # Define node types for RAG
    processes = [n for n in G_rag.nodes if n.startswith("P")]
    resources = [n for n in G_rag.nodes if n.startswith("R")]

    # Create a figure with two subplots
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 6))

    # --- RAG (Left Subplot) ---
    # Use bipartite layout with increased separation to avoid arrow piercing
    pos_rag = nx.bipartite_layout(G_rag, processes, align='horizontal', scale=2.0, center=(0, 0))

    # Draw process nodes (circles) with thinner borders
    nx.draw_networkx_nodes(G_rag, pos_rag, nodelist=processes, node_shape='o', 
                           node_color='lightblue', node_size=600, 
                           edgecolors='black', linewidths=0.3, ax=ax1)  # Thinner borders

    # Draw resource nodes (rectangles with a dot)
    for resource in resources:
        x, y = pos_rag[resource]
        rect = Rectangle((x - 0.1, y - 0.1), 0.2, 0.2, 
                         facecolor='lightgreen', edgecolor='black', linewidth=0.3)  # Thinner borders
        ax1.add_patch(rect)
        ax1.plot(x, y, 'ko', markersize=6)

    # Draw edges for RAG with smaller arrowheads
    allocation_edges = [(u, v) for u, v in G_rag.edges if u.startswith("R") and v.startswith("P")]
    request_edges = [(u, v) for u, v in G_rag.edges if u.startswith("P") and v.startswith("R")]

    nx.draw_networkx_edges(G_rag, pos_rag, edgelist=allocation_edges, edge_color='black', 
                           width=1.5, arrows=True, arrowstyle='-|>', arrowsize=10, ax=ax1)  # Smaller arrows
    nx.draw_networkx_edges(G_rag, pos_rag, edgelist=request_edges, edge_color='black', 
                           width=1.5, arrows=True, arrowstyle='->', arrowsize=10, ax=ax1)

    # Draw labels outside nodes for RAG
    label_pos_rag = pos_rag.copy()
    for node in label_pos_rag:
        x, y = label_pos_rag[node]
        if node.startswith("P"):
            label_pos_rag[node] = (x - 0.15, y)  # Move process labels to the left
        else:
            label_pos_rag[node] = (x + 0.15, y)  # Move resource labels to the right
    nx.draw_networkx_labels(G_rag, label_pos_rag, font_size=12, font_weight='bold', ax=ax1)

    # Set title for RAG
    ax1.set_title("Resource Allocation Graph", fontsize=14, pad=15)
    ax1.axis('off')

    # --- WFG (Right Subplot) ---
    pos_wfg = nx.circular_layout(G_wfg, scale=1.0)

    # Draw process nodes for WFG with thinner borders
    if wfg_deadlock_cycle:
        deadlock_nodes = set(wfg_deadlock_cycle)
        nx.draw_networkx_nodes(G_wfg, pos_wfg, nodelist=[n for n in G_wfg.nodes if n not in deadlock_nodes], 
                               node_shape='o', node_color='lightblue', node_size=600, 
                               edgecolors='black', linewidths=0.3, ax=ax2)
        nx.draw_networkx_nodes(G_wfg, pos_wfg, nodelist=[n for n in deadlock_nodes], 
                               node_shape='o', node_color='salmon', node_size=600, 
                               edgecolors='black', linewidths=0.3, ax=ax2)
    else:
        nx.draw_networkx_nodes(G_wfg, pos_wfg, nodelist=list(G_wfg.nodes), node_shape='o', 
                               node_color='lightblue', node_size=600, 
                               edgecolors='black', linewidths=0.3, ax=ax2)

    # Draw edges for WFG with smaller arrowheads
    if wfg_deadlock_cycle:
        deadlock_edges = [(wfg_deadlock_cycle[i], wfg_deadlock_cycle[i + 1]) for i in range(len(wfg_deadlock_cycle) - 1)]
        non_deadlock_edges = [(u, v) for u, v in G_wfg.edges if (u, v) not in deadlock_edges]
        nx.draw_networkx_edges(G_wfg, pos_wfg, edgelist=non_deadlock_edges, edge_color='black', 
                               width=1.5, arrows=True, arrowstyle='->', arrowsize=10, ax=ax2)
        nx.draw_networkx_edges(G_wfg, pos_wfg, edgelist=deadlock_edges, edge_color='red', 
                               width=2, arrows=True, arrowstyle='->', arrowsize=10, ax=ax2)
    else:
        nx.draw_networkx_edges(G_wfg, pos_wfg, edgelist=list(G_wfg.edges), edge_color='black', 
                               width=1.5, arrows=True, arrowstyle='->', arrowsize=10, ax=ax2)

    # Draw labels outside nodes for WFG
    label_pos_wfg = pos_wfg.copy()
    for node in label_pos_wfg:
        x, y = label_pos_wfg[node]
        # Adjust label position based on node position to avoid overlap
        if x > 0:
            label_pos_wfg[node] = (x + 0.15, y)  # Right side
        else:
            label_pos_wfg[node] = (x - 0.15, y)  # Left side
    nx.draw_networkx_labels(G_wfg, label_pos_wfg, font_size=12, font_weight='bold', ax=ax2)

    # Set title for WFG
    ax2.set_title("Wait-For Graph", fontsize=14, pad=15)
    ax2.axis('off')

    # Custom legend
    legend_elements = [
        Line2D([0], [0], marker='o', color='w', label='Process', markerfacecolor='lightblue', markersize=10),
        Line2D([0], [0], marker='s', color='w', label='Resource', markerfacecolor='lightgreen', markersize=10),
        Line2D([0], [0], color='black', lw=1.5, label='Held (<-)'),
        Line2D([0], [0], color='black', lw=1.5, linestyle='solid', label='Request (->)/Wait-For'),
    ]
    if wfg_deadlock_cycle:
        legend_elements.append(Line2D([0], [0], color='red', lw=2, label='Deadlock Cycle'))
    fig.legend(handles=legend_elements, loc='upper center', bbox_to_anchor=(0.5, 0.98), 
               fontsize=10, title="Legend", title_fontsize=12, frameon=True, 
               edgecolor='black', framealpha=1, ncol=len(legend_elements))

    # Add text for deadlock or safe sequence
    if wfg_deadlock_cycle:
        cycle_text = "Deadlock Cycle: " + " -> ".join(wfg_deadlock_cycle)
        plt.figtext(0.5, 0.05, cycle_text, ha="center", fontsize=12, color='red', weight='bold', 
                    bbox=dict(facecolor='white', edgecolor='red', boxstyle='round,pad=0.5'))
    else:
        safe_sequence = compute_safe_sequence(processes, resources_held, resources_wanted)
        if safe_sequence:
            sequence_text = "Safe Execution Sequence: " + " -> ".join(safe_sequence)
            plt.figtext(0.5, 0.05, sequence_text, ha="center", fontsize=12, color='green', weight='bold', 
                        bbox=dict(facecolor='white', edgecolor='green', boxstyle='round,pad=0.5'))
        else:
            plt.figtext(0.5, 0.05, "No Safe Execution Sequence Found", ha="center", fontsize=12, color='orange', 
                        weight='bold', bbox=dict(facecolor='white', edgecolor='orange', boxstyle='round,pad=0.5'))

    # Adjust layout
    plt.tight_layout(rect=[0, 0.1, 1, 0.9])
    plt.show()

if __name__ == "__main__":
    # Example usage with no deadlock (to match the image)
    sample_rag_no_deadlock = {
        "P1": ["R1", "R2"],
        "P2": ["R3"],
        "P3": [],
        "P4": [],
        "R1": [],
        "R2": [],
        "R3": ["P1"],
        "R4": ["P1"],
    }
    sample_resources_held_no_deadlock = {
        "P1": ["R3", "R4"],
        "P2": [],
        "P3": [],
        "P4": [],
    }
    sample_resources_wanted_no_deadlock = {
        "P1": ["R1", "R2"],
        "P2": ["R3"],
        "P3": [],
        "P4": [],
    }
    visualize_rag(sample_rag_no_deadlock, sample_resources_held_no_deadlock, sample_resources_wanted_no_deadlock)

    # Example with deadlock
    sample_rag = {
        "P1": ["R1"],
        "R1": ["P2"],
        "P2": ["R2"],
        "R2": ["P1"],
        "P3": [],
        "R3": [],
    }
    sample_resources_held = {
        "P1": ["R2"],
        "P2": ["R1"],
        "P3": [],
    }
    sample_resources_wanted = {
        "P1": ["R1"],
        "P2": ["R2"],
        "P3": [],
    }
    sample_cycle = ["P1", "R1", "P2", "R2", "P1"]
    visualize_rag(sample_rag, sample_resources_held, sample_resources_wanted, sample_cycle)
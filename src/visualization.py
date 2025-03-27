import networkx as nx
import matplotlib.pyplot as plt

def visualize_rag(graph, cycle=None):
    """Visualizes the Resource Allocation Graph (RAG) and highlights any deadlock cycle.

    Args:
        graph (dict): The RAG as an adjacency list.
        cycle (list, optional): The list of nodes forming a deadlock cycle.
    """
    G = nx.DiGraph()
    # Add edges to the graph
    for node, neighbors in graph.items():
        for neighbor in neighbors:
            G.add_edge(node, neighbor)

    # Define node colors: processes in light blue, resources in light green
    node_colors = []
    for node in G.nodes():
        if node.startswith("P"):
            node_colors.append("lightblue")
        else:
            node_colors.append("lightgreen")

    # Layout and draw the graph
    pos = nx.spring_layout(G)
    plt.figure(figsize=(8, 6))
    nx.draw(G, pos, with_labels=True, node_color=node_colors, node_size=500, font_size=10, arrows=True)

    # Highlight the cycle if provided
    if cycle:
        cycle_edges = [(cycle[i], cycle[i+1]) for i in range(len(cycle)-1)]
        nx.draw_networkx_edges(G, pos, edgelist=cycle_edges, edge_color="red", width=2)

    plt.title("Resource Allocation Graph (Processes: Blue, Resources: Green)")
    plt.show()
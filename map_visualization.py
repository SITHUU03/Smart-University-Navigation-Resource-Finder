import matplotlib.pyplot as plt
import networkx as nx

def _as_networkx_graph(graph_like):
    """Convert various graph representations to a NetworkX Graph.
    Supports:
      - dict[str, list[tuple[str, weight]]]
      - dict[str, dict[str, weight]]
      - nx.Graph (returned as-is)
    """
    if isinstance(graph_like, nx.Graph):
        return graph_like

    G = nx.Graph()
    if isinstance(graph_like, dict):
        for node, neighbors in graph_like.items():
            # neighbors can be a dict or a list/tuple of pairs
            if isinstance(neighbors, dict):
                iterable = neighbors.items()
            else:
                iterable = neighbors  # expect list[ (nbr, dist), ... ]
            for entry in iterable:
                if isinstance(entry, tuple) and len(entry) >= 2:
                    nbr, dist = entry[0], entry[1]
                else:
                    # fallback if malformed
                    continue
                G.add_edge(node, nbr, weight=dist)
        return G
    raise TypeError("Unsupported graph representation: %r" % type(graph_like))

def draw_campus(graph, path=None):
    """Draw the campus map using a NetworkX graph.

    Args:
        graph: Graph structure of the campus (dict or nx.Graph).
        path (list[str]): Optional list of nodes representing the shortest path.
    """
    G = _as_networkx_graph(graph)

    # Layout for positioning
    pos = nx.spring_layout(G, seed=42)  # fixed seed = stable layout

    # Draw nodes + labels
    nx.draw_networkx_nodes(G, pos, node_color="lightblue", node_size=800)
    nx.draw_networkx_labels(G, pos, font_size=10, font_family="Arial")

    # Draw edges
    nx.draw_networkx_edges(G, pos, edge_color="gray")

    # Draw edge weights (distances)
    edge_labels = nx.get_edge_attributes(G, "weight")
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_size=8)

    # If a path was given, highlight it
    if path and len(path) > 1:
        path_edges = list(zip(path, path[1:]))
        nx.draw_networkx_edges(G, pos, edgelist=path_edges, edge_color="red", width=3)
        nx.draw_networkx_nodes(G, pos, nodelist=path, node_color="orange", node_size=900)

    # Show plot
    plt.title("Campus Map", fontsize=14)
    plt.axis("off")
    plt.show()
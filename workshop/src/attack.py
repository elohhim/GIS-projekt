import os
import random

import igraph


def generate_euclidean_graph(n, m, dcc=True, *, epsilon=0.01):
    """Generates euclidean graph of given number of vertices and edges.

    NOTE: Not very efficient and still not sure what euclidean graphs are.

    :param n: Number of vertices.
    :param m: Approximate number of edges.
    :param dcc: If returning only dominant connected component.
    :param epsilon: Tells how precise number of edges shpuld be.

    :return:Generated euclidean graph.
    """
    radius = 1/n
    while True:
        g = igraph.Graph.GRG(n, radius)
        deviation = (m-g.ecount())/m
        if abs(deviation) < epsilon:
            break
        else:
            radius += (1 if deviation > 0 else -1) / n
    return g.clusters().giant() if dcc else g


def generate_random_graph(n, m, dcc=True):
    """Generates random (ER) graph of given number of vertices and edges.

    :param n: Number of vertices.
    :param m: Number of edges.
    :param dcc: If returning only dominant connected component.

    :return: Generated random (ER) graph.
    """
    g = igraph.Graph.Erdos_Renyi(n, m=m, directed=False)
    return g.clusters().giant() if dcc else g


def connected(g):
    """Checks if graph is connected.

    :param g: Graph which will be checked.

    :return: True if graph is connected else False.
    """
    if g.ecount() == 0 or g.vcount() == 0:
        return False
    return g.is_connected()


def get_random_edge(g):
    """Gets random edge of a given graph.

    :param g: Given graph.

    :return: Random choosen edge of a graph.
    """
    return random.choice(g.es())


def attack(g):
    """Perform attack on given graph by removing one of the edges.

    :param g: Graph which will be attacked.
    :return: Graph after performing an attack.
    """
    if g.ecount() == 0 or g.vcount() == 0:
        raise ValueError("Can't perform attack on graph with 0 edges or "
                         "vertices.")
    edge = get_random_edge(g)
    return g - edge


def safe_path_return(path):
    """Returns path only if file exists in file system.

    :param path: Path to be returned.
    :raises FileNotFoundError: When file doesn't exist.
    """
    if os.path.exists(path):
        return path
    else:
        raise FileNotFoundError(f"File {path} doesn't exist.")


def graph2dot(g, filename, directory="graphs"):
    """Saves given graph in dot format.

    :param g: Graph to be saved.
    :param filename: File name.
    :param directory: Destination directory, default value 'graphs'.
    :return: Path to the saved file.
    """
    dot_ext = ".dot"
    dot_path = os.path.join(directory, filename+dot_ext)
    g.write_dot(dot_path)
    return safe_path_return(dot_path)


def dot2svg(dot_path):
    """Converts dot file into svg using dot command from graphviz package.

    :param dot_path:
    :return: Path to created svg file.
    """
    svg_ext = ".svg"
    prefix, _ = os.path.splitext(dot_path)
    svg_path = prefix + svg_ext
    os.system(f"dot {dot_path} -Tsvg > {svg_path}")
    return safe_path_return(svg_path)


def show_svg(svg_path):
    """Shows svg file if in Jupyter environment.

    :param svg_path: Path to file which will be shown in notebook.
    """
    try:
        from IPython.display import SVG, display
        display(SVG(svg_path))
    except ImportError:
        print("Could not render SVG graphs outside Jupyter notebook.")


def preview_graph(g, name):
    """Preview graph in Jupyter notebook.

    :param g: Graph to be previewed.
    :param name: Svg filename to be used.
    """
    show_svg(dot2svg(graph2dot(g, name)))


def success_new_cluster(old_g, new_g):
    return len(new_g.clusters()) > len(old_g.clusters())


def success_connected(old_g, new_g):
    return not connected(new_g)


def process(n, m, k, graph_type='random', dcc=True, show=False,
            strategy='connected', **kwargs):
    """Process the experiment.

    :param n: Number of graph vertices.
    :param m: Number of graph edges.
    :param k: Number of tries.
    :param graph_type: Type of graph, might be 'euclidean' or 'random', defaults
        to 'random'.
    :param dcc: Flag telling if dominant connected component only should be used.
    :param show: Flag telling if generated graphs should be showed (only for
        Jupyter notebook).
    :param strategy: Success strategy to be used, defaults to 'connected'.

    :return: None
    """
    success_strategies = {'connected': success_connected,
                          'new_cluster': success_new_cluster}
    graph_generators = {'euclidean': generate_euclidean_graph,
                        'random': generate_random_graph}
    tries = k
    successes = 0
    for k in range(tries):
        g = graph_generators[graph_type](n, m, dcc, **kwargs)
        if show:
            preview_graph(g, "original")
        attacked_g = attack(g)
        if show:
            preview_graph(attacked_g, f"attack")
        if success_strategies[strategy](g, attacked_g):
            successes += 1
        if k % int(tries/10) == 0:
            print(f"{k} attacks done.")
    print(f"Successes: {successes}. Break probability {successes/tries}.")


if __name__ == '__main__':
    process()

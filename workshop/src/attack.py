import os
import random
from collections import namedtuple

import igraph
import math


class GISError(ValueError):
    pass


def generate_euclidean_graph(n, m):
    """Generates euclidean graph of given number of vertices and number of
    edges approximate to given one.

    Uses formula for expected value of number of edges for euclidean graph:

    Em = πξ^2 * n(n-1)/2

    Where:
        Em - expected value for number of edges
        ξ - euclidean graph radius
        n - number of vertices

    :param n: Expected value for number of vertices.
    :param m: Expected value for number of edges.

    :return: Generated euclidean graph.
    """
    radius = (2 * m / (math.pi * n * (n - 1))) ** 0.5
    g = igraph.Graph.GRG(n, radius)
    return g.clusters().giant()


def generate_random_graph(n, m):
    """Generates random (ER) graph of given number of vertices and edges.

    :param n: Number of vertices.
    :param m: Number of edges.

    :return: Generated random (ER) graph.
    """
    ksi = 2*m / (n*(n-1))
    if ksi < 1/n:
        raise GISError(f"Can't generate connected random ER graph ξ={ksi} "
                         f"is lower than 1/n={1/n}.")
    g = igraph.Graph.Erdos_Renyi(n, m=m, directed=False)
    return g.clusters().giant()


def graph_factory(graph_type, n, m, epsilon):
    """ Creates graph based on given attributes.

    :param graph_type: Type of graphs in population: "random" or "euclidean".
    :param n: Expected value for generated graph number of vertices.
    :param m: Expected value for number of edges of graph.
    :param epsilon: Tells how close to expected values the number of vertices
        and edges should be.
    :return: Generated graph.
    """
    max_tries = 100
    factory_methods = {
        "random": generate_random_graph,
        "euclidean": generate_euclidean_graph
    }
    for _ in range(max_tries):
        g = factory_methods[graph_type](n, m)
        deviations = (n - g.vcount()) / n, (m - g.ecount()) / m
        if max(map(abs, deviations)) < epsilon:
            break
    else:
        raise GISError(
            f"Failed after {max_tries} tries when generating"
            f"graph:\n"
            f"- type: {graph_type}\n"
            f"- vertices: {n}\n"
            f"- edges: {m}\n"
            f"Interrupting processing, please reconsider if it is possible to "
            f"create such connected graph within given epsilon boundaries " 
            f"({epsilon}).")
    return g


def generate_graph_population(population_size, graph_type, n, m,
                              epsilon=0.1):
    """ Creates population of graphs with given attributes.

    :param population_size: Size of population to be generated.
    :param graph_type: Type of graphs in population: "random" or "euclidean".
    :param n: Size of generated graphs in population.
    :param m: Expected value for number of edges of graphs in
        population.
    :param epsilon: Tells how close to expected value the number of vertices
        and edges should be.
    :return: Generated population of graphs as a list.
    """
    try:
        return [graph_factory(graph_type, n, m, epsilon)
                for _ in range(population_size)]
    except GISError as e:
        raise GISError(f"Problem when generating graph population: {e}")


def get_random_edge(g):
    """Gets random edge of a given graph.

    :param g: Given graph.

    :return: Random choosen edge of a graph.
    """
    return random.choice(g.es())


def attack_random(g):
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

    :return: Number of successful attacks.
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
        attacked_g = attack_random(g)
        if show:
            preview_graph(attacked_g, f"attack")
        if success_strategies[strategy](g, attacked_g):
            successes += 1
        if k % int(tries/10) == 0:
            print(f"{k} attacks done.")
    print(f"Successes: {successes}. Break probability {successes/tries}.")
    return successes


def perform_attack_old(g, multiplicity):
    """Performs attack of given multiplicity on a graph.

    :param g: Attacked graph.
    :param multiplicity: Quantity of edges that are removed during attack.
    :return: Graphs after attack.
    """
    for _ in range(multiplicity):
        g = attack_random(g)
    return g


def perform_attack(g, multiplicity):
    """Performs attack of given multiplicity on a graph.

    New impl (roughly 100 times faster) makes usage of igraph native methods.

    :param g: Attacked graph.
    :param multiplicity: Quantity of edges that are removed during attack.
    :return: Graphs after attack.
    """
    result = g.copy()
    result.delete_edges(random.sample(list(g.es), k=multiplicity))
    return result


AnalysisResult = namedtuple("AnalysisResult", "tries successes failures")


def analyse_attack(g, tries, multiplicity, failure_threshold=None):
    """Performs analysis of random attacks on given graph.

    :param g: Analysed graph.
    :param tries: Number of random attack tries to be performed.
    :param multiplicity: Quantity of edges that are removed during attack.
    :param failure_threshold: Tells after how many failed attack attempts
        analysis should be forfeited. If None all tries are performed despite
        failures. Defaults to None.
    :return: AnalysisResult type tuple.
    """
    failures = 0
    successes = 0
    for i in range(tries):
        attacked_g = perform_attack(g, multiplicity)
        if attacked_g.is_connected():
            failures += 1
        else:
            successes += 1
        if failure_threshold is not None and failures == failure_threshold:
            break
    return AnalysisResult(i+1, successes, failures)


if __name__ == '__main__':
    pass

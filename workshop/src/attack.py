import random
import math
from collections import namedtuple
from itertools import zip_longest

import igraph
import numpy as np
import matplotlib.pyplot as plt


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
    g = igraph.Graph.GRG(n, radius, torus=True)
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
    if epsilon is None:
        return factory_methods[graph_type](n, m)
    for _ in range(max_tries):
        g = factory_methods[graph_type](n, m)
        deviations = (n - g.vcount()) / n, (m - g.ecount()) / m
        if max(map(abs, deviations)) < epsilon:
            break
    else:
        raise GISError(
            f"Failed after {max_tries} tries when generating "
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
        #raise GISError(f"Problem when generating graph population: {e}")
        print(f"Problem when generating graph population: {e}")
        return []


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


AttackResult = namedtuple("AttackResult", "tries successes failures probability")


def analyse_graph_attack(g, tries, multiplicity, failure_threshold=None):
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
        eff_multiplicity = min(multiplicity, g.ecount())
        attacked_g = perform_attack(g, eff_multiplicity)
        if attacked_g.is_connected():
            failures += 1
        else:
            successes += 1
        if failure_threshold is not None and failures == failure_threshold:
            break
    tries_performed = i+1
    return AttackResult(tries_performed, successes, failures,
                        successes/tries_performed)


PopulationParameters = namedtuple("PopulationParameters",
                                  "size graph_type n m")

PopulationParametersTest = namedtuple("PopulationParametersTest",
                                      "size graph_type n m epsilon")

AttackParameters = namedtuple("AttackParameters",
                              "tries multiplicity failure_threshold")


PopulationAttackResult = namedtuple("PopulationAttackResult",
                                    "attack_parameters mean results")


def analyse_population_attack(population, attack_parameters):
    """Performs series of attack analysis on each graph from given
    population.

    :param population:
    :param attack_parameters:
    :return:
    """
    results = [analyse_graph_attack(g, *attack_parameters)
               for g in population]
    mean_result = AttackResult(*tuple(np.mean(results, axis=0)))
    return PopulationAttackResult(attack_parameters, mean_result, results)


def plot_results(pparams, results):
    """Plots population analysis results into file.
    """
    fig = plt.figure()
    ax = fig.add_subplot(111)
    x = [r.attack_parameters.multiplicity for r in results]
    y = [r.mean.probability for r in results]
    plt.plot(x, y, '--ro')
    axes = plt.gca()
    axes.set_xlim([0, pparams.m])
    axes.set_ylim([0, 1.1])
    plt.grid(True)
    gtype = {
        "random": "losowych ER",
        "euclidean": "euklidesowych"
    }
    plt.title(f"Analiza ataków na populację {pparams.size} grafów "
              f"{gtype[pparams.graph_type]} o:\n"
              f" {pparams.n} wierzchołkach i {pparams.m} krawędziach")
    plt.xlabel("Liczba atakowanych krawędzi")
    plt.ylabel("Prawdopodobienstwo powodzenia ataku")
    file_name = f"N{pparams.n}_M{pparams.m}_{pparams.graph_type}"
    plt.savefig(f"plots/{file_name}.png", dpi=300)


def plot_results2(pp1, pp2, results1, results2, layout="horizontal"):
    """Plots population comparision analysis results into file.
    """
    layout_spec = {
        "horizontal": (1, 2),
        "vertical": (2, 1)
    }[layout]
    figsize = {
        "horizontal": (16, 6),
        "vertical": (8, 12)
    }[layout]

    fig = plt.figure(figsize=figsize)

    # Plotting results on one subplot
    ax1 = fig.add_subplot(*layout_spec, 1)
    ax1.set_yscale('log')

    def add_plot(results, pp, style, label_prefix):
        labels = {
            "random": "grafy ER",
            "euclidean": "grafy euklidesowe"
        }
        x = [r.attack_parameters.multiplicity for r in results]
        y = [r.mean.probability for r in results]
        plt.plot(x, y, style, label=f"{label_prefix} - {labels[pp.graph_type]}")

    add_plot(results1, pp1, '--ro', "P1")
    add_plot(results2, pp2, '--bs', "P2")
    axes = plt.gca()
    axes.set_xlim([0, max(pp1.m, pp2.m)])
    axes.set_ylim([1e-3, 1.1])
    plt.xlabel("Liczba atakowanych krawędzi")
    plt.ylabel("Prawdopodobienstwo powodzenia ataku")
    plt.grid(True, which="both")
    ax1.legend()
    # Plotting difference on second subplot
    ax2 = fig.add_subplot(*layout_spec, 2)
    x = [r.attack_parameters.multiplicity
         for r in max(results1, results2, key=len)]
    pairs = zip_longest((r.mean.probability for r in results1),
                        (r.mean.probability for r in results2), fillvalue=1.0)
    dy = [r1 - r2 for r1, r2 in pairs]
    plt.plot(x, dy, '--gd', label="P1 - P2")
    plt.xlabel("Liczba atakowanych krawędzi")
    plt.ylabel("Różnica prawdopodobienstw powodzenia ataku")
    plt.grid(True)
    plt.axhline(0, color='black')
    ax2.legend()
    gtype = {
        "random": "losowych ER",
        "euclidean": "euklidesowych"
    }

    title = (f"Analiza porównawcza ataków na populacje:\n"
             f" - {pp1.size} grafów {gtype[pp1.graph_type]} o "
             f"{pp1.n} wierzchołkach i {pp1.m} krawędziach\n"
             f" - {pp2.size} grafów {gtype[pp2.graph_type]} o "
             f"{pp2.n} wierzchołkach i {pp2.m} krawędziach")
    plt.suptitle(title)
    file_name = "_".join([f"N{pp1.n}", "M{pp1.m}", pp1.graph_type, "vs",
                         pp2.graph_type, layout])
    plt.savefig(f"plots/{file_name}.png", dpi=300)


POPULATION_SIZE = 10

ATTACK_TRIES = 10

FAILURE_THRESHOLD = ATTACK_TRIES/10

test_data_sets = [
        PopulationParameters(POPULATION_SIZE, "random", 2, 1),
        PopulationParameters(POPULATION_SIZE, "random", 3, 2),
        PopulationParameters(POPULATION_SIZE, "random", 3, 3),
        PopulationParameters(POPULATION_SIZE, "random", 4, 3),
        PopulationParameters(POPULATION_SIZE, "random", 4, 4),
        PopulationParameters(POPULATION_SIZE, "random", 4, 5),
    ]

data_sets_10 = [
    PopulationParameters(POPULATION_SIZE, "random", 10, 20),
    PopulationParameters(POPULATION_SIZE, "euclidean", 10, 20),
    PopulationParameters(POPULATION_SIZE, "random", 10, 30),
    PopulationParameters(POPULATION_SIZE, "euclidean", 10, 30),
    PopulationParameters(POPULATION_SIZE, "random", 10, 40),
    PopulationParameters(POPULATION_SIZE, "euclidean", 10, 40),
]

data_sets_100 = [
    PopulationParameters(POPULATION_SIZE, "random", 100, 200),
    PopulationParameters(POPULATION_SIZE, "euclidean", 100, 200),
    PopulationParameters(POPULATION_SIZE, "random", 100, 800),
    PopulationParameters(POPULATION_SIZE, "euclidean", 100, 800),
    PopulationParameters(POPULATION_SIZE, "random", 100, 1600),
    PopulationParameters(POPULATION_SIZE, "euclidean", 100, 1600),
]

data_sets_1000 = [
    PopulationParameters(POPULATION_SIZE, "random", 1000, 4000),
    PopulationParameters(POPULATION_SIZE, "euclidean", 1000, 4000),
    PopulationParameters(POPULATION_SIZE, "random", 1000, 8000),
    PopulationParameters(POPULATION_SIZE, "euclidean", 1000, 8000),
    PopulationParameters(POPULATION_SIZE, "random", 1000, 16000),
    PopulationParameters(POPULATION_SIZE, "euclidean", 1000, 16000),
]

data_sets_4000 = [
    PopulationParameters(POPULATION_SIZE, "random", 4000, 40000),
    PopulationParameters(POPULATION_SIZE, "euclidean", 4000, 40000)
]

all_data_sets = data_sets_10 + data_sets_100 + data_sets_1000


def process_data_set(pparam, truncate):
    """Process attack analysis over defined population.

    :param pparam: Population definition.
    :param truncate: If analysis should stop when probability reaches 1.
    :return: Analysis results.
    """
    population = generate_graph_population(*pparam)
    results = []
    for i in range(20):
        attack_parameters = AttackParameters(ATTACK_TRIES,
                                             int(1 + i * (pparam.m / 20)),
                                             FAILURE_THRESHOLD)
        result = analyse_population_attack(population, attack_parameters)
        results.append(result)
        print(f"## Analysis results:\n"
              f"# Params: {result.attack_parameters}\n"
              f"# Mean: {result.mean}")
        if truncate and math.isclose(result.mean.probability, 1.0,
                                     abs_tol=0.01):
            break
    plot_results(pparam, results)
    return results


def process(data_sets=all_data_sets, is_test=False, truncate=False):
    """Performs experiment by performing series of attack analysis over
    graph populations defined in data sets.

    :param data_sets: List of experiment run definitions.
    :param is_test: Defaults False.
    :param truncate: See process_data_set truncate param.
    :return:
    """
    for pparam in data_sets:
        print(f"### Analysing graph population defined by: {pparam}")
        if is_test:
            pparam = PopulationParametersTest(*pparam, None)
        process_data_set(pparam, truncate)
    return None


def process_pairs(data_sets=all_data_sets):
    """ Performs experiment by performing series of attack analysis over
    graph populations defined in data sets.

    :param data_sets: List of experiment run definitions.
    :param is_test: Defaults False.
    :param truncate: If analysis should stop when probability reaches 1.
    """
    it = iter(data_sets)
    pairs = zip(it, it)
    print(pairs)
    for data_set1, data_set2 in pairs:
        print(f"### Comapring graph populations defined by:\n"
              f"\t- {data_set1}\n"
              f"\t- {data_set2}")
        results1 = process_data_set(data_set1, True)
        results2 = process_data_set(data_set2, True)
        plot_results2(data_set1, data_set2, results1, results2, "horizontal")
        plot_results2(data_set1, data_set2, results1, results2, "vertical")



def test():
    process(test_data_sets, True)


if __name__ == '__main__':
    process()

#!/usr/bin/env python2

def generate_random_gt():

    import graph_tool

    graph_tool.generation.random_rewire(g, model=erdos)

def generate_random_jgraph():

    from jgraph import *

    g = jgraph.Graph()
    g.add_vertices(4)
    g.add_edges([(0,2),(1,2),(3,2)])

    print g.betweenness()

    g = Graph.Erdos_Renyi(n=10000, m=100000)

def sample_k(max):

    accept = False
    while not accept:
        k = np.random.randint(1,max+1)
        accept = np.random.random() < 1.0/k
    return k

import gt

g = gt.random_graph(1000, lambda: sample_k(40), model="probabilistic-configuration",
                    edge_probs=lambda i, k: 1.0 / (1 + abs(i - k)), directed=False,
                    n_iter=100)

gt.graph_draw(g, vertex_fill_color=bm, edge_color="black", output="blockmodel.pdf")

generate_random_gt()

# -*- coding: utf-8 -*-

from __future__ import division
import os, igraph, random, distutils, math
from IPython.display import SVG, display

class experiment:
    """Class integrating methods for graph-based experiments"""

    def graph(self, vertex_count):
        
        g = igraph.Graph()

        g.add_vertices(vertex_count)
 
        return g

    def test_graph(self):

        g = graph(10)

        g.name = "simple"

        print(g)

        print g.name

    def random_vertex_number(self, g):
 
        vertices = g.vcount()
 
        return random.randrange(vertices)

    def test_random_vertex_number(self, g):

        print(random_vertex_number(g))

    def random_vertex_pair(self, g):
 
        pair = []
 
        vertex = random_vertex_number(g)
        
        pair.append(vertex)
        
        another_vertex = random_vertex_number(g)
        
        while another_vertex == pair[0]:
            another_vertex = random_vertex_number(g)

        pair.append(another_vertex)

        return pair

    def test_random_vertex_pair(self, g):

        for i in range(1):
        
            pair = random_vertex_pair(g)

        print(pair)

    def add_random_edges(self, g, edge_count):
        
        edges = []
        
        for i in range(0, edge_count):
            
            vertex_pair = random_vertex_pair(g)
            
            if not g.are_connected(vertex_pair[0], vertex_pair[1]):

                edges.append(vertex_pair)

                g.add_edges(edges)
                
                edges.remove(vertex_pair)
        
        return g

    def test_add_random_edges(self, g, edge_count):

        g = add_random_edges(g, edge_count)

        print g.name
        print(g)

    def density(self, g):
        
        return g.density(loops = False)

    def test_density(self, g):

        print(density(g))

    def calculate_density(self, n, position):
        """Compute the minimal, average or maximal edge density
        achievable with the given number of vertices.

        Example:
        >>> calculate_density(10, "max")
        1.0
        """

        if position == "min":
            result = self.min_edges_sure(n) / self.max_edges(n)
            return result

        elif position == "max":
            result = 1
            return result

        elif position == "avg":
            result = 0.5 * (self.calculate_density(n, "min") + \
                         self.calculate_density(n, "max"))
            return result

    def max_edges(self, n):
        return 0.5 * n * (n - 1)

    def min_edges(self, n):
        return (n - 1)

    def min_edges_sure(self, n):
        """Apply the rule shown by Daniel Poole from Ohio State University
        to calculate the minimal number of edges to ensure connectedness
        of the graph.
          - math.stackexchange.com/q/1036775
        """
        return round(n / 2, 0)

    def generate_graph_preview(self, g):
       
        # name = g.name
        name = "preview"
     
        directory = "graphs/"
        
        file_name = directory + name
        
        dot_ext = ".dot"
        svg_ext = ".svg"
        
        g.write_dot(file_name + ".dot")

        #igraph.write(g, file_name + dot_ext)
        
        cmd = "dot " + file_name + dot_ext + " -Tsvg > " + file_name + svg_ext 

        #print cmd
        
        os.system(cmd)

    def preview_graph(self, g):

        name = "preview"
        
        directory = "graphs/"
        
        file_name = directory + name + ".svg"
        
        display(SVG(file_name))
        
        os.system("rm " + file_name)

    def show(self, g):

        self.generate_graph_preview(g)
        
        self.preview_graph(g)

    def dominant_component(self, g):
        
    #    name_safe = g.name
        
        connected_components = g.clusters()
        
        dominant_component = connected_components.giant()
        
    #    dominant_component.name = name_safe
        
        return dominant_component

    def connected(self, g):

        if g.ecount() == 0 or g.vcount() == 0:
            return False
        
        return g.is_connected()

    def test_connected(self, g):

        g = self.dominant_component(g)

        print("Is g connected?", self.connected(g))

        show(g)

    def random_edge(self, g):

        # print(g.ecount())
        
        edge = random.choice(g.es())
        
        #vertex_tuple = edge.tuple

        return edge

    def test_random_edge(self, g):

        print random_edge(g).tuple

    def breaks_upon_attack(self, g):
        
        edge = self.random_edge(g)
        
        safe_name = g.name
        
        g = g - edge
        
        g.name = safe_name
        
        broken = not self.connected(g)
        
        return [broken, g, edge]

    def test_breaks_upon_attack(self, g):

        [broken, g, edge] = breaks_upon_attack(g)

        print broken

        print g

        print g.name

        print "Affected edge:", edge.tuple

        # Preview graph after attack:
        show(g)

    def expected_density(self, n, m):
        """Calculate using a formula."""

        density = (2 * m) / (n * (n - 1))

        #print "Expected density computed:", round(density, 5)

        return density

    def expected_vertex_count(n, density):
        """Calculate using a formula."""

        result = 0.5 * density * n * (n - 1)

        return result

    # Generate a random geometric (Euclidean) graph with
    # n vertices and approximately m edges.
    def euclidean_net(self, n, m = None, density = None):
        
        g = igraph.Graph()

        if density == None:
            graph_density = self.expected_density(n, m)
        elif m == None:
            graph_density = density
            m = n * density
        
        radius = math.sqrt(graph_density / (math.pi * n))

        #print "Radius:", round(radius, 5)
        
        #graph_density = 0
        
        while g.ecount() < m:

            g_old = g
            
            g = igraph.Graph().GRG(n, radius)
            
            g.name = "Euclidean"

            g = self.dominant_component(g)

    #         graph_density = density(g)
            
            radius = radius + 0.02

    #            print "Stepping towards a greater radius. Edges currently:", g.ecount()

        difference_old = m - g_old.ecount()
        difference_new = g.ecount() - m

        if difference_old < difference_new:
            g = g_old

        return g

    def inspect(self, g):
        
    #        print "=== Graph type:", g.name, "==="

        print "=== Graph"

        print "Density:", round(self.density(g), 5)

        print "Vertices:", g.vcount()
        
        print "Edges:", g.ecount()

    def test_generate_euclidean_net(self, ):

        g = euclidean_net(80, 20)

        inspect(g)

    # Generate a random graph with
    # n vertices and m edges.

    # WARNING/TODO: Freezes "randomly" from time to time
    def random_net_DEPRECATED(self, n, m):
        
        g = graph(vertex_count = n)
        
        g = add_random_edges(g, edge_count = m)
        
        g.name = "random"
        
        g = self.dominant_component(g)
        
        while g.vcount() < n or g.ecount() < m:
            
            g.add_vertices(n - g.vcount())

            g = add_random_edges(g, edge_count = m - g.ecount())
            
            g = self.dominant_component(g)
        
        return g

    def random_net(self, n, m=None, p=None):
        """Generate a random network consisting of one cluster"""

        if p == None:
            g = igraph.Graph.Erdos_Renyi(n, m=m)
        elif m == None:
            g = igraph.Graph.Erdos_Renyi(n, p)
        else:
            print("Error: only one of (p, m) can be supplied at once.")
            exit()

        g = self.dominant_component(g)

        return g

    def test_random_net(self):

        # import cProfile
        # cProfile.run('g = random_net(19, 3)')

        g = random_net(7, 7)

        inspect(g)

        show(g)

    # How many random attacks did it
    # take to break the net?
    def random_connectivity_degree(self, g):
        
        degree = 0
        edge = None
        
        while g.ecount() > 0 and g.vcount() > 0 and self.connected(g):

            edge = self.random_edge(g)
        
            #safe_name = g.name

            g.delete_edges(edge)

            #g.name = safe_name
            
            degree = degree + 1

    #     return [broken, g, edge]

            if g.ecount() <= 0:
                #print "g has 0 edges"
                return degree

    #            if not self.connected(g):
    #                print "g disconnected"

        return degree

    def test_random_connectifity_degree(self, g):

        print random_connectivity_degree(g)

    # Run a campaign of net creation and attacking
    # until discontinuity.

    def compare_resiliences(self, n, m):

        g = random_net(n, m)

        #inspect(g)

        rcd = random_connectivity_degree(g)

        print "Resilience factor:", rcd
        
        show(g)

    #     g_prime = euclidean_net(n, m)

    #     inspect(g_prime)

    #     print "Resilience factor:", random_connectivity_degree(g_prime)

    def test_compare_resiliences(self):

        # import cProfile

        # report = cProfile.run('compare_resiliences(6, 5)')

        compare_resiliences(6, 5)

    def probe(self, n, m = None, density = None, type="random"):
        """Generate a random graph and return its experimental edge-consistency.

        Arguments:
        n -- vertex count,
        m -- edge count.
        """

        if type == "random" and m == None:
            g = self.random_net(n, p = density)
        elif type == "random" and m != None:
            g = self.random_net(n, m)
        elif type == "geometric" and m == None:
            g = self.euclidean_net(n, density=density)
        else:
            g = self.euclidean_net(n, m)

        #self.inspect(g)

        (vertices, edges) = (g.vcount(), g.ecount())

        rcd_g = self.random_connectivity_degree(g)

        #print "Attacks resisted:", rcd_g, ", last removed edge:", edge_1.tuple

        return self.density(g), rcd_g #, (vertices, edges), g.vcount()

    def probe_euclidean(self, n, m):

        g = self.euclidean_net(n, m)
        #self.inspect(g)

        rcd_g, edge_1 = self.random_connectivity_degree(g)

        #print "Attacks resisted:", rcd_g, ", last removed edge:", edge_1.tuple

        return g

    def plot_xy(self, data, n):
        """Plot graph edge-connectivity versus its edge density.
        
        Example:
          >>> data = [result1, result2, result3]
          >>> plot_xy(data)
        """
        
        import pandas as pd

        x = 'averaged density'
        y = 'averaged edge-connectivity'

        df = pd.DataFrame(data, columns = [x, y])
        df.set_index(x, inplace=True)
        t = "Mean resilience of graphs of " + str(n) + " nodes"
        #t = "Średni stopień spójności krawędziowej grafu o " + str(n) + " wierzchołkach"
        df.plot(title = t)

        return df

    def plot_save(self, data, n, file_name=""):
        """Plot graph edge-connectivity versus its edge density.
        
        Example:
          >>> data = [result1, result2, result3]
          >>> plot_xy(data)
        """
        
        import pandas as pd

        import matplotlib.pyplot as plt
        import numpy as np

        x = 'averaged density'
        y = 'averaged edge-connectivity'

        df = pd.DataFrame(data, columns = [x, y])
        df.set_index(x, inplace=True)
        t = "Mean resilience of graphs of " + str(n) + " nodes"
        #t = "Średni stopień spójności krawędziowej grafu o " + str(n) + " wierzchołkach"
        df.plot(title = t)

        if file_name != "":
            plt.savefig(file_name)

        return df

    def worker(self, n, d, position):
        """Accepts thread-separated jobs."""
        
        name = multiprocessing.current_process().name
    #     print name, 'Starting'
        result = e.probe(n, density = d, type=position)
    #     print name, 'Exiting'

        return result

    def scheduler(self, n, d, position):
        """Utilize multiprocessing for more efficient time usage

        Instructions:
          - https://stackoverflow.com/questions/19086106
        """

        jobs = []
        for i in range(5):
            p = multiprocessing.Process(target=worker, args=(n, d, position))
            jobs.append(p)
            p.start()

# import multiprocessing as mp

# def init_worker(mps, fps, cut):
#     global memorizedPaths, filepaths, cutoff
#     global DG

#     print "process initializing", mp.current_process()
#     memorizedPaths, filepaths, cutoff = mps, fps, cut
#     DG = 1##nx.read_gml("KeggComplete.gml", relabel = True)

# def work(item):
#     _all_simple_paths_graph(DG, cutoff, item, memorizedPaths, filepaths)

# def _all_simple_paths_graph(DG, cutoff, item, memorizedPaths, filepaths):
#     pass # print "doing " + str(item)

# def main():
#     m = mp.Manager()
#     memorizedPaths = m.dict()
#     filepaths = m.dict()
#     cutoff = 1 ##
#     # use all available CPUs
#     p = mp.Pool(initializer=init_worker, initargs=(memorizedPaths,
#                                                    filepaths,
#                                                    cutoff))
#     degreelist = range(10 ** 5) ##
#     for _ in p.imap_unordered(work, degreelist, chunksize=500):
#         pass
#     p.close()
#     p.join()

# if __name__ == "__main__":
    
#     main()

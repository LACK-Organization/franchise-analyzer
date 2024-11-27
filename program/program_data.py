"""CSC111 Project 2: CALK's Franchise Analyzer

This module contains the main classes for Franchise Analyzer including _WeightedVertex, WeightedGraph,
and GraphGenerator. This classes are meant to be imported and used in main.py and in other modules that contribute to
main.py.

Created by Leandro Hamaguchi, Aryan Nair, Carlos Solares, and Karan Singh. (CALK)

Copyright and Usage Information
===============================

This program is created solely for the personal and private use of CALK's members (Leandro Hamaguchi, Aryan Nair,
Carlos Solares, and Karan Singh). All forms of distribution of this code, whether as given or with any changes,
are expressly prohibited. For more information on copyright send a message to one of the following emails:
 - l.brasil@mail.utoronto.ca
 - aryan.nair@mail.utoronto.ca
 - carlos.solares@mail.utoronto.ca
 - kar.singh@mail.utoronto.ca

This file is Copyright (c) CALK Team
"""
from __future__ import annotations
import csv
from typing import Any, Union


class _WeightedVertex:
    """A vertex in a graph.

    Instance Attributes:
        - item: The name of this vertex.
        - vertex_data: The numerical data represnting factors of this vertex. Example: Reviews for vertice of
                       OtherRestauarnts type.
        - neighbours: A dictionary mapping the vertices that are adjacent to this vertex to a list with the first item
                      as the real life distance from one vertex to the other and the second item as the actual graph
                      weight of the edge.
        - cluster: An integer representing the cluster the vertex is a part of. A cluster value of 0 means that the
                   vertex is not part of any cluster.
        - coordinates: The coordinates of the vertex.
        - vertex_type: The type of the vertex

    Representation Invariants:
        - self not in self.neighbours
        - all(self in u.neighbours for u in self.neighbours)
        - self.vertex_type in {'MCD', 'OtherRestaurant', 'Landmark', 'IntersectionMain', 'IntersectionSmall', 'TTC'}
    """
    item: str
    vertex_data: dict[str, float]
    neighbours: dict[_WeightedVertex, list[Union[int, float]]]
    cluster: int
    coordinates: tuple[float, float]
    vertex_type: str

    def __init__(self, item: str, vertex_data: dict, neighbours: dict[_WeightedVertex, list[Union[int, float]]],
                 cluster: int, coordinates: tuple[float, float], vertex_type: str) -> None:
        """Initialize a new vertex with the given item and neighbours."""
        self.item = item
        self.vertex_data = vertex_data
        self.neighbours = neighbours
        self.cluster = cluster
        self.coordinates = coordinates
        self.vertex_type = vertex_type

    def best_weighted_path(self, vertex2: str, visited: set[_WeightedVertex])\
            -> list[Union[float, list[_WeightedVertex]]]:
        """Calculate the best weighted score between any two points on the graph based on the weighted edges.
        We calculate the full weight of each edge as distance * (1 - weight). Then to find the weighted score between
        two vertices, we find the least sum of all edges between the two vertices.

        NEW IMPLEMENTATION: Returns a list of two elements: the score, and a list of the vertices in the chosen path.

        Preconditions:
         - self and vertex2 are connected or self.item == vertex2.item
        """
        score = 0
        visited.add(self)
        path = [self]
        all_neighbours = {}
        if self == vertex2:
            return [score, path]
        else:
            for u in self.neighbours:
                if u not in visited:
                    if u.cluster != self.cluster:
                        score += self.neighbours[u][0] * (1 - self.neighbours[u][1])
                    else:
                        score += 1 - self.neighbours[u][1]
                    best_score = u.best_weighted_path(vertex2, visited)
                    score += best_score[0]
                    path += best_score[1]
                    all_neighbours[score] = path
# R1702 (too-many-nested-blocks) error ignored due to recursive nature of function
            if all_neighbours == {}:
                return [score, path]
            else:
                min_path_score = min(all_neighbours)
                path = all_neighbours[min(all_neighbours)]

                return [min_path_score, path]


class WeightedGraph:
    """A graph.

    Representation Invariants:
        - all(item == self._vertices[item].item for item in self._vertices)
        - all(isinstance(self._vertices[item], list) for item in self._vertices if isinstance(item, int))
        - all(isinstance(self._vertices[item], _WeightedVertex) for item in self._vertices if isinstance(item, str))

    Private Instance Attributes:
        - vertices:
            A collection of the vertices contained in this graph.
            Maps item to _WeightedVertex object or to a list of Vertex objects if the key represents a cluster.
    """
    vertices: dict[str | int, _WeightedVertex | dict[str, _WeightedVertex]]

    def __init__(self) -> None:
        """Initialize an empty graph (no vertices or edges)."""
        self.vertices = {}

    def add_vertex(self, item: Any, vertex_data: dict[str, float], coordinates: tuple[float, float], vertex_type: str,
                   cluster: int = 0) -> None:
        """Add a vertex with the given item to this graph.

        The new vertex is not adjacent to any other vertices.
        """
        if cluster == 0:
            if item not in self.vertices:
                self.vertices[item] = _WeightedVertex(
                    item, vertex_data, {}, cluster, coordinates, vertex_type)
        else:
            if cluster not in self.vertices:
                self.vertices[cluster] = {item: _WeightedVertex(
                    item, vertex_data, {}, cluster, coordinates, vertex_type)}
            else:
                self.vertices[cluster][item] = _WeightedVertex(
                    item, vertex_data, {}, cluster, coordinates, vertex_type)

    def add_edge(self, item1: str, item2: str, distance: int, weight: float = 1.0) -> None:
        """Add an edge between the two vertices with the given items in this graph,
        with the given weight.

        Raise a ValueError if item1 or item2 do not appear as vertices in this graph.

        Preconditions:
            - item1 != item2
            - not (self.vertices[item1].cluster > 0 and self.vertices[item2].cluster > 0)
              or (distance == 0 and weight == 0)
            - (self.vertices[item1].cluster > 0 and self.vertices[item2].cluster > 0) == (distance == 0)
        """
        all_vertices = self.get_vertices()
        if item1 in all_vertices and item2 in all_vertices:
            v1 = all_vertices[item1]
            v2 = all_vertices[item2]
            v1.neighbours[v2] = [distance, weight]
            v2.neighbours[v1] = [distance, weight]
        else:
            raise ValueError

    def calculate_edge_weight(self, row: list, factor_weights: list[float]) -> float:
        """Returns the weight of the edge between the vertex with item 1 and the vertex with item 2 based on the data
        for each edge in the edge_data csv file. Each line of the csv file contains data about one edge.

        All factors in row are located after index 2 (i.e. from index 3 on).

        Weight is calculated by subtracting the product between each individual weight in the list factor_weights
        with each factor in row from 1 (i.e. 1 - weight_so_far).

        Preconditions:
         - item1 in row and item2 in row
         - len(factor_weights) == len(row) - 3
         - All factors in row are located after index 2
        """
        weight_so_far = 0
        for i in range(len(factor_weights)):
            weight_so_far += factor_weights[i] * float(row[i + 3])
        return 1 - weight_so_far

    def get_neighbours(self, item: Any) -> set:
        """Returns a set of the neighbours of the given item.

        Note that the *items* are returned, not the _Vertex objects themselves.

        Raise a ValueError if item does not appear as a vertex in this graph.
        """
        all_vertices = self.get_vertices()
        if item in all_vertices:
            v = all_vertices[item]
            return {neighbour.item for neighbour in v.neighbours}
        else:
            raise ValueError

    def get_vertices(self) -> dict[str, _WeightedVertex]:
        """Returns a dictionary mapping the item to its respective vertex.

        Since in this WeightedGraph implementation we use cluster identifiers as some of the keys in the self.vertices
        dictionary, this method can facilitate certain manipulations in the graph.
        """
        all_vertices = {item: self.vertices[item] for item in self.vertices if isinstance(item, str)}
        for key in self.vertices:
            if isinstance(key, int):  # means key is a cluster identifier
                for subkey in self.vertices[key]:  # access inner dictionary that represents the vertices inside cluster
                    all_vertices[subkey] = self.vertices[key][subkey]
        return all_vertices

    def get_edges(self) -> set[tuple[str, str]]:
        """Returns a list with all the edges in self.

        The edge is represented by a tuple which contains the item of vertex1 and the item of vertex2.
        """
        all_edges = set()
        all_vertices = self.get_vertices()

        for item in all_vertices:
            neighbours = self.get_neighbours(item)
            for item2 in neighbours:
                all_edges.add((item, item2))

        return all_edges

    def get_cluster(self, cluster: int) -> dict[str, _WeightedVertex] | int:
        """Returns the vertices that are part of the given cluster.
        """
        for key in self.vertices:
            if key == cluster:
                return self.vertices[key]

        raise ValueError

    def create_cycle(self, vertices: list[str], weights: Union[list[float], float] = 0.0) -> None:
        """Generates a cycle representation of a cluster with the vertices with its respective items inside <vertices>.
        All edges have, by default, weight equal 0 between each other (i.e. simulated real-world distance and weighted
        distance are both equal to 0).

        If there are only 2 vertices inside the cluster they are connected to each other by an edge.

        Preconditions:
         - all(v in self.get_vertices())
        """
        for i in range(len(vertices)):
            self.add_edge(vertices[i], vertices[(i + 1) % len(vertices)], 0, weights)

    def adjacent(self, item1: Any, item2: Any) -> bool:
        """Return whether item1 and item2 are adjacent vertices in this graph.

        Return False if item1 or item2 do not appear as vertices in this graph.
        """
        if item1 in self.vertices and item2 in self.vertices:
            v1 = self.vertices[item1]
            return any(v2.item == item2 for v2 in v1.neighbours)
        else:
            # We didn't find an existing vertex for both items.
            return False


class GraphGenerator:
    """
    GraphGenerator generates two WeightedGraph based on the vertex and edge data provided.

    This class loads all needed graph functionality for both normal_graph and scaled_graph based on the data inputed as
    vertex_data, edge_data, and factor_weights.

    Instance Attributes:
     - normal_graph: a WeightedGraph that simulates the real world map with the normal distances between places
        as the weights of the edges between vertices.
     - scaled_graph: a WeightedGraph that represents how efficient, in real life, it really is to get from a
        location to another. In this model, the weights of each edge are the real world distance between the two places
        times a factor.

    Representation Invariants:
     - len(self.normal_graph.vertices) > 0
     - len(self.scaled_graph.vertices) > 0
    """
    normal_graph: WeightedGraph
    scaled_graph: WeightedGraph

    def __init__(self, vertex_data_file: str, edge_data_file: str, factor_weights: list[float],
                 vertex_data_categories: dict[str, list[str]]) -> None:
        """Initialize a new WeightedGraph representation of the region in between two franchises
        based on data collected.

        vertex_data: path to a csv file containing information about every vertex.
        edge_data: path to a csv file containing information about every weighted edge.
        factor_weights: list with decimals used to weigh each component that composes the total weight of an edge.
        vertex_data_categories: A dictionary which maps the vertex to the categories of data associted with it.

        Preconditions:
         - all(_check_len_data_row(edge_data_file) - 3 == len(factor_weights) for row in edge_data)
         - First column of edge_data contains vertex1 name (i.e. vertex1 item) or the cluster it belongs to.
         - Second column of edge_data contains vertex2 name (i.e. vertex2 item) or the cluster it belongs to.
         - Third column of edge_data contains the approximated real-world distance between one place (vertex)
         and another.
         - First column of vertex_data contains vertex type.
         - Second column of vertex_data contains vertex cluster.
         - Third column of vertex_data contains the name of the vertex (i.e. vertex item).
        """
        len_edge_data_row = self._check_len_data_row(edge_data_file)
        self.normal_graph = self.load_graph(vertex_data_file, edge_data_file,
                                            [0] * len_edge_data_row, vertex_data_categories)
        self.scaled_graph = self.load_graph(vertex_data_file, edge_data_file, factor_weights, vertex_data_categories)

    def _check_len_data_row(self, data_file: str) -> int:
        """Returns the length of a row in the data_file.

        Used to check if length of data_file's row is correct and to get the length of the row.
        """
        len_data_row = 0
        with open(data_file) as edge_data:
            line = csv.reader(edge_data.readline())
            for row in line:  # gets the length of the first row and breaks the loop, so loop only runs once.
                len_data_row = len(row)  # Thus E9996 error ignored.
                break
        return len_data_row

    def load_graph(self, vertex_data: str, edge_data: str, factor_weights: list[float],
                   vertex_data_categories: dict[str, list[str]]) -> WeightedGraph:
        """Returns a loaded WeightedGraph representation of the region in between two franchises.
        """
        graph = WeightedGraph()
        self.load_vertex_data(graph, vertex_data, vertex_data_categories)
        self.load_clusters(graph)
        self.load_edge_data(graph, edge_data, factor_weights)
        return graph

    def load_vertex_data(self, graph: WeightedGraph, vertex_data: str,
                         vertex_data_categories: dict[str, list[str]]) -> None:
        """Populates the given WeightedGraph with the vertices retrieved from the given vertex data file.

        vertex_data is a csv file containing the following information about each vertex:
         1. Vertex type (whether it is a Franchise, a TTC stop, a Landmark, a Intersection, or Another Restaurant;
         2. Vertex cluster (an integer representing the group in which the vertex is inserted in, and if it's 0 then
            it's not part of a cluster);
         3. Vertex name (i.e. the <item>);
         4. Vertex data (i.e. number representation of the factors that describe that vertex).
         5. Vertex coordinates (the geographical coordinates of each vertex)
        """
        types = list(vertex_data_categories)
        with open(vertex_data) as v_data:
            reader = csv.reader(v_data)
            for row in reader:
                if str(row[0]) == types[0]:
                    data_names_list = vertex_data_categories[types[0]]
                elif str(row[0]) == types[1]:
                    data_names_list = vertex_data_categories[types[1]]
                elif str(row[0]) == types[2]:
                    data_names_list = vertex_data_categories[types[2]]
                elif str(row[0]) == types[3]:
                    data_names_list = vertex_data_categories[types[3]]
                elif str(row[0]) == types[4]:
                    data_names_list = vertex_data_categories[types[4]]
                else:
                    data_names_list = vertex_data_categories[types[5]]
                data_dict = self._map_name_to_data(data_names_list, row[3:11])
                graph.add_vertex(row[2], data_dict, (float(row[-2]), float(row[-1])), row[0], int(row[1]))

    def _map_name_to_data(self, data_names: list[str], row: list) -> dict[str, Any]:
        """Helper function that returns a dictionary mapping each name from the given data_names list to its respective
        data in the row of data_file.
        """
        data_dict = {}
        for i in range(len(data_names)):
            data_dict[data_names[i]] = float(row[i])
        return data_dict

    def load_clusters(self, graph: WeightedGraph) -> None:
        """Generates all clusters in the graph as cycles. Except when the cluster has 2 vertices, then they are
        connected by one edge in between them.
        """
        amount_of_clusters = sum(1 for item in graph.vertices if isinstance(item, int))
        for cluster in range(1, amount_of_clusters + 1):
            vertices = list(graph.vertices[cluster])
            graph.create_cycle(vertices)

    def load_edge_data(self, graph: WeightedGraph, edge_data: str, factor_weights: list[float]) -> None:
        """Generates edges for the given scaled_graph based on the information given in the edge_data csv file.

        edge_data is a csv file that contains the following data about each edge;
         1. v1 and v2, v1 and a cluster, a cluster and v2, or a cluster and another cluster;
         2. The real life distance in meters between one vertex and the other;
         3. Other important information that describe that edge (i.e. a road).

         Each factor in edge data is multiplied by the corrisponding weight in factor_weights.

        Preconditions:
         - len(scaled_graph._vertices) >= 2
        """
        with open(edge_data) as e_data:
            reader = csv.reader(e_data)
            for row in reader:
                distance = int(row[2])
                weight = graph.calculate_edge_weight(row, factor_weights)
                items = self._convert_type([row[0], row[1]])
                item_row0 = items[0]
                item_row1 = items[1]
                if isinstance(item_row0, int) and isinstance(item_row1, int):
                    cluster1 = graph.get_cluster(int(item_row0))
                    cluster2 = graph.get_cluster(int(item_row1))
                    item1_cluster1 = list(cluster1)[0]
                    item2_cluster2 = list(cluster2)[0]
                    graph.add_edge(item1_cluster1, item2_cluster2, distance, weight)
                elif isinstance(item_row0, str) and isinstance(item_row1, int):
                    cluster = graph.get_cluster(int(item_row1))
                    item1_cluster = list(cluster)[0]
                    item2 = item_row0
                    graph.add_edge(item1_cluster, item2, distance, weight)
                elif isinstance(item_row0, int) and isinstance(item_row1, str):
                    cluster = graph.get_cluster(int(item_row0))
                    item1 = item_row1
                    item2_cluster = list(cluster)[0]
                    graph.add_edge(item1, item2_cluster, distance, weight)
                else:
                    graph.add_edge(item_row0, item_row1, distance, weight)

    def _convert_type(self, items: list[str | int]) -> list[str | int]:
        """Tries to convert each item in a list into an integer, and if it can, mutates the list to convert the item
        to an integer.
        """
        for i in range(len(items)):
            try:
                items[i] = int(items[i])
            except ValueError:
                pass

        items_alias = items
        return items_alias


if __name__ == '__main__':
    import python_ta.contracts

    python_ta.contracts.check_all_contracts()

    import doctest

    doctest.testmod()

    import python_ta

    python_ta.check_all(config={
        'extra-imports': ['csv', 'plotly.graph_objects', 'program_data'],
        'disable': ['E9996', 'R0914', 'R0913', 'E9998', 'R1702'],
        'allowed-io': ['_check_len_data_row', 'load_edge_data', 'load_vertex_data'],
        'max-line-length': 120
    })

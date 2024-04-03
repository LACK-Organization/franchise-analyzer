"""CSC111 Project 2: LACK's Franchise Analyzer

This module contains the main classes for Franchise Analyzer including _WeightedVertex, WeightedGraph,
and GraphGenerator. This classes are meant to be imported and used in analyzer.py.

Created by Leandro Hamaguchi, Aryan Nair, Carlos Solares, and Karan Singh. (LACK)
TODO: Finish file dosctring!
TODO: Add RI and IA to every class (update if needed)!
TODO: Explain, in the docstring, new terms created (e.g. cluster, vertex type, etc.)
"""
from __future__ import annotations
import csv
from typing import Any, Union


class _WeightedVertex:
    """A vertex in a graph.

    Instance Attributes: TODO: update docstring
        - item: The name of this vertex.
        - vertex_data: The data stored within this vertex.
        - neighbours: A dictionary mapping the vertices that are adjacent to this vertex to a list with the first item
        as the real life distance from one vertex to the other and the second item as the actual graph weight of the
        edge.
        - cluster: An integer representing the cluster the vertex is a part of. A cluster value
        of 0 means that the vertex is not part of any cluster.
        - coordinates: The coordinates of the vertex.

    Representation Invariants:
        - self not in self.neighbours
        - all(self in u.neighbours for u in self.neighbours)
    """
    item: str
    vertex_data = dict
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
        self.vertex_type: vertex_type

    def best_weighted_path(self, vertex2: str, visited: set[_WeightedVertex]) -> list:
        """Calculate the best weighted score between any two points on the graph based on the weighted edges.
        We calculate the full weight of each edge as distance * (1 - weight). Then to find the weighted score between
        two vertices, we find the least sum of all edges between the two vertices.

        NEW IMPLEMENTATION: Returns a list of two elements: the score, and a list of the vertices in the chosen path.

        Preconditions:
         - vertex1 != vertex2
         - vertex1 is in graph
         - vertex2 is in graph
         - WeightedGraph is connected
        """
        score = 0
        visited.add(self)
        path = [self]
        all_neighbours = {}
        if self == vertex2:
            return [score, path]
        else:
            for neighbour in self.neighbours:
                if neighbour not in visited:
                    score += self.neighbours[neighbour][0] * (1 - self.neighbours[neighbour][1])
                    best_score = neighbour.best_weighted_path(vertex2, visited)
                    score += best_score[0]
                    path += best_score[1]
                    all_neighbours[score] = path

            if all_neighbours == {}:
                return [score, path]
            else:
                min_path_score = min(all_neighbours)
                path = all_neighbours[min(all_neighbours)]

                return [min_path_score, path]

    def calculate_customer_choice(self, vertex: str, franchise1: str, franchise2: str):
        """
        Calculate which McDonald's a customer would be more likely to go to, given the vertex of the
        customer's location. Uses the weighed edges to calculate the path with the highest score.

        Preconditions:
         -
        """
        score_franchise1 = best_weighted_path(vertex, franchise1)
        score_franchise2 = best_weighted_path(vertex, franchise2)


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

    def add_vertex(self, item: Any, vertex_data: dict, coordinates: tuple[float, float], vertex_type: str,
                   cluster: int = 0) -> None:
        """Add a vertex with the given item to this graph.

        The new vertex is not adjacent to any other vertices.
        """
        if cluster == 0:
            if item not in self.vertices:
                self.vertices[item] = _WeightedVertex(item, vertex_data, {}, cluster, coordinates,
                                                       vertex_type)
        else:
            if cluster not in self.vertices:
                self.vertices[cluster] = {item: _WeightedVertex(item, vertex_data, {}, cluster, coordinates,
                                                                 vertex_type)}
            else:
                self.vertices[cluster][item] = _WeightedVertex(item, vertex_data, {}, cluster, coordinates,
                                                                vertex_type)
                # TODO: If time permits, make a helper to connect the vertices in a
                                                   # cycle.


    def add_edge(self, item1: str | int, item2: str | int, distance: int, weight: float = 1.0) -> None:
        """Add an edge between the two vertices with the given items in this graph,
        with the given weight.

        Raise a ValueError if item1 or item2 do not appear as vertices in this graph.

        Preconditions:
            - item1 != item2
            - not (self.vertices[item1].cluster > 0 and self.vertices[item2].cluster > 0)
              or (distance == 0 and weight == 0)
            - (self.vertices[item1].cluster > 0 and self.vertices[item2].cluster > 0) == (distance == 0)
        """
        if not (item1 in self.vertices and item2 in self.vertices):
            raise ValueError
        else:
            v1 = self.vertices[item1]
            v2 = self.vertices[item2]
            if v1.cluster != 0 and v2.cluster == 0:
                v1[list(self.vertices.keys())[0]].neighbours[v2] = [distance, weight]
                v2.neighbours[v1] = [distance, weight]
            elif v1.cluster == 0 and v2.cluster != 0:
                v1.neighbours[v2] = [distance, weight]
                v2[list(self.vertices.keys())[0]].neighbours[v1] = [distance, weight]
            elif v1.cluster != 0 and v2.cluster != 0:
                v1[list(self.vertices.keys())[0]].neighbours[v2] = [distance, weight]
                v2[list(self.vertices.keys())[0]].neighbours[v1] = [distance, weight]
            else:
                v1.neighbours[v2] = [distance, weight]
                v2.neighbours[v1] = [distance, weight]

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
            weight_so_far += factor_weights[i] * row[i + 3]
        return 1 - weight_so_far

    def get_neighbours(self, item: Any) -> set:
        """Returns a set of the neighbours of the given item.

        Note that the *items* are returned, not the _Vertex objects themselves.

        Raise a ValueError if item does not appear as a vertex in this graph.
        """
        if item in self.vertices:
            v = self.vertices[item]
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

    def get_cluster(self, cluster: int) -> dict[str, _WeightedVertex]:
        """Returns the vertices that are part of the given cluster.
        """
        for key in self.vertices:
            if key == cluster:
                return self.vertices[key]

    def create_cluster(self, vertices: list[str], weights: Union[list[float], float] = 0.0) -> None:
        """Generates a cycle representation of a cluster with the vertices with its respective items inside <vertices>.
        All edges have, by default, weight equal 0 between each other (i.e. simulated real-world distance and weighted distance are both equal
        to 0).

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

    def __init__(self, vertex_data_file: str, edge_data_file: str, factor_weights: list[float]) -> None:
        """Initialize a new WeightedGraph representation of the region in between two franchises
        based on data collected.

        vertex_data: path to a csv file containing information about every vertex.
        edge_data: path to a csv file containing information about every weighted edge.
        factor_weights: list with decimals used to weigh each component that composes the total weight of an edge.

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
        self.normal_graph = self.load_graph(vertex_data_file, edge_data_file, [] * len_edge_data_row)
        self.scaled_graph = self.load_graph(vertex_data_file, edge_data_file, factor_weights)

    def _check_len_data_row(self, data_file: str) -> int:
        """Returns the length of a row in the data_file.

        Used to check if length of data_file's row is correct and to get the length of the row.
        """
        len_data_row = 0
        with open(data_file) as edge_data:
            line = csv.reader(edge_data.readline())
            for row in line:  # gets the length of the first row and breaks the loop
                len_data_row = len(row)
                break
        return len_data_row

    def load_graph(self, vertex_data: csv, edge_data: csv, factor_weights: list[float]) -> WeightedGraph:
        """Returns a loaded WeightedGraph representation of the region in between two franchises.
        """
        graph = WeightedGraph()
        self.load_vertex_data(graph, vertex_data)
        self.load_edge_data(graph, edge_data, factor_weights)
        return graph

    def load_vertex_data(self, scaled_graph: WeightedGraph, vertex_data: csv) -> None:
        """Populates the given WeightedGraph with the vertices retrieved from the given vertex data file.

        vertex_data is a csv file containing the following information about each vertex:
         1. Vertex type (whether it is a Franchise, a TTC stop, a Landmark, a Intersection, or Another Restaurant;
         2. Vertex cluster (an integer representing the group in which the vertex is inserted in, and if it's 0 then
            it's not part of a cluster);
         3. Vertex name (i.e. the <item>);
         4. Vertex data (i.e. number representation of the factors that describe that vertex).

        TODO: Change function to work on every data_file based on headers
        """
        for row in vertex_data:
            data_names_list = []
            if str(row[0]) == 'MCD':
                data_names_list = ['Vehicular Traffic', 'Pedestrian Traffic', 'Bike Traffic', 'Reviews',
                                  'Operating Hours', 'Drive Through', 'Wifi']
            elif str(row[0]) == 'OtherRestaurant':
                data_names_list = ['Reviews', 'Client Similarity']
            elif str(row[0]) == 'Landmark':
                data_names_list = ['Significance']
            elif str(row[0]) == 'Intersection Main':
                data_names_list = ['Bike Per Car Ratio', 'Vehicular Traffic', 'Pedestrian Traffic Traffic']
            elif str(row[0]) == 'Intersection Small':
                scaled_graph.add_vertex(row[2], {}, (float(row[-2]), float(row[-1])), row[0], int(row[1]))
            elif str(row[0]) == 'Intersection':
                data_names_list = ['Bike Per Car Ratio', 'Vehicular Traffic', 'Pedestrian Traffic Traffic',
                                  'Longitude', 'Latitude']
            else:
                data_names_list = ['Google Reviews']
            data_dict = self._map_name_to_data(data_names_list, row)
            scaled_graph.add_vertex(row[2], data_dict, (float(row[-2]), float(row[-1])), row[0], int(row[1]))

    def _map_name_to_data(self, data_names: list[str], row: list) -> dict[str, Any]:
        """Helper function that returns a dictionary mapping each name from the given data_names list to its respective
        data in the row of data_file.
        """
        data_dict = {}
        for i in range(len(data_names)):
            data_dict[data_names[i]] = str(row[i])
        return data_dict

    def load_edge_data(self, scaled_graph: WeightedGraph, edge_data: csv, factor_weights: list[float]) -> None:
        """Generates edges for the given scaled_graph based on the information given in the edge_data csv file.
        This

        edge_data is a csv file that contains the following data about each edge:
         1. v1 and v2, v1 and a cluster, a cluster and v2, or a cluster and another cluster;
         2. The real life distance in meters between one vertex and the other;
         3. Other important information that describe that edge (i.e. a road).

        Preconditions:
         - len(scaled_graph._vertices) >= 2

        TODO: finish this docstring
        """
        clusters_created = []
        for row in edge_data:
            distance = row[2]
            weight = scaled_graph.calculate_edge_weight(row, factor_weights)
            if (isinstance(row[0], int) and isinstance(row[1], int)) and (row[0] not in clusters_created
                                                                            and row[1] not in clusters_created):
                # Connecting clusters as cycles in graph:
                cluster1 = scaled_graph.get_cluster(row[0])
                cluster2 = scaled_graph.get_cluster(row[1])
                scaled_graph.create_cluster(list(cluster1))
                scaled_graph.create_cluster(list(cluster2))
                clusters_created.append(row[0])
                clusters_created.append(row[1])
                # Adding edge between clusters:
                item1_cluster1 = list(cluster1)[0]
                item2_cluster2 = list(cluster2)[0]
                scaled_graph.add_edge(item1_cluster1, item2_cluster2, distance, weight)
            elif isinstance(row[0], str) and isinstance(row[1], int) and row[1] not in clusters_created:
                # Connecting cluster as cycle in graph:
                cluster = scaled_graph.get_cluster(row[1])
                scaled_graph.create_cluster(list(cluster))
                clusters_created.append(row[1])
                # Adding edge between vertex and cluster:
                item1_cluster = list(cluster)[0]
                item2 = row[0]
                scaled_graph.add_edge(item1_cluster, item2, distance, weight)
            elif isinstance(row[0], int) and isinstance(row[1], str) and row[0] not in clusters_created:
                # Connecting cluster as cycle in graph:
                cluster = scaled_graph.get_cluster(row[0])
                scaled_graph.create_cluster(list(cluster))
                clusters_created.append(row[0])
                # Adding edge between cluster and vertex:
                item1 = row[1]
                item2_cluster = list(cluster)[0]
                scaled_graph.add_edge(item1, item2_cluster, distance, weight)
            else:
                scaled_graph.add_edge(row[0], row[1], distance, weight)

    def _load_edge_data_helper(self, vertex1: str | int, vertex2: str | int, edge_file: str) -> dict:
        """Return the data corresponding to the edge between vertex1 and vertex2."""
        # TODO: Check if function is necessary
        with open(edge_file, 'r') as roads:
            reader = csv.reader(roads)
            mapping = {}
            for row in reader:
                if row[0] == vertex1 and row[1] == vertex2:
                    mapping['vertex1'] = row[0]
                    mapping['vertex2'] = row[1]
                    mapping['distance'] = row[2]
                    mapping['safety'] = row[3]
                    mapping['road hierarchy'] = row[4]
                    mapping['speed limit'] = row[5]
        return mapping

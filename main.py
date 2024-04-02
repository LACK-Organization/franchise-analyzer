"""
LACK's Franchise Analyser
TODO: Finish file dosctring
"""
from __future__ import annotations
import csv
from typing import Any, Union, TextIO





def get_weight(vertex1: str, vertex2: str, edge_data: str) -> float:
    with open(edge_data, 'r') as file:
        reader = csv.reader(file)
        weight = 0
        for row in reader:
            if (str(row[0]) == vertex1 or str(row[0]) == vertex2) and (str(row[1]) == vertex1 or str(row[1]) == vertex2):
                weight += 0.45 * float(row[3]) + 0.35 * float(row[4]) + 0.2 * float(row[5])
        return weight


class _WeightedVertex:
    """A vertex in a graph.

    Instance Attributes: TODO: update docstring
        - item: The name of this vertex.
        - vertex_data: The data stored within this vertex.
        - neighbours: The vertices that are adjacent to this vertex.
        - cluster: An integer representing the cluster the vertex is a part of. A cluster value
        of 0 means that the vertex is not part of any cluster.
        - coordinates: The coordinates of the vertex.

    Representation Invariants:
        - self not in self.neighbours
        - all(self in u.neighbours for u in self.neighbours)
    """
    item: str
    vertex_data = dict
    neighbours: dict[_WeightedVertex, Union[int, float]]
    cluster: int
    coordinates: tuple[float]
    vertex_type: str

    def __init__(self, item: str, vertex_data: dict, neighbours: dict[_WeightedVertex, Union[int, float]], cluster: int,
                 coordinates: tuple[float], vertex_type: str) -> None:
        """Initialize a new vertex with the given item and neighbours."""
        self.item = item
        self.vertex_data = vertex_data
        self.neighbours = neighbours
        self.cluster = cluster
        self.coordinates = coordinates
        self.vertex_type: vertex_type


class WeightedGraph:
    """A graph.

    Representation Invariants:
        - all(item == self._vertices[item].item for item in self._vertices)
        - all(is_instance(self._vertices[item], list) for item in self._vertices if is_instance(item, int))
        - all(is_instance(self._vertices[item], _WeightedVertex) for item in self._vertices if is_instance(item, str))

    Private Instance Attributes:
        - _vertices:
            A collection of the vertices contained in this graph.
            Maps item to _WeightedVertex object or to a list of Vertex objects if the key represents a cluster.
    """
    vertices: dict[str | int, _WeightedVertex | dict[str, _WeightedVertex]]

    def __init__(self) -> None:
        """Initialize an empty graph (no vertices or edges)."""
        self.vertices = {}

    def add_vertex(self, item: Any, vertex_data: dict, coordinates: tuple[float], vertex_type: str,
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


    def add_edge(self, item1: str | int, item2: str | int, weight: Union[int, float] = 1) -> None:
        """Add an edge between the two vertices with the given items in this graph,
        with the given weight.

        Raise a ValueError if item1 or item2 do not appear as vertices in this graph.

        Preconditions:
            - item1 != item2
        """
        if not (item1 in self.vertices and item2 in self.vertices):
            raise ValueError
        else:
            v1 = self.vertices[item1]
            v2 = self.vertices[item2]
            if v1.cluster != 0 and v2.cluster == 0:
                v1[list(self.vertices.keys())[0]].neighbours[v2] = weight
                v2.neighbours[v1] = weight
            elif v1.cluster == 0 and v2.cluster != 0:
                v1.neighbours[v2] = weight
                v2[list(self.vertices.keys())[0]].neighbours[v1] = weight
            elif v1.cluster != 0 and v2.cluster != 0:
                v1[list(self.vertices.keys())[0]].neighbours[v2] = weight
                v2[list(self.vertices.keys())[0]].neighbours[v1] = weight
            else:
                v1.neighbours[v2] = weight
                v2.neighbours[v1] = weight

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

    def best_score(self, vertex1: str, vertex2: str, graph: WeightedGraph, visited: set[_WeightedVertex]):
        """Calculate the best score between any two points on the graph based on the weighted edges.
        """
        score = 0

        v = self.vertices[vertex1]
        for neighbour in v.neighbours:
            if neighbour not in visited:


class DataEngine:
    """DataEngine generates a WeightedGraph based on the vertex and edge data we have.
    """

    graph_map: WeightedGraph

    def __init__(self, vertex_data: TextIO, edge_data: TextIO) -> None:
        """Initialize a new WeightedGraph representation of the region in between two franchises
        based on data collected.

        vertex_data: name of text file containing information about every vertex.
        edge_data: name of text file containing information about every weighted edge.
        """
        self.graph_map = self.load_graph(vertex_data, edge_data)

    def load_graph(self, vertex_data: TextIO, edge_data: TextIO) -> WeightedGraph:
        """Returns a loaded WeightedGraph representation of the region in between two franchises.
        TODO: finish this method and fix graph type: Type[WeightedGraph]
        """
        graph = WeightedGraph()
        self.load_vertex_data(graph, vertex_data)
        self.load_edge_data(graph, edge_data)
        return graph

    def load_vertex_data(self, graph_map: WeightedGraph, data_file: TextIO) -> None:
        """Populates the given WeightedGraph with the vertices retrieved from the given vertex data file.

        data_file is a text file containing the following information about each vertex (in the following order):
         1. Vertex type (whether it is a Franchise, a TTC stop, a Landmark, a Intersection, or Another Restaurant;
         2. Vertex cluster (an integer representing the group in which the vertex is inserted in, and if it's 0 then
            it's not part of a cluster);
         3. Vertex name (i.e. the <item>);
         4. Vertex data (i.e. number representation of the factors that describe that vertex).

        TODO: finish this method
        """
        for row in data_file:
            graph_map.add_vertex()
            graph_map.add_edge()
            if str(row[0]) == 'MCD':
                name_list = ['Type', 'Cluster', 'Name', 'Vehicular Traffic', 'Pedestrian Traffic',
                             'Bike Traffic', 'Reviews', 'Operating Hours', 'Drive Through', 'Wifi']
                for i in range(len(name_list)):
                    self[name_list[i]] = str(row[i])
            elif str(row[0]) == 'OtherRestaurant':
                name_list = ['Type', 'Cluster', 'Name', 'Reviews', 'Client Similarity']
                for i in range(len(name_list)):
                    data_mapping[name_list[i]] = str(row[i])
            elif str(row[0]) == 'Landmark':
                name_list = ['Type', 'Cluster', 'Name', 'Significance']
                for i in range(len(name_list)):
                    data_mapping[name_list[i]] = str(row[i])
            elif str(row[0]) == 'Intersection':
                name_list = ['Type', 'Cluster', 'Name', 'Bike Per Car Ratio', 'Vehicular Traffic',
                             'Pedestrian Traffic Traffic']
                for i in range(len(name_list)):
                    data_mapping[name_list[i]] = str(row[i])
            else:
                name_list = ['Type', 'Cluster', 'Name', 'Google Reviews']
                for i in range(len(name_list)):
                    data_mapping[name_list[i]] = str(row[i])

    def load_edge_data(self, graph_map: WeightedGraph, data_file: TextIO) -> None:
        """Generates edges... TODO: finish this method
        """

"""
LACK's Franchise Analyser
TODO: Finish file dosctring
"""
from __future__ import annotations
import csv
from typing import Any, Union

def data_collector(datafile: str, name: str, type: str) -> dict:
    """Return the data associtated with the vertex"""
    with open(datafile, 'r') as file1:
        reader = csv.reader(file1)
        data_mapping = {}
        for row in reader:
            if str(row[2]) == name and row[0] == type:
                if str(row[0]) == 'MCD':
                    data_mapping['Type'] = str(row[0])
                    data_mapping['Cluster'] = int(row[1])
                    data_mapping['Name'] = str(row[2])
                    data_mapping['Vehicular Traffic'] = int(row[3])
                    data_mapping['Pedestrian Traffic'] = int(row[4])
                    data_mapping['Bike Traffic'] = int(row[5])
                    data_mapping['Reviews'] = int(row[6])
                    data_mapping['Operating Hours'] = int(row[7])
                    data_mapping['Drive Through'] = int(row[8])
                    data_mapping['Wifi'] = int(row[9])
                elif str(row[0]) == 'OtherRestaurant':
                    data_mapping['Type'] = str(row[0])
                    data_mapping['Cluster'] = int(row[1])
                    data_mapping['Name'] = str(row[2])
                    data_mapping['Reviews'] = int(row[3])
                    data_mapping['Client Similarity'] = int(row[4])
                elif str(row[0]) == 'Landmark':
                    data_mapping['Type'] = str(row[0])
                    data_mapping['Cluster'] = int(row[1])
                    data_mapping['Name'] = str(row[2])
                    data_mapping['Significance'] = int(row[3])
                elif str(row[0]) == 'Intersection':
                    data_mapping['Type'] = str(row[0])
                    data_mapping['Cluster'] = int(row[1])
                    data_mapping['Name'] = str(row[2])
                    data_mapping['Bike Per Car Ratio'] = str(row[3])
                    data_mapping['Vehicular Traffic'] = str(row[4])
                    data_mapping['Pedestrian Traffic Traffic'] = str(row[5])
                else:
                    data_mapping['Type'] = str(row[0])
                    data_mapping['Cluster'] = int(row[1])
                    data_mapping['Name'] = str(row[2])
                    data_mapping['Google Reviews'] = int(row[3])
    return data_mapping





def _get_weight(vertex1: str, vertex2: str, edge_data: str) -> float:
    with open(edge_data, 'r') as file:
        reader = csv.reader(file)
        weight = 0
        for row in reader:
            if (str(row[0]) == vertex1 or str(row[0]) == vertex2) and (str(row[1]) == vertex1 or str(row[1]) == vertex2):
                weight = 0.45 * float(row[3]) + 0.35 * float(row[4]) + 0.2 * float(row[5])
        return weight


class _Vertex:
    """A vertex in a graph.

    Instance Attributes:
        - item: The name of this vertex.
        - vertex_data: The data stored within this vertex.
        - neighbours: The vertices that are adjacent to this vertex.
        - cluster: An integer representing the cluster the vertex is a part of. A cluster value
        of 0 means that the vertex is not part of any cluster.

    Representation Invariants:
        - self not in self.neighbours
        - all(self in u.neighbours for u in self.neighbours)
    """
    item: str
    vertex_data = dict
    neighbours: dict[_Vertex, Union[int, float]]
    cluster: int

    def __init__(self, item: str, vertex_data: dict, neighbours: dict[_Vertex, Union[int, float]], cluster: int) -> None:
        """Initialize a new vertex with the given item and neighbours."""
        self.item = item
        self.vertex_data = vertex_data
        self.neighbours = neighbours
        self.cluster = cluster


class Graph:
    """A graph.

    Representation Invariants:
        - all(item == self._vertices[item].item for item in self._vertices)
        - all(is_instance(self._vertices[item], list) for item in self._vertices if is_instance(item, int))
        - all(is_instance(self._vertices[item], _Vertex) for item in self._vertices if is_instance(item, str))

    Private Instance Attributes:
        - _vertices:
            A collection of the vertices contained in this graph.
            Maps item to _Vertex object or to a list of Vertex objects if the key represents a cluster.
    """
    _vertices: dict[str | int, _Vertex | list[_Vertex]]

    def __init__(self) -> None:
        """Initialize an empty graph (no vertices or edges)."""
        self._vertices = {}

    def add_vertex(self, item: Any, type_of_vertex: str, coordinates: tuple[int], cluster: int) -> None:
        """Add a vertex with the given item to this graph.

        The new vertex is not adjacent to any other vertices.
        """
        if item not in self._vertices:
            self._vertices[item] = _Vertex(item, {}, type_of_vertex, coordinates, cluster)

    def add_edge(self, item1: Any, item2: Any, weight: Union[int, float] = 1) -> None:
        """Add an edge between the two vertices with the given items in this graph,
        with the given weight.

        Raise a ValueError if item1 or item2 do not appear as vertices in this graph.

        Preconditions:
            - item1 != item2
        """
        if item1 in self._vertices and item2 in self._vertices:
            v1 = self._vertices[item1]
            v2 = self._vertices[item2]
            if v1.cluster_number == 0 and v2.cluster_number == 0:
                # Add the new edge
                v1.neighbours[v2] = weight
                v2.neighbours[v1] = weight
            elif v1.cluster_number == 0 and v2.cluster_number != 0:
                cluster = v2.cluster_number
                for i in self._vertices:
                    vertex = self._vertices[i]
                    if vertex.cluster_number == cluster:
                        v1.neighbours[vertex] = weight
                        vertex.neighbours[v1] = weight
            elif v2.cluster_number == 0 and v1.cluster_number != 0:
                cluster = v1.cluster_number
                for i in self._vertices:
                    vertex = self._vertices[i]
                    if vertex.cluster_number == cluster:
                        v2.neighbours[vertex] = weight
                        vertex.neighbours[v2] = weight
            elif v1.cluster_number != 0 and v1.cluster_number != 0:
                if v1.cluster_number == v2.cluster_number:

                else:


        else:
            # We didn't find an existing vertex for both items.
            raise ValueError

    def adjacent(self, item1: Any, item2: Any) -> bool:
        """Return whether item1 and item2 are adjacent vertices in this graph.

        Return False if item1 or item2 do not appear as vertices in this graph.
        """
        if item1 in self._vertices and item2 in self._vertices:
            v1 = self._vertices[item1]
            return any(v2.item == item2 for v2 in v1.neighbours)
        else:
            # We didn't find an existing vertex for both items.
            return False

    def get_neighbours(self, item: Any) -> set:
        """Return a set of the neighbours of the given item.

        Note that the *items* are returned, not the _Vertex objects themselves.

        Raise a ValueError if item does not appear as a vertex in this graph.
        """
        if item in self._vertices:
            v = self._vertices[item]
            return {neighbour.item for neighbour in v.neighbours}
        else:
            raise ValueError

"""
LACK's Franchise Analyser
"""
from __future__ import annotations
import csv
from typing import Any, Union


class _Vertex:
    """A vertex in a graph.

    Instance Attributes:
        - item: The data stored in this vertex.
        - neighbours: The vertices that are adjacent to this vertex.
        - type: The type of vertex in our graph.

    Representation Invariants:
        - self not in self.neighbours
        - all(self in u.neighbours for u in self.neighbours)
    """
    item: Any
    neighbours: dict[_Vertex, Union[int, float]]


    def __init__(self, item: Any, neighbours: dict[_Vertex, Union[int, float]], type: str) -> None:
        """Initialize a new vertex with the given item and neighbours."""
        self.item = item
        self.neighbours = neighbours
        self.type = type

class Franchise(_Vertex):
    """Subclass of Vertex used to represent a Franchise restaurant on our graph."""
    item: {}
    neighbours: dict[_Vertex, Union[int, float]]
    type: str

    def __init__(self, item: dict, neighbours: dict[_Vertex, Union[int, float]], type="Franchise") -> None:
        super().__init__(neighbours, type)
        self.item = item
        self.neighbours = neighbours
        self.type = type


class Landmark(_Vertex):
    """Subclass of Vertex used to represent a landmark on our graph. For example,
    a TTC station or a monument in Toronto."""
    item: Any
    neighbours: dict[_Vertex, Union[int, float]]
    type: str

    def __init__(self, item: str, neighbours: dict[_Vertex, Union[int, float]], type="Landmark") -> None:
        super().__init__(item, neighbours, type)
        self.type = type




class Graph:
    """A graph.

    Representation Invariants:
        - all(item == self._vertices[item].item for item in self._vertices)
    """
    # Private Instance Attributes:
    #     - _vertices:
    #         A collection of the vertices contained in this graph.
    #         Maps item to _Vertex object.
    _vertices: dict[Any, _Vertex]

    def __init__(self) -> None:
        """Initialize an empty graph (no vertices or edges)."""
        self._vertices = {}

    def add_vertex(self, item: Any, type: str) -> None:
        """Add a vertex with the given item to this graph.

        The new vertex is not adjacent to any other vertices.
        """
        if item not in self._vertices:
            if type == 'Franchise':
                self._vertices[item] = Franchise(item)
            else:
                self._vertices[item] = Landmark(item)

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

            # Add the new edge
            v1.neighbours[v2] = weight
            v2.neighbours[v1] = weight
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

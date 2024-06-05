from collections import defaultdict
from dataclasses import dataclass, field
from typing import MutableMapping, Container, Dict, Sized, Iterator, Tuple, Set


@dataclass(slots=True)
class Graph[T](MutableMapping[T, T], Container[T], Sized):
    """
    A Graph data structure that implements MutableMapping, Container, and Sized interfaces.

    The Graph is represented internally as a dictionary
    where each key-value pair corresponds to a vertex and its adjacent vertices.

    Attributes:
        _graph: A dictionary representing the graph.
        Each key is a vertex, and the value is a list of vertices adjacent to the key.

    Methods:
        __post_init__: Initializes the graph.
        __setitem__(key, value): Adds an edge from 'key' to 'value' in the graph.
        __delitem__(key): Removes the vertex 'key' and all its edges from the graph.
        __getitem__(key): Returns the vertices adjacent to the vertex 'key'.
        __len__(): Returns a tuple where the first element is the number of vertices,
        and the second element is the number of edges.
        __iter__(): Returns an iterator over the vertices in the graph.
        __contains__(item): Checks if the vertex 'item' is in the graph.
    """

    _graph: Dict[T, Set[T]] = field(default_factory=lambda: defaultdict(set), init=False)
    _vertex_to_id: Dict[T, int] = field(default_factory=dict, init=False)
    _counter: int = 0

    def __post_init__(self) -> None:
        """
        Initialize the Graph object after the instance has been created.

        This method is called after the instance has been created and has had its initial attributes set.
        """
        pass

    def __setitem__(self, __key: T, __value: T) -> None:
        """
        Add an edge from '__key' to '__value' in the graph.

        :param __key: The starting vertex of the edge.
        :param __value: The ending vertex of the edge.
        """
        self._graph[__key].add(__value)
        self._graph[__value] = set()

        if __key not in self._vertex_to_id:
            self._vertex_to_id[__key] = self._counter
            self._counter += 1

        if __value not in self._vertex_to_id:
            self._vertex_to_id[__value] = self._counter
            self._counter += 1

    def __delitem__(self, __key: T) -> None:
        """
        Remove the vertex '__key' and all its edges from the graph.

        :param __key: The vertex to be removed.
        """
        del self._graph[__key]
        for vertex in self._graph:
            self._graph[vertex].discard(__key)

    def __getitem__(self, __key: T) -> Set[T]:
        """
        Return the vertices adjacent to the vertex '__key'.

        :param __key: The vertex whose adjacent vertices are to be returned.
        :return: The vertices adjacent to the vertex '__key'.
        """
        return self._graph[__key]

    def __iter__(self) -> Iterator[T]:
        """
        Return an iterator over the vertices in the graph.

        :return: An iterator over the vertices in the graph.
        """
        return iter(self._graph)

    def __len__(self) -> Tuple[int, int]:
        """
        Calculate and return the number of vertices and edges in the graph.

        This method calculates the number of vertices by counting the number of keys in the `_vertex_to_id` dictionary.
        It calculates the number of edges by iterating over the values in the `_graph`
        dictionary (which are lists of edges), and summing up their lengths.

        :return: A tuple where the first element is the number of vertices, and the second element is the number of
        edges.
        """
        vertex_length: int = len(self._graph.keys())
        edges_length: int = sum(len(edges) for edges in self._graph.values())

        return vertex_length, edges_length

    def __contains__(self, item: T) -> bool:
        """
        Check if the vertex 'item' is in the graph.

        :param item: The vertex to be checked.
        :return: True if the vertex is in the graph, False otherwise.
        """
        return item in self._graph

    def convert_to_int(self, key: T) -> int:
        """
        Convert the key to an integer and return it.

        :exception: KeyError: If the key is not found in the graph.
        :param key: The key to be converted.
        :return: The integer representation of the key.
        """
        if key not in self._vertex_to_id:
            raise KeyError(f"Key {key} not found in the graph.")

        return self._vertex_to_id[key]

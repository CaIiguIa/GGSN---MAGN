from collections import defaultdict
from dataclasses import dataclass, field
from typing import MutableMapping, Container, Dict, List, Tuple, Sized


@dataclass(slots=True)
class Graph[K, T](MutableMapping[K, T], Container[K], Sized):
    _graph: Dict[int, List[int]] = field(default_factory=lambda: defaultdict(list), init=False)
    _vertex_to_id: Dict[K, int] = field(default_factory=dict, init=False)

    def __post_init__(self) -> None:
        pass

    def __setitem__(self, __key: K, __value: T) -> None:
        pass

    def __delitem__(self, __key: K) -> None:
        pass

    def __getitem__(self, __key: K) -> T:
        pass

    def __len__(self) -> Tuple[int, int]:
        """
        Calculate and return the number of vertices and edges in the graph.

        This method calculates the number of vertices by counting the number of keys in the `_vertex_to_id` dictionary.
        It calculates the number of edges by iterating over the values in the `_graph` dictionary (which are lists of edges),
        and summing up their lengths.

        :return: A tuple where the first element is the number of vertices and the second element is the number of edges.
        """
        vertex_length: int = len(self._vertex_to_id)
        edges_length: int = sum(len(edges) for edges in self._graph.values())

        return vertex_length, edges_length

    def __iter__(self) -> int:
        pass

    def __contains__(self, item: K) -> bool:
        pass

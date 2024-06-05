from collections import deque
from dataclasses import dataclass
from typing import final, Generator, List

from magn.database.structures.graph import Graph


@final
@dataclass(slots=True)
class TopologicalSorter:

    def sort(self, graph: Graph) -> Generator:
        stack = deque()
        vertex_length, _ = len(graph)

        visited: List[bool] = [False] * vertex_length

        for vertex in graph:
            if not visited[vertex]:
                self._dfs(graph, vertex, visited, stack)

        for element in stack:
            yield element

    def _dfs(self, graph: Graph, vertex: int, visited: List[bool], stack: deque) -> None:
        visited[vertex] = True

        for neighbour in graph[vertex]:
            if not visited[neighbour]:
                self._dfs(graph, neighbour, visited, stack)

        stack.appendleft(vertex)

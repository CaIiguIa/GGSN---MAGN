from collections import deque
from dataclasses import dataclass
from typing import final, Generator, List

from magn.database.structures.graph import Graph


@final
@dataclass(slots=True)
class TopologicalSorter:
    """
    A class that provides a method to perform topological sorting on a Graph.

    This class uses Depth-First Search (DFS) to perform the topological sort.

    Methods:
        sort(graph: Graph) -> Generator:
            Performs topological sorting on the given graph and returns a generator that yields the vertices in topological order.

        _dfs(graph: Graph, vertex: int, visited: List[bool], stack: deque) -> None:
            A helper method that performs Depth-First Search on the graph from the given vertex.
    """

    def sort(self, graph: Graph) -> Generator:
        """
        Perform topological sorting on the given graph.

        This method uses Depth-First Search (DFS) to visit each vertex in the graph.
        It maintains a stack of vertices, where each vertex is pushed onto the stack after all of its neighbours have been visited.

        :param graph: The graph to be sorted.
        :return: A generator that yields the vertices in topological order.
        """
        stack = deque()
        vertex_length, _ = len(graph)

        visited: List[bool] = [False] * vertex_length

        for vertex in graph:
            if not visited[vertex]:
                self._dfs(graph, vertex, visited, stack)

        for element in stack:
            yield element

    def _dfs(self, graph: Graph, vertex: int, visited: List[bool], stack: deque) -> None:
        """
        Perform Depth-First Search on the graph from the given vertex.

        This is a helper method used by the sort method. It visits the given vertex and all vertices reachable from it
        that haven't yet been visited. It maintains a stack of vertices, where each vertex is pushed onto the stack
        after all of its neighbours have been visited.

        :param graph: The graph to be traversed.
        :param vertex: The starting vertex for the DFS.
        :param visited: A list that keeps track of which vertices have been visited.
        :param stack: A stack of vertices, where each vertex is pushed onto the stack after all of its neighbours have been visited.
        """
        visited[vertex] = True

        for neighbour in graph[vertex]:
            if not visited[neighbour]:
                self._dfs(graph, neighbour, visited, stack)

        stack.appendleft(vertex)

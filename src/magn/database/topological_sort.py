"""Topological sorting algorithm for sorting dependencies."""

from collections import deque
from dataclasses import dataclass
from typing import final, Generator, Dict, Sequence


@final
@dataclass(slots=True)
class TopologicalSorter:
    """Sorts the given dependencies topologically and returns a generator of the sorted nodes."""

    def sort(self, dependencies: Dict[str, Sequence[str]]) -> Generator:
        """Sorts the given dependencies topologically and returns a generator of the sorted nodes."""
        stack = deque()
        visited = {node: False for node in dependencies}

        for node in dependencies:
            if not visited[node]:
                self._dfs(node, dependencies, visited, stack)

        while stack:
            yield stack.pop()

    def _dfs(self, node: str, dependencies: Dict[str, Sequence[str]], visited: Dict[str, bool], stack: deque) -> None:
        """Depth-first search helper function."""
        visited[node] = True

        for neighbor in dependencies[node]:
            if not visited[neighbor]:
                self._dfs(neighbor, dependencies, visited, stack)

        stack.append(node)

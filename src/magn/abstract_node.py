"""Module for base node class."""

from abc import ABC, abstractmethod
from typing import List, Self


class AbstractNode(ABC):
    """Base class for nodes in the graph."""

    @abstractmethod
    def neighbors(self) -> List[Self]:
        """Return the neighbours of the node."""
        raise NotImplementedError()

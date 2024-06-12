from dataclasses import dataclass
from pathlib import Path
from typing import Self, List, Dict

from magn.asa.asa_graph import ASAGraph
from magn.magn_object_node import MAGNObjectNode


@dataclass(slots=True)
class MAGNGraph:
    def __init__(self):
        self.asa_graphs: List[ASAGraph] = []
        self.objects: Dict[str, List[MAGNObjectNode]] = {}

    @classmethod
    def from_sqlite3(cls, file: Path) -> Self:
        """
        Substitute for the lack in ability to create many constructors in python.

        :param file:
        :return:
        """
        pass

    @classmethod
    def from_asa(cls, asa_graphs: List[ASAGraph]) -> Self:
        """
        Substitute for the lack in ability to create many constructors in python.

        :param asa_graphs:
        :return:
        """
        pass

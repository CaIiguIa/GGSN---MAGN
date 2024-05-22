from dataclasses import dataclass
from pathlib import Path
from typing import Self, List

from magn.asa.ASAGraph import ASAGraph


@dataclass(slots=True)
class MAGNGraph:

    @classmethod
    def from_sqlite3(cls, file: Path) -> Self:
        """
        Substitute for the lack in ability to create many constructors in python.

        :param file:
        :return:
        """
        raise NotImplementedError()

    @classmethod
    def from_asa(cls, asa_graphs: List[ASAGraph]) -> Self:
        """
        Substitute for the lack in ability to create many constructors in python.

        :param asa_graphs:
        :return:
        """
        raise NotImplementedError()

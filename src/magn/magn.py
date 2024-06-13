from dataclasses import dataclass
from pathlib import Path
from typing import Self, List

from magn.asa.ASAGraph import ASAGraph
from magn.database.database import Database
from magn.database.topological_sort import TopologicalSorter


@dataclass(slots=True)
class MAGNGraph:
    """
    TODO: Add docstring
    TODO: Add generics
    TODO: Change Any to proper ASAGraph[T] type
    """

    @classmethod
    def from_sqlite3(cls, file: Path) -> Self:
        """
        Substitute for the lack in the ability to create many constructors in python.

        :param file:
        :return:
        """
        database = Database.from_sqlite3(file)

        for table_name in database.sort():
            table = database.tables[table_name]
            for column in table.columns:
                column_data = table[column]

        raise NotImplementedError()

    @classmethod
    def from_asa(cls, asa_graphs: List[ASAGraph]) -> Self:
        """
        Substitute for the lack in the ability to create many constructors in python.

        :param asa_graphs:
        :return:
        """
        raise NotImplementedError()

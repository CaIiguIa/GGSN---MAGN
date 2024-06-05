from dataclasses import dataclass
from pathlib import Path
from typing import Self, List, Any, Container, Tuple
from collections.abc import MutableMapping

import pandas as pd

from magn.asa.ASAGraph import ASAGraph
from magn.database.converters.sqlite3 import SQLite3Converter
from magn.database.sorting.topological_sort import TopologicalSorter


@dataclass(slots=True)
class MAGNGraph[T](MutableMapping[Tuple[str, str], Any], Container[Tuple[str, str]]):
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
        converter = SQLite3Converter(file)
        database = converter.convert()
        sorter = TopologicalSorter()

        for table_id in sorter.sort(database.graph):
            table: pd.DataFrame = database.tables[table_id]

        raise NotImplementedError()


    @classmethod
    def from_asa(cls, asa_graphs: List[ASAGraph]) -> Self:
        """
        Substitute for the lack in the ability to create many constructors in python.

        :param asa_graphs:
        :return:
        """
        raise NotImplementedError()

    def __post_init__(self) -> None:
        raise NotImplementedError()

    def __setitem__(self, __key: Tuple[str, str], __value):
        raise NotImplementedError()

    def __delitem__(self, __key: Tuple[str, str]):
        raise NotImplementedError()

    def __getitem__(self, __key: Tuple[str, str]):
        raise NotImplementedError()

    def __len__(self):
        raise NotImplementedError()

    def __iter__(self):
        raise NotImplementedError()

    def __contains__(self, __item) -> bool:
        raise NotImplementedError()

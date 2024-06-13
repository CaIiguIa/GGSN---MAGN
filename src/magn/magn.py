from dataclasses import dataclass
from pathlib import Path
from typing import Self, List, Dict

import pandas as pd

from magn.asa.asa_graph import ASAGraph
from magn.database.database import Database
from magn.magn_object_node import MAGNObjectNode


@dataclass(slots=True)
class MAGNGraph:
    """
    TODO: Add docstring
    TODO: Add generics
    TODO: Change Any to proper ASAGraph[T] type
    """

    def __init__(self):
        """
        Initialize the MAGN graph.

        Attributes:
        asa_graphs: list of ASA graphs
        objects:    map of table names to a list of MAGN object nodes
        """
        self.asa_graphs: List[ASAGraph] = []
        self.objects: Dict[str, List[MAGNObjectNode]] = {}

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

    def fit(self, data: pd.DataFrame, num_epochs: int, learning_rate: float):
        if 'Target' not in data.keys():
            raise NameError("Data must have a target column.")

        data_no_target = data.drop(['Target'], axis=1)
        data_target = data['Target']
        asa_graphs = [self.get_asa_by_name(name) for name in data_no_target.keys()]
        target_asa_graph = self.get_asa_by_name(data_target.keys()[0])
        neurons = list(map(lambda _asa: _asa.get_elements(), asa_graphs))

        for epoch in range(num_epochs):
            for idx, row in data_no_target.iterrows():
                target_col = data_target[idx]
                target_value = row[target_col]
                row_no_target = row.drop([target_col])

    def get_asa_by_name(self, name: str) -> ASAGraph:
        """
        Get an ASA graph by name.

        :param name: the name of the ASA graph
        :return: the ASA graph with the given name
        """
        for asa_graph in self.asa_graphs:
            if asa_graph.name == name:
                return asa_graph

        raise ValueError(
            f"ASA graph with name {name} not found, check your input data. Column names may be "
            f"incorrect.")

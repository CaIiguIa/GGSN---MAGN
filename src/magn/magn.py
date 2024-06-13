from dataclasses import dataclass
from pathlib import Path
from typing import Self, List, Dict

from pandas import Series

from magn.asa.asa_graph import ASAGraph
from magn.magn_object_node import MAGNObjectNode


@dataclass(slots=True)
class MAGNGraph:
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

    def fit(self, data_x: Series, data_y: Series, num_epochs: int, ):
        """
        Fit the MAGN graph to the data. It is assumed that

        :param data_x: the data to fit the MAGN graph to
        :param num_epochs: the number of epochs to train the MAGN graph
        """
        for epoch in range(num_epochs):
            for datum in data_x:  # for every row of data
                asa_graphs = []
                for name in datum.keys():  # activate sensors
                    asa = self.get_asa_by_name(name)
                    if asa is None:
                        raise ValueError(
                            f"ASA graph with name {name} not found, check your input data. Column names may be "
                            f"incorrect.")
                    asa.sensor(datum[name])
                    asa_graphs.append(asa)

                activated_neurons = map(lambda _asa: _asa.get_elements(), asa_graphs)
                for neuron_i in activated_neurons:
                    for neuron_j in activated_neurons:
                        # TODO calculate delta
                        pass




                pass

    def get_asa_by_name(self, name: str) -> ASAGraph | None:
        """
        Get an ASA graph by name.

        :param name: the name of the ASA graph
        :return: the ASA graph with the given name
        """
        for asa_graph in self.asa_graphs:
            if asa_graph.name == name:
                return asa_graph
        return None

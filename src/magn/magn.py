from collections import deque
from dataclasses import dataclass
from pathlib import Path
from typing import Self, List, Dict

import pandas as pd

from magn.abstract_node import AbstractNode
from magn.asa.asa_element import ASAElement
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

        for epoch in range(num_epochs):
            for idx, row in data_no_target.iterrows():
                target_col = data_target[idx]
                target_value = row[target_col]
                row_no_target = row.drop([target_col])
                activated_neurons = list(map(lambda _asa: _asa.search(row_no_target[_asa.name]), asa_graphs))

                self._update_priorities(activated_neurons, target_value, learning_rate)

    def predict(self, data: pd.Series, target: str):
        activated_neurons = list(map(lambda _asa: _asa.search(data[_asa.name]), self.asa_graphs))
        return self._calculate_prediction(activated_neurons, target)

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

    def _update_priorities(self, neurons: List[ASAElement], target_value: int | float | str, learning_rate: float):
        """
        Update the priorities of the neurons in the MAGN graph.

        :param neurons: the neurons to update
        :param target_value: the target value
        :param learning_rate: the learning rate
        """
        if isinstance(target_value, str):
            deltas = self._calc_delta_categorical(neurons, target_value)
        else:
            deltas = self._calc_delta_numerical(neurons, target_value)

        for neuron, delta in zip(neurons, deltas):
            if delta == 0.0:
                neuron.priority *= (1 + learning_rate * neuron.key)
            else:
                neuron.priority *= (1 - learning_rate * delta * neuron.key)

    def _calc_delta_categorical(self, neurons: List[ASAElement], target_value: str) -> List[float]:
        """
        Calculate the delta for a categorical neuron.

        :param neurons: the neurons for which delta is calculated
        :param target_value: the target value
        :return: the deltas
        """
        deltas = []

        for neuron in neurons:
            delta = 0 if neuron.key == target_value else 1
            deltas.append(delta)

        return self._normalize(deltas)

    def _calc_delta_numerical(self, neurons: List[ASAElement], target_value: int | float) -> List[float]:
        """
        Calculate the delta for a numerical neuron.

        :param neurons: the neurons for which delta is calculated
        :param target_value: the target value
        :return: the delta
        """
        deltas = []

        for neuron in neurons:
            deltas.append(target_value - neuron.key)

        return self._normalize(deltas)

    def _normalize(self, values: List[float]) -> List[float]:
        """
        Normalize the values.

        :param values: the values to normalize
        :return: the normalized values
        """
        max_value = max(values)
        min_value = min(values)
        return [(value - min_value) / (max_value - min_value) for value in values]

    def _calculate_prediction(self, activated_neurons: List[ASAElement], target: str) -> int | float | str:
        """
        Calculate the prediction based on the activated neurons.

        :param activated_neurons: the activated neurons
        :param target: the target
        :return: the prediction
        """
        # go from activated_neurons to target feature (any value of target feature) with BFS
        # on all found paths, calculate the sum of the (neuron_priority * connection_weight) on the path
        # return the target value with the highest sum

        paths = []
        for neuron in activated_neurons:
            paths += self.bfs(neuron, target)

        stimulation = list(map(lambda path: self._stimulation(path), paths))
        max_stimuli = stimulation.index(max(stimulation))
        max_element = paths[max_stimuli][-1]
        if not isinstance(max_element, ASAElement):
            raise ValueError("Implementation error. The target feature is not an ASA element.")
        return max_element.key

    def bfs(self, start_node: ASAElement, target_feature: str):
        queue: deque[(AbstractNode, List[AbstractNode])] = deque(
            [(start_node, [start_node])])  # queue of (current_node, path)
        paths = []

        while queue:
            current_node, path = queue.popleft()

            if isinstance(current_node, ASAElement) and current_node.feature == target_feature:
                paths.append(path)
            else:
                for neighbor in current_node.neighbors():
                    if neighbor not in path:
                        queue.append((neighbor, path + [neighbor]))
        return paths

    def _stimulation(self, path: List[AbstractNode]) -> float:
        stimulation = 0.0
        # Iterate over neighboring pairs
        for i, (current_node, next_node) in enumerate(zip(path, path[1:])):
            current_is_element = isinstance(current_node, ASAElement)
            current_is_object = isinstance(current_node, MAGNObjectNode)
            next_is_element = isinstance(next_node, ASAElement)
            next_is_object = isinstance(next_node, MAGNObjectNode)

            if current_is_element and next_is_element:
                if current_node.bl_next is next_node:
                    stimulation += current_node.priority * current_node.bl_next_weight
                else:
                    stimulation += current_node.priority * current_node.bl_prev_weight

            if current_is_element and next_is_object:
                stimulation += current_node.priority * current_node.magn_weight()

            if current_is_object and next_is_element:
                stimulation += current_node.priority * next_node.magn_weight()

            if current_is_object and next_is_object:
                stimulation += current_node.priority * next_node.magn_weight()

        return stimulation

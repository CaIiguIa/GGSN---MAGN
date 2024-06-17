"""MAGN graph module."""

from collections import deque
from dataclasses import dataclass, field
from pathlib import Path
from typing import Self, List, Dict, Tuple, Final

import pandas as pd

from magn.abstract_node import AbstractNode
from magn.asa.asa_element import ASAElement
from magn.asa.asa_graph import ASAGraph
from magn.database.database import Database
from magn.magn_object_node import MAGNObjectNode


@dataclass(slots=True)
class MAGNGraph:
    """Class related to creating and managing MAGN.
    TODO: Add docstring
    TODO: Add generics
    TODO: Change Any to proper ASAGraph[T] type
    """

    asa_graphs: List[ASAGraph] = field(default_factory=list)
    objects: Dict[str, List[MAGNObjectNode]] = field(default_factory=dict)

    @classmethod
    def from_sqlite3(cls, file: Path) -> Self:
        """Substitute for the lack in the ability to create many constructors in python."""

        database = Database.from_sqlite3(file)
        magn = MAGNGraph()

        print("Processing tables...")
        for table_name in database.sort():
            table, keys = database[table_name]
            p_keys, f_keys = keys

            asa_graphs, objects = magn._process_table(table, p_keys, f_keys, table_name)
            magn.asa_graphs += asa_graphs
            magn.objects[table_name] = objects
            print(f"Table {table_name} processed.")
        print("Tables processed.")
        return magn

    def fit(self, data: pd.DataFrame, num_epochs: int, learning_rate: float):
        mock_name: Final[str] = Database.mock_column_name

        if mock_name not in data.keys():
            raise NameError("Data must have a target column.")

        data_no_target = data.drop([mock_name], axis=1)
        data_target = data[mock_name]
        asa_graphs = [self.get_asa_by_name(name) for name in data_no_target.columns]
        print("Teaching MAGN...")
        for epoch in range(num_epochs):
            print(f"epoch {epoch}...")
            for idx, row in data_no_target.iterrows():
                target_col = data_target[idx]
                target_value = row[target_col]
                row_no_target = row.drop([target_col])
                asa_no_target = [asa for asa in asa_graphs if asa.name != target_col]
                activated_neurons = list(map(lambda _asa: _asa.search(row_no_target[_asa.name]), asa_no_target))

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

    def _process_table(self, table: pd.DataFrame,
                       primary_keys: List[str],
                       foreign_keys: Dict[str, Tuple[str, str]],
                       table_name: str) -> Tuple[List[ASAGraph], List[MAGNObjectNode]]:
        """
        Create an ASA graph from a table.

        :param table: the table
        :param primary_keys: the primary keys of said table
        :param foreign_keys: the foreign keys of said table
        """
        # First create the ASA graphs for primary keys
        data = table.reset_index().dropna()

        asa_graphs = []
        for p_key in primary_keys:
            asa = self._create_asa_graph(data, p_key)
            asa_graphs.append(asa)

        processed_cols = [f_key[0] for f_key in foreign_keys.values()] + primary_keys
        table_not_processed = data.drop(processed_cols, axis=1)

        for column_name in table_not_processed.columns:
            asa = self._create_asa_graph(table_not_processed, column_name)
            asa_graphs.append(asa)

        objects = self._create_magn_objects(asa_graphs, data, table_name, foreign_keys)

        return asa_graphs, objects

    @classmethod
    def _create_asa_graph(cls, table: pd.DataFrame, column_name: str) -> ASAGraph:
        column = table[column_name]
        asa_graph = ASAGraph(column_name)
        for value in column:
            asa_graph.insert(value, column_name)

        return asa_graph

    def _create_magn_objects(self, asa_graphs: List[ASAGraph], table: pd.DataFrame, table_name: str,
                             foreign_keys: Dict[str, Tuple[str, str]]) -> list[MAGNObjectNode]:
        objects = []
        fk_cols = [f_key for f_key in foreign_keys.values()]
        fk_names = [f_key[0] for f_key in foreign_keys.values()]

        for idx, row in table.iterrows():
            object_node = MAGNObjectNode(table_name)
            for column_name, value in row.items():
                if column_name in fk_names:
                    continue
                asa = self.get_first_asa_by_name(asa_graphs, str(column_name))
                element = asa.search(value)
                if element is None:
                    raise ValueError(f"Element {value} not found in the \"{column_name}\" ASA graph.")

                element.magn_objects.append(object_node)
                object_node.values.append(element)

            for fk_name, fk_foreign_name in fk_cols:
                fk_value = row[fk_name]
                self._add_object_foreign_keys(object_node, fk_foreign_name, fk_value)
            objects.append(object_node)

        return objects

    def _add_object_foreign_keys(self, object_node: MAGNObjectNode, fk_foreign_name: str, fk_value: int | float | str):
        asa = self.get_first_asa_by_name(self.asa_graphs, fk_foreign_name)
        element = asa.search(fk_value)
        if element is None:
            raise ValueError(f"Element {fk_value} not found in the \"{fk_foreign_name}\" ASA graph.")

        for obj in element.magn_objects:
            obj.objects.append(object_node)

    def _update_priorities(self, neurons: List[ASAElement], target_value: int | float | str, learning_rate: float):
        """
        Update the priorities of the neurons in the MAGN graph.

        :param neurons: Neurons to update
        :param target_value: the target value
        :param learning_rate: the learning rate
        """
        if isinstance(target_value, str):
            deltas = self._calc_delta_categorical(neurons, target_value)
        else:
            deltas = self._calc_delta_numerical(neurons, target_value)

        for neuron, delta in zip(neurons, deltas):
            if isinstance(neuron.key, str):  # TODO: REALLY BAD, no isinstance..
                neuron.priority *= (1 - learning_rate * delta)
            elif delta == 0.0:
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
            if not isinstance(neuron.key, str):  # TODO: REALLY BAD, no isinstance...
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
        return [
            ((value - min_value) / (max_value - min_value) if (max_value - min_value) != 0.0 else 0.0)
            for value in values
        ]

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

    @classmethod
    def get_first_asa_by_name(cls, asa_graphs: List[ASAGraph], name: str) -> ASAGraph:
        for asa_graph in asa_graphs:
            if asa_graph.name == name:
                return asa_graph
        raise ValueError(f"ASA graph with name {name} not found.")

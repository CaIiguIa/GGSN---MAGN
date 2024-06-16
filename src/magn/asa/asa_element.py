from typing import List

from magn.abstract_node import AbstractNode
from magn.magn_object_node import MAGNObjectNode


class ASAElement(AbstractNode):
    """
    A class representation of an element in ASA graph. An Element is a part of a node in the ASA graph.

    key:                    represents the unique identifier of the node in the ASA graph.
    feature:                name of the feature which value the ASAElement represents.
    key_duplicates:         integer that counts the number of duplicate keys. It is initially set to 1.
    bl_prev:                points to the previous node in the bidirectional linked list. It is initially set to None.
    bl_next:                points to the next node in the bidirectional linked list. It is initially set to None.
    magn_object:            list that stores the MAGN graph objects associated with the node.
    """

    def __init__(self, key: int | float | str, feature: str):
        if key is None:
            raise ValueError("Key cannot be None")
        self.key: int | float | str = key
        self.feature: str = feature
        self.key_duplicates: int = 1
        self.priority: float = 1.0

        # Bidirectional linked list
        self.bl_prev: ASAElement | None = None
        self.bl_next: ASAElement | None = None
        self.bl_prev_weight: float = 0.0
        self.bl_next_weight: float = 0.0

        # MAGN
        self.magn_objects: List[MAGNObjectNode] = []  # List of MAGN objects

    def magn_weight(self):
        """
        Calculate the weight of the connection between this element and MAGN object.
        :param self:
        :return: float, the weight of the connection between this element and MAGN object
        """
        return 1.0 / self.key_duplicates

    def neighbors(self) -> List[AbstractNode]:
        return self.magn_objects

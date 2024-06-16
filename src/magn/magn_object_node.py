from typing import List

from magn.abstract_node import AbstractNode


class MAGNObjectNode(AbstractNode):
    """
    A class representation of a node (object) in the MAGN graph.

    clazz:                  the class of the object. Table name in the database.
    duplicates:             integer that counts the number of duplicate objects. It is initially set to 1.
    priority:               currently unused. The priority of the object. It is initially set to 1.0.
    values:                 list that stores the values associated with the object.
    objects:                list that stores the objects associated with the object.
    """

    def __init__(self, clazz):
        self.clazz: str = clazz
        self.duplicates: int = 1
        self.priority: float = 1.0
        self.values: List[AbstractNode] = [] # ASAElements!
        self.objects: List[MAGNObjectNode] = []

    def neighbors(self) -> List[AbstractNode]:
        return self.objects + self.values

    def magn_weight(self):
        """
        Calculate the weight of the connection between this object and other MAGN object.
        :param self:
        :return: float, the weight of the connection between this object and other MAGN object.
        """
        return 1.0 / self.duplicates

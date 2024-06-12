class ASAElement:
    """
    A class representation of an element in ASA graph. An Element is a part of a node in the ASA graph.

    key:                    represents the unique identifier of the node in the ASA graph.
    key_duplicates:         integer that counts the number of duplicate keys. It is initially set to 1.
    bl_prev:                points to the previous node in the bidirectional linked list. It is initially set to None.
    bl_next:                points to the next node in the bidirectional linked list. It is initially set to None.
    magn_object:            list that stores the MAGN graph objects associated with the node.
    """

    def __init__(self, key):
        self.key: int | float | str = key
        self.key_duplicates: int = 1

        # Bidirectional linked list
        self.bl_prev: ASAElement | None = None
        self.bl_next: ASAElement | None = None
        self.bl_prev_weight: float | None = None
        self.bl_next_weight: float | None = None

        # MAGN
        self.magn_object = []  # TODO: maybe change this to a set/list of MAGN objects IDs

    def magn_weight(self):
        """
        Calculate the weight of the element in the MAGN graph.
        :param self:
        :return: float, the weight of the element in the MAGN graph
        """
        return 1.0 / self.key_duplicates

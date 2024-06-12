class MAGNObjectNode:
    """
    A class representation of a node (object) in the MAGN graph.

    clazz:                  the class of the object. Table name in the database.
    duplicates:             integer that counts the number of duplicate objects. It is initially set to 1.
    """

    def __init__(self, clazz):
        self.clazz: str = clazz
        self.duplicates: int = 1

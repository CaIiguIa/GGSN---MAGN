from typing import List

from src.asa.ASAElement import ASAElement


class ASANode:
    """
    A node in the ASA graph (Aggregative Sorting Associative graph).
    It can consist of 1 - 3 elements

    Attributes:
    elements:   list of elements in the node
    parent:     the parent node of the current node
    children:   list of children nodes of the current node
    """

    def __init__(self):
        self.elements: List[ASAElement] = []
        self.parent: ASANode | None = None
        self.children: List[ASANode] = []

    def search(self, key):
        """
        Search for an element in the node with the given key

        :param key: the key of the element to search for
        :return: the element with the given key if it exists, None otherwise
        """

        for element in self.elements:
            if element.key == key:
                return element
        return None

    def is_leaf(self) -> bool:
        """
        Check if the node is a leaf node

        :return: True if the node is a leaf node, False otherwise
        """

        return len(self.children) == 0

    def has_parent(self) -> bool:
        """
        Check if the node has a parent node

        :return: True if the node has a parent node, False otherwise
        """

        return self.parent is not None

    def left_child(self):
        """
        Get the leftmost child of the node

        :return: the leftmost child of the node
        """

        if self.children:
            return self.children[0]

        return None

    def right_child(self):
        """
        Get the rightmost child of the node

        :return: the rightmost child of the node
        """

        if self.children:
            return self.children[-1]

        return None

    def middle_child(self):
        """
        Get the middle child of the node

        :return: the middle child of the node
        """

        if len(self.children) != 3:
            raise ValueError("The node does not have 3 children")

        return self.children[1]

    def left_element(self):
        """
        Get the leftmost element of the node

        :return: the leftmost element of the node
        """

        if self.elements:
            return self.elements[0]

        return None

    def right_element(self):
        """
        Get the rightmost element of the node

        :return: the rightmost element of the node
        """

        if self.elements:
            return self.elements[-1]

        return None

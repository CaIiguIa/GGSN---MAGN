from typing import List

from src.magn.asa.ASAElement import ASAElement


class ASANode:
    """
    A node in the ASA graph (Aggregative Sorting Associative graph).
    It can consist of 1 - 3 elements

    Attributes:
    elements:   list of elements in the node
    parent:     the parent node of the current node
    children:   list of children nodes of the current node
    """

    def __init__(self, parent=None):
        self.elements: List[ASAElement] = []
        self.parent: ASANode | None = parent
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

    def keys(self):
        return [element.key for element in self.elements].sort()

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

    def middle_child(self, create=False):
        """
        Get the middle child of the node. Creates one if it does not exist and parameter "create" is True

        :return: the middle child of the node
        """

        if not create and len(self.children) != 3:
            raise ValueError("The node does not have 3 children")

        if create and len(self.children) == 1:
            new_node = ASANode(self)
            self.children.append(new_node)

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

    def insert_element(self, new_element: ASAElement):
        self.elements.append(new_element)
        self.elements.sort(key=lambda element: element.key)

    def insert_child(self, node: 'ASANode'):
        pass

    def remove_element(self, element_to_remove: ASAElement):
        self.elements = [element for element in self.elements if element.key != element_to_remove.key]

    def remove_child(self, node: 'ASANode'):
        self.children = [child for child in self.children if child.keys() != node.keys()]

    def split_into_two(self):
        """
        Splits the node into two. The node has to have exactly 2 elements to work

        :return: created nodes
        """
        if len(self.elements) != 2:
            raise ValueError("Node has to have 2 elements to be split")

        left_node = ASANode(self.parent)
        left_node.insert_element(self.elements[0])

        right_node = ASANode(self.parent)
        right_node.insert_element(self.elements[1])

        self.parent.remove_child(self)
        # TODO: take node's children and give them to left_node and right_node: split children with formula:
        # self.children[0: int((len(self.children)+1)/2)]
        self

from typing import List

import networkx as nx
import matplotlib.pyplot as plt

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
        Search for an element in the node with the given key. It does not search in the children nodes

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
        """
        Returns keys in the node in sorted order. It does not return keys of the children nodes
        """
        return sorted([element.key for element in self.elements])

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

        :param create: if True, creates a middle child if it does not exist

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
        Get the leftmost element of the node. It is the element with the smallest key in the node

        :return: the leftmost element of the node
        """

        if self.elements:
            return self.elements[0]

        return None

    def right_element(self):
        """
        Get the rightmost element of the node. It is the element with the biggest key in the node

        :return: the rightmost element of the node
        """

        if self.elements:
            return self.elements[-1]

        return None

    def insert_element(self, new_element: ASAElement):
        """
        Insert a new element to the node. The element is inserted in the correct (ascending) order

        :param new_element: the element to insert
        """
        self.elements.append(new_element)
        self.elements.sort(key=lambda element: element.key)

    def insert_child(self, node: 'ASANode'):
        """
        Inserts child node to the node in the correct order
        """
        n_children = len(self.children)
        if n_children == 3:
            raise ValueError("The node cannot have more than 3 children")

        if n_children == 0:
            self.children.append(node)
            return

        for n_children in range(n_children):
            if self.children[n_children].keys() > node.keys():
                self.children.insert(n_children, node)
                return

    def remove_element(self, element_to_remove: ASAElement):
        self.elements = [element for element in self.elements if element.key != element_to_remove.key]

    def remove_child(self, node: 'ASANode'):
        self.children = [child for child in self.children if child.keys() != node.keys()]

    def split_into_two(self):
        """
        Splits the node into two. The node needs to have exactly 2 elements to be split

        :return: created nodes
        """
        if len(self.elements) != 2:
            raise ValueError("Node needs to have 2 elements to be split")

        left_node = ASANode(self.parent)
        left_node.insert_element(self.elements[0])

        right_node = ASANode(self.parent)
        right_node.insert_element(self.elements[1])

        self.parent.remove_child(self)

        children_split_point = int((len(self.children) + 1) / 2)
        left_children = self.children[0: children_split_point]
        right_children = self.children[children_split_point:]

        for child in left_children:
            left_node.insert_child(child)
            child.parent = left_node

        for child in right_children:
            right_node.insert_child(child)
            child.parent = right_node

        self.parent = None
        self.children = []

        return left_node, right_node

    def id_keys(self):
        return ", ".join(map(str, self.keys()))

    def get_node_name(self, node: 'ASANode', depth: int):
        if depth == 0:
            return f"Root [{node.id_keys()}]"
        return f"C{depth} [{node.id_keys()}]"

    def plot_graph_node(self, graph: nx.Graph, depth):
        """
        Plot the ASA graph node. Does not plot the children nodes.
        """
        if self.parent:
            graph.add_edge(self.get_node_name(self.parent, depth - 1), self.get_node_name(self, depth))
        else:
            graph.add_node(self.get_node_name(self, depth))

        for child in self.children:
            child.plot_graph_node(graph, depth + 1)

import networkx as nx

from magn.asa.asa_element import ASAElement
from magn.asa.asa_node import ASANode


class ASAGraph:
    """
    An ASA graph

    Attributes:
    root:   the root node of the ASA graph
    sensor: the sensor that is associated with the ASA graph
    """

    def __init__(self, name: str):
        self.root: ASANode = ASANode()
        self.name = name
        # self.sensor = None

    def search(self, key: int | float | str) -> ASAElement | None:
        """
        Search for a node in the ASA graph with the given key

        :param key: the key of the element to search for
        :return: the element with the given key if it exists, None otherwise
        """

        node = self.root
        while True:
            element = node.search(key)
            if element:
                return element

            if node.is_leaf():
                return None

            if key < node.left_element().key:
                node = node.left_child()

            elif key > node.right_element().key:
                node = node.right_child()

            else:
                node = node.middle_child()

    def insert(self, key: int | float | str, feature_name: str):
        """
        Insert an element with the given key into the ASA graph

        :param feature_name:  the name of the feature that the element represents
        :param key: the key of the element to insert
        """

        node = self.root
        while True:
            element = node.search(key)
            if element is not None:
                element.key_duplicates += 1
                return

            if node.is_leaf():
                new_element = ASAElement(key, feature_name)
                self.insert_bl(new_element)
                node.insert_element(new_element)
                while node is not None and len(node.elements) > 2:
                    node = self.split_node(node)
                break

            elif key < node.left_element().key:
                node = node.left_child()

            elif key > node.right_element().key:
                node = node.right_child()

            else:
                node = node.middle_child()

        self.bl_fix_weights()

    def insert_bl(self, new_element: ASAElement):
        """
        Insert an element into the bidirectional linked list
        If the tree is empty, the element is not inserted as there is no need to update the pointers and their order

        :param new_element: the element to insert
        """

        if not self.root.elements:
            return

        current_element = self.leftmost_element()

        while new_element.key > current_element.key:
            if current_element.bl_next:
                current_element = current_element.bl_next
            else:
                current_element.bl_next = new_element
                new_element.bl_prev = current_element
                return

        if current_element.bl_prev:
            current_element.bl_prev.bl_next = new_element

        new_element.bl_prev = current_element.bl_prev
        new_element.bl_next = current_element
        current_element.bl_prev = new_element

    def leftmost_element(self) -> ASAElement:
        """
        Get the leftmost element in the ASA graph. It is the element with the smallest key

        :return: the leftmost element in the ASA graph
        """

        current_node = self.root
        while not current_node.is_leaf():
            current_node = current_node.left_child()

        return current_node.left_element()

    def rightmost_element(self) -> ASAElement:
        """
        Get the rightmost element in the ASA graph. It is the element with the biggest key

        :return: the rightmost element in the ASA graph
        """

        current_node = self.root
        while not current_node.is_leaf():
            current_node = current_node.right_child()

        return current_node.right_element()

    def min(self):
        """
        Returns element with minimal value in the tree
        """
        return self.leftmost_element()

    def max(self):
        """
        Returns element with maximal value in the tree
        """
        return self.rightmost_element()

    def print_bl(self):
        """
        Print the bidirectional linked list. It prints the elements in the tree in ascending order
        """
        print("(value|duplicates) --weight-- (value|duplicates) --weight-- ...")
        current_element = self.leftmost_element()

        while current_element:
            print(f"({current_element.key}|{current_element.key_duplicates})", end="")
            if current_element.bl_next:
                print(f" --{current_element.bl_next_weight}-- ", end="")
            current_element = current_element.bl_next

    def bl(self):
        """
        Returns the bidirectional linked list as a list
        """
        elements = []
        current_element = self.leftmost_element()
        while current_element:
            elements.append(current_element.key)
            current_element = current_element.bl_next
        return elements

    def split_node(self, node: ASANode):
        """
        Split the node if it has more 3 elements
        Throws an error if the node does not have 3 elements
        """
        if len(node.elements) != 3:
            raise ValueError("The node does not have 3 elements thus it cannot be split")

        # remove middle element from node
        middle_element = node.elements[1]
        node.remove_element(middle_element)

        if node.parent is None:
            new_parent = ASANode()
            self.root = new_parent
            new_parent.insert_element(middle_element)

            new_parent.insert_child(node)
            node.parent = new_parent

        else:
            node.parent.insert_element(middle_element)

        return node.split_into_two()

    def plot_graph(self):
        """
        Plot the ASA graph
        """
        graph = nx.DiGraph()
        self.root.plot_graph_node(graph, depth=0)
        nx.draw(graph, with_labels=True)

    def bl_fix_weights(self):
        """
        Fix the weights of the bidirectional linked list. Highly inefficient, but it works.
        """
        if isinstance(self.leftmost_element().key, str):
            return

        value_range = self.rightmost_element().key - self.leftmost_element().key

        current_element = self.leftmost_element()
        while current_element.bl_next:
            current_element.bl_next_weight = 1.0 - (current_element.bl_next.key - current_element.key) / value_range
            current_element = current_element.bl_next

            if current_element.bl_prev is not None:
                current_element.bl_prev_weight = current_element.bl_prev.bl_next_weight

    def sensor(self, value):
        if self.search(value) is None:
            raise ValueError(f"Value: {value} not found in the ASA Graph")

    def get_elements(self):
        """
        Get all elements in the ASA graph
        """
        elements = []
        current_element = self.leftmost_element()
        while current_element:
            elements.append(current_element)
            current_element = current_element.bl_next
        return elements

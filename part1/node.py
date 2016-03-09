"""
Assignment Part 3 - Graph Implementation
"""
import random

class GraphNode(object):
    """
    Initialization of basic GaphNode
    """
    def __init__(self, name, counter=0):
        self.counter = counter
        self.node_list = []
        self.name = name

    def print_node(self):
        """
        Printing node name
        """
        print self.name

    def add_node(self, node):
        """
        Adding child node in to given node
        """
        self.node_list.append(node)

    def get_node_list(self):
        """
        Return list of connected nodes in given node.
        """
        return self.node_list

def visit_node(node):
    """
    Visiting of node based on the requirement given.
    """
    node.print_node()
    if len(node.get_node_list()) == 0:
        return
    else:
        random_val = random.randrange(0, len(node.get_node_list()))
        visit_node(node.get_node_list()[random_val])

if __name__ == "__main__":
    START_NODE = GraphNode("START", 10)
    FIRST_NODE = GraphNode("Node 1")
    SECOND_NODE = GraphNode("Node 2")
    THIRD_NODE = GraphNode("Node 3")
    STOP_NODE = GraphNode("STOP")
    START_NODE.add_node(FIRST_NODE)
    FIRST_NODE.add_node(SECOND_NODE)
    FIRST_NODE.add_node(THIRD_NODE)
    SECOND_NODE.add_node(THIRD_NODE)
    SECOND_NODE.add_node(FIRST_NODE)
    THIRD_NODE.add_node(STOP_NODE)
    visit_node(START_NODE)

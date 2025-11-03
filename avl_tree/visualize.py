"""
Visualization helpers using graphviz. Produces a graph where each node label contains:
    value
    height
    balance factor

Nodes with |balance| > 1 are colored red; else green.
"""

from typing import Optional
from graphviz import Digraph, Source
from .node import Node

def _node_label(node: Node, balance: int) -> str:
    # Label shows value, height, balance
    return f"{node.value}\\n(h={node.height}, b={balance})"

def _add_nodes_edges(dot: Digraph, node: Optional[Node]):
    if not node:
        return
    balance = (node.left.height if node.left else 0) - (node.right.height if node.right else 0)
    color = "red" if abs(balance) > 1 else "green"
    dot.node(str(id(node)), _node_label(node, balance), color=color, style="filled", fillcolor="white", fontcolor=color)
    if node.left:
        dot.edge(str(id(node)), str(id(node.left)))
        _add_nodes_edges(dot, node.left)
    if node.right:
        dot.edge(str(id(node)), str(id(node.right)))
        _add_nodes_edges(dot, node.right)

def tree_to_graphviz(root: Optional[Node], highlight_node: Optional[int] = None) -> Source:
    dot = Digraph(format="svg")
    dot.attr('node', shape='circle')
    if not root:
        dot.node("empty", "Empty")
    else:
        _add_nodes_edges(dot, root)
    return Source(dot.source)

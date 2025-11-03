"""
AVL Tree implementation with insert, delete, search, rotations and step logging.
Each public operation returns a dict with:
- 'logs': list[str] textual logs
- 'steps': list[ { desc: str, graph: graphviz.Source } ] snapshots for step-by-step mode
"""

from __future__ import annotations
from typing import Optional, List, Dict, Any
from .node import Node
from .visualize import tree_to_graphviz
import copy

class AVLTree:
    def __init__(self):
        self.root: Optional[Node] = None
        self.last_action: str | None = None

    
    # Helper functions
    
    def get_height(self, node: Optional[Node]) -> int:
        return node.height if node else 0

    def update_height(self, node: Node):
        node.height = 1 + max(self.get_height(node.left), self.get_height(node.right))

    def get_balance(self, node: Optional[Node]) -> int:
        if not node:
            return 0
        return self.get_height(node.left) - self.get_height(node.right)

    def count_nodes(self) -> int:
        def _count(n):
            return 0 if not n else 1 + _count(n.left) + _count(n.right)
        return _count(self.root)

    
    # Rotations
    
    def right_rotate(self, y: Node) -> Node:
        x = y.left
        T2 = x.right

        # Rotation
        x.right = y
        y.left = T2

        # Update heights
        self.update_height(y)
        self.update_height(x)

        return x

    def left_rotate(self, x: Node) -> Node:
        y = x.right
        T2 = y.left

        # Rotation
        y.left = x
        x.right = T2

        # Update heights
        self.update_height(x)
        self.update_height(y)

        return y

    
    # Insert (public wrapper)
    
    def insert(self, key: int) -> Dict[str, Any]:
        logs: List[str] = []
        steps: List[Dict[str, Any]] = []

        logs.append(f"Insert {key}")
        self.last_action = f"Insert {key}"

        # inner recursive insertion that returns new root
        def _insert(node: Optional[Node], key: int) -> Node:
            if not node:
                n = Node(key)
                logs.append(f"Created node {key}")
                steps.append(self._snapshot(f"Inserted {key}", None))
                return n
            if key < node.value:
                node.left = _insert(node.left, key)
            elif key > node.value:
                node.right = _insert(node.right, key)
            else:
                logs.append(f"Key {key} already present; ignoring.")
                return node

            # update height and get balance
            self.update_height(node)
            balance = self.get_balance(node)
            logs.append(f"At node {node.value}: height={node.height}, balance={balance}")

            # LL Case (left-left) -> Right rotate
            if balance > 1 and key < node.left.value:
                logs.append(f"Right Rotation (LL) at node {node.value}")
                steps.append(self._snapshot(f"LL case before rotation at {node.value}", node))
                node = self.right_rotate(node)
                steps.append(self._snapshot(f"After Right Rotation at {node.value}", node))
                return node

            # RR Case (right-right) -> Left rotate
            if balance < -1 and key > node.right.value:
                logs.append(f"Left Rotation (RR) at node {node.value}")
                steps.append(self._snapshot(f"RR case before rotation at {node.value}", node))
                node = self.left_rotate(node)
                steps.append(self._snapshot(f"After Left Rotation at {node.value}", node))
                return node

            # LR Case (left-right): left child left-rotate then node right-rotate
            if balance > 1 and key > node.left.value:
                logs.append(f"Left-Right Rotation (LR) at node {node.value}")
                steps.append(self._snapshot(f"LR case before rotations at {node.value}", node))
                node.left = self.left_rotate(node.left)
                steps.append(self._snapshot(f"After left-rotation of left child of {node.value}", node))
                node = self.right_rotate(node)
                steps.append(self._snapshot(f"After right-rotation at {node.value}", node))
                return node

            # RL Case (right-left): right child right-rotate then node left-rotate
            if balance < -1 and key < node.right.value:
                logs.append(f"Right-Left Rotation (RL) at node {node.value}")
                steps.append(self._snapshot(f"RL case before rotations at {node.value}", node))
                node.right = self.right_rotate(node.right)
                steps.append(self._snapshot(f"After right-rotation of right child of {node.value}", node))
                node = self.left_rotate(node)
                steps.append(self._snapshot(f"After left-rotation at {node.value}", node))
                return node

            return node

        self.root = _insert(self.root, key)
        return {"logs": logs, "steps": steps}

    
    # Find minimum node (used in delete)
    
    def _min_value_node(self, node: Node) -> Node:
        current = node
        while current.left:
            current = current.left
        return current

    
    # Delete (public wrapper)
    
    def delete(self, key: int) -> Dict[str, Any]:
        logs: List[str] = []
        steps: List[Dict[str, Any]] = []

        logs.append(f"Delete {key}")
        self.last_action = f"Delete {key}"

        def _delete(node: Optional[Node], key: int) -> Optional[Node]:
            if not node:
                logs.append(f"Key {key} not found.")
                return None
            if key < node.value:
                node.left = _delete(node.left, key)
            elif key > node.value:
                node.right = _delete(node.right, key)
            else:
                # this is the node to be deleted
                logs.append(f"Found node {node.value} for deletion")
                steps.append(self._snapshot(f"Deleting {node.value}", node))
                if not node.left:
                    temp = node.right
                    logs.append(f"Node {node.value} has no left child, replace with right child")
                    return temp
                elif not node.right:
                    temp = node.left
                    logs.append(f"Node {node.value} has no right child, replace with left child")
                    return temp
                else:
                    # Node with two children: get inorder successor
                    temp = self._min_value_node(node.right)
                    logs.append(f"In-order successor is {temp.value}")
                    node.value = temp.value
                    node.right = _delete(node.right, temp.value)

            if not node:
                return None

            # update height and rebalance
            self.update_height(node)
            balance = self.get_balance(node)
            logs.append(f"At node {node.value}: height={node.height}, balance={balance}")

            # Balancing after deletion (same cases but with checks)
            # LL
            if balance > 1 and self.get_balance(node.left) >= 0:
                logs.append(f"Right Rotation (LL) at node {node.value}")
                steps.append(self._snapshot(f"LL rebalance before at {node.value}", node))
                node = self.right_rotate(node)
                steps.append(self._snapshot(f"After Right Rotation at {node.value}", node))
                return node

            # LR
            if balance > 1 and self.get_balance(node.left) < 0:
                logs.append(f"Left-Right Rotation (LR) at node {node.value}")
                steps.append(self._snapshot(f"LR rebalance before at {node.value}", node))
                node.left = self.left_rotate(node.left)
                steps.append(self._snapshot(f"After left-rotation of left child of {node.value}", node))
                node = self.right_rotate(node)
                steps.append(self._snapshot(f"After right-rotation at {node.value}", node))
                return node

            # RR
            if balance < -1 and self.get_balance(node.right) <= 0:
                logs.append(f"Left Rotation (RR) at node {node.value}")
                steps.append(self._snapshot(f"RR rebalance before at {node.value}", node))
                node = self.left_rotate(node)
                steps.append(self._snapshot(f"After Left Rotation at {node.value}", node))
                return node

            # RL
            if balance < -1 and self.get_balance(node.right) > 0:
                logs.append(f"Right-Left Rotation (RL) at node {node.value}")
                steps.append(self._snapshot(f"RL rebalance before at {node.value}", node))
                node.right = self.right_rotate(node.right)
                steps.append(self._snapshot(f"After right-rotation of right child of {node.value}", node))
                node = self.left_rotate(node)
                steps.append(self._snapshot(f"After left-rotation at {node.value}", node))
                return node

            return node

        self.root = _delete(self.root, key)
        return {"logs": logs, "steps": steps}

    
    # Search
    
    def search(self, key: int) -> bool:
        def _search(node: Optional[Node], key: int) -> bool:
            if not node:
                return False
            if key == node.value:
                return True
            elif key < node.value:
                return _search(node.left, key)
            else:
                return _search(node.right, key)
        return _search(self.root, key)

    
    # Snapshot helper for educational steps
    
    def _snapshot(self, desc: str, node: Optional[Node]):
        """
        Returns a dict with description and a graphviz.Source snapshot.
        We deep-copy the tree to avoid later mutations affecting saved snapshots.
        """
        # To prevent referencing the same objects, create a deep copy of the current root
        root_copy = copy.deepcopy(self.root)
        graph = tree_to_graphviz(root_copy, highlight_node=(node.value if node else None))
        return {"desc": desc, "graph": graph}

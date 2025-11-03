from __future__ import annotations
from dataclasses import dataclass
from typing import Optional

@dataclass
class Node:
    value: int
    left: Optional["Node"] = None
    right: Optional["Node"] = None
    height: int = 1  # leaf has height 1

    def __repr__(self):
        return f"Node({self.value}, h={self.height})"

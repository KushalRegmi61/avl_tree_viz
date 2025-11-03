"""
Helper utilities: pseudocode generator, color utilities, and small helpers.
"""

from typing import Optional

def pseudocode_for_last_action(action: Optional[str]) -> str:
    """
    Returns a small pseudocode/explanation based on the last action string.
    Keeps explanations concise and educational.
    """
    if not action:
        return "No actions yet."

    if action.startswith("Insert"):
        return (
            "Insert(key):\n"
            "1. Perform BST insert.\n"
            "2. Update heights moving up.\n"
            "3. Compute balance = height(left) - height(right).\n"
            "4. If balance > 1 and key < left.value -> Right rotate (LL).\n"
            "   If balance < -1 and key > right.value -> Left rotate (RR).\n"
            "   If balance > 1 and key > left.value -> Left-then-Right (LR).\n"
            "   If balance < -1 and key < right.value -> Right-then-Left (RL).\n"
            "5. Update heights after rotations.\n"
        )

    if action.startswith("Delete"):
        return (
            "Delete(key):\n"
            "1. Perform BST delete.\n"
            "2. If node had two children, replace with in-order successor.\n"
            "3. Update heights moving up.\n"
            "4. Rebalance similarly to insert using balance factors.\n"
        )

    return f"Action: {action}\nNo detailed pseudocode available."

"""
app.py
Streamlit entrypoint for the AVL Tree Visualizer.

Purpose:
- Interactive educational AVL Tree visualizer using Streamlit + Graphviz.
- Supports insert, delete, search, clear, and step-by-step educational mode.
- Shows node value, height, balance factor, colors imbalanced nodes red, logs each operation and rotation.

How to run:
    pip install streamlit graphviz
    streamlit run app.py

Module interaction:
- avl_tree.node -> Node dataclass (value, left, right, height)
- avl_tree.avl  -> AVLTree class: insert, delete, search, rotations, step generator
- avl_tree.visualize -> Graphviz rendering utilities
- utils.helpers -> logging & pseudocode helpers

Author: Fixed rerun logic to avoid Streamlit experimental_rerun() errors.
"""

from typing import Optional, Any, Dict
import streamlit as st
from avl_tree.avl import AVLTree
from avl_tree.visualize import tree_to_graphviz
from utils.helpers import pseudocode_for_last_action

# Page config
st.set_page_config(page_title="AVL Tree Visualizer 🌳", layout="wide")


# Session state defaults

if "avl" not in st.session_state:
    st.session_state.avl = AVLTree()

if "logs" not in st.session_state:
    st.session_state.logs = []

if "step_mode" not in st.session_state:
    st.session_state.step_mode = False

if "steps" not in st.session_state:
    st.session_state.steps = []

if "step_index" not in st.session_state:
    st.session_state.step_index = 0

# New flag to coordinate a single safe rerun
if "should_rerun" not in st.session_state:
    st.session_state.should_rerun = False

avl: AVLTree = st.session_state.avl

#  UI layout 
st.title("AVL Tree Visualizer 🌳")
col1, col2 = st.columns([2, 3])

with col1:
    st.subheader("Controls")
    value = st.text_input("Value (integers only)", key="value_input")
    insert_btn = st.button("Insert")
    delete_btn = st.button("Delete")
    search_btn = st.button("Search")
    clear_btn = st.button("Clear Tree")
    # Keep step_mode checkbox in sync with session_state.step_mode
    step_mode_checkbox = st.checkbox(
        "Step-by-step educational mode",
        value=st.session_state.step_mode,
        key="step_mode_checkbox",
    )
    # When checkbox toggles, update the session_state step_mode and ensure UI refresh
    if step_mode_checkbox != st.session_state.step_mode:
        st.session_state.step_mode = step_mode_checkbox
        st.session_state.should_rerun = True

    st.markdown("---")
    st.subheader("AVL Stats")
    try:
        nodes_count = avl.count_nodes()
        tree_height = avl.get_height(avl.root)
    except Exception:
        nodes_count = 0
        tree_height = 0
    st.write(f"Nodes: {nodes_count}")
    st.write(f"Height: {tree_height}")

    st.markdown("---")
    st.subheader("Educational")
    with st.expander("How AVL balancing works (brief)"):
        st.write(
            """
        - AVL maintains |balance factor| ≤ 1 for every node.
        - Balance factor = height(left) - height(right).
        - Rotations:
            - LL (Right rotation)
            - RR (Left rotation)
            - LR (Left-Right rotation): left child left-rotates, then node right-rotates.
            - RL (Right-Left rotation): right child right-rotates, then node left-rotates.
        """
        )

with col2:
    st.subheader("Tree Visualization")
    try:
        graph = tree_to_graphviz(avl.root)
        # Graphviz Source -> st.graphviz_chart accepts source string
        st.graphviz_chart(graph.source)
    except Exception as e:
        st.error(f"Visualization error: {e}")

    st.subheader("Operation Log")
    # show most recent first
    for log in reversed(st.session_state.logs[-200:]):
        st.write(log)

    st.markdown("---")
    st.subheader("Pseudocode / Explanation")
    last_action = getattr(avl, "last_action", None) or "No actions yet."
    st.code(pseudocode_for_last_action(last_action), language="text")


#  Helper functions 
def add_log(msg: str) -> None:
    st.session_state.logs.append(msg)


def push_steps(steps: list) -> None:
    st.session_state.steps = steps
    st.session_state.step_index = 0



# Button handlers (set should_rerun flag, don't call experimental_rerun directly)

if insert_btn:
    # Insert operation
    try:
        v = int(value)
    except Exception:
        st.error("Please enter an integer to insert.")
    else:
        result: Dict[str, Any] = avl.insert(v)
        for msg in result.get("logs", []):
            add_log(msg)
        # store snapshots for step mode if requested
        if st.session_state.step_mode:
            push_steps(result.get("steps", []))
        # update session avl (redundant but explicit)
        st.session_state.avl = avl
        st.session_state.should_rerun = True

if delete_btn:
    try:
        v = int(value)
    except Exception:
        st.error("Please enter an integer to delete.")
    else:
        result: Dict[str, Any] = avl.delete(v)
        for msg in result.get("logs", []):
            add_log(msg)
        if st.session_state.step_mode:
            push_steps(result.get("steps", []))
        st.session_state.avl = avl
        st.session_state.should_rerun = True

if search_btn:
    try:
        v = int(value)
    except Exception:
        st.error("Please enter an integer to search.")
    else:
        found = avl.search(v)
        add_log(f"Search {v}: {'Found' if found else 'Not found'}")
        st.session_state.avl = avl
        st.session_state.should_rerun = True

if clear_btn:
    st.session_state.avl = AVLTree()
    st.session_state.logs.append("Cleared tree")
    st.session_state.should_rerun = True


# Step-by-step controls (previous / next). Use separate buttons so they can be clicked.
if st.session_state.step_mode and st.session_state.steps:
    st.markdown("---")
    st.subheader("Step-by-step Playback")
    step_idx = st.session_state.step_index
    total = len(st.session_state.steps)
    # Guard against out-of-range step_idx
    if step_idx < 0:
        step_idx = 0
        st.session_state.step_index = 0
    if step_idx >= total:
        step_idx = max(0, total - 1)
        st.session_state.step_index = step_idx

    st.write(f"Step {step_idx + 1} / {total}")
    st.write(st.session_state.steps[step_idx]["desc"])
    # Render snapshot graph for this step
    try:
        st.graphviz_chart(st.session_state.steps[step_idx]["graph"].source)
    except Exception as e:
        st.error(f"Step visualization error: {e}")

    prev_btn = st.button("Previous Step")
    next_btn = st.button("Next Step")

    if prev_btn and step_idx > 0:
        st.session_state.step_index = step_idx - 1
        st.session_state.should_rerun = True

    if next_btn and step_idx < total - 1:
        st.session_state.step_index = step_idx + 1
        st.session_state.should_rerun = True



# Single safe rerun point

# If any handler above set `should_rerun = True`, perform exactly one rerun and reset the flag.
if st.session_state.get("should_rerun", False):
    # reset first to avoid potential rerun-loop if something else sets it again
    st.session_state.should_rerun = False
    st.rerun()

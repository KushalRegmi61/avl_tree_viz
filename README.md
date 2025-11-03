
# AVL Tree Visualizer

An interactive Streamlit app to visualize **AVL Trees**.  
Supports **insert**, **delete**, **search**, and **clear** operations with **automatic balancing** (LL, RR, LR, RL rotations) and step-by-step explanations.

---

## Overview

This app is an educational tool for learning **self-balancing binary search trees (AVL Trees)**.  
It uses **Streamlit** for the interface and **Graphviz** for dynamic tree visualization, showing node values, heights, and balance factors.

---

## Live Demo

Access the live demo here:  [Streamlit AVL Tree Visualizer](YOUR_LIVE_DEMO_LINK_HERE)

---

## Features

- Insert, Delete, Search, and Clear nodes
- Automatic AVL balancing with rotations:
  - LL (Right Rotation)
  - RR (Left Rotation)
  - LR (Left-Right Rotation)
  - RL (Right-Left Rotation)
- Step-by-step educational mode
- Operation log showing all actions
- Pseudocode panel explaining the last operation
- Nodes colored by balance status (balanced vs imbalanced)

---

## Project Structure

```

avl_tree_visualizer/
├── app.py                  # Streamlit entrypoint
├── avl_tree/
│   ├──__init__.py
│   ├── node.py             # Node dataclass
│   ├── avl.py              # AVLTree class with rotations
│   └── visualize.py        # Graphviz rendering utilities
├── utils/
│   └── helpers.py          # Logging and pseudocode utilities
└── README.md

````

---

## Installation

1. Clone the repository:
```bash
git clone https://github.com/kushalregmi61/avl_tree_viz.git
cd avl-tree-visualizer
````

2. Create and activate a virtual environment:

```bash
python -m venv .venv
source .venv/bin/activate      # Linux/macOS
.venv\Scripts\activate         # Windows
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

4. Run the app:

```bash
streamlit run app.py
```

---

## Modules

| Module               | Description                                              |
| -------------------- | -------------------------------------------------------- |
| `avl_tree.node`      | Node class with value, left, right, and height           |
| `avl_tree.avl`       | AVLTree class with insert, delete, search, and rotations |
| `avl_tree.visualize` | Convert AVL tree to Graphviz visualization               |
| `utils.helpers`      | Pseudocode and logging utilities                         |
| `app.py`             | Streamlit interface integrating all modules              |

---



## License

```
MIT License. Free to use for educational and research purposes.
```



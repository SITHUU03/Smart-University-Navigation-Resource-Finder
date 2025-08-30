import tkinter as tk
from tkinter import ttk

# Optional data structure (kept for reference/future use)
class TreeNode:
    def init(self, name):
        self.name = name
        self.children = []

    def add_child(self, child):
        self.children.append(child)

    def display(self, level=0):
        print("  " * level + f"- {self.name}")
        for child in self.children:
            child.display(level + 1)


# Hierarchical data used by the GUI Treeview
university_structure = {
    "Faculty of Computing": {
        "Department of Software Engineering": [
            "Data Structures & Algorithms",
            "Web Development",
            "Database Systems",
        ],
        "Department of Information Systems": [
            "Business Information Systems",
            "Enterprise Systems",
        ],
    },
    "Faculty of Engineering": {
        "Department of Civil Engineering": [
            "Structural Analysis",
            "Transportation Engineering",
        ],
        "Department of Electrical Engineering": [
            "Circuit Theory",
            "Power Systems",
        ],
    },
    "Faculty of Science": {
        "Department of Mathematics": [
            "Calculus",
            "Linear Algebra",
        ],
        "Department of Physics": [
            "Quantum Mechanics",
            "Classical Mechanics",
        ],
    },
}


def build_resource_tree(parent):
    """Create a Treeview widget displaying university resources.
    Returns the Treeview (unpacked) so the caller can place it in the layout.
    """
    tree = ttk.Treeview(parent, columns=("Type",), show="tree headings", height=20)

    # Style for better look
    style = ttk.Style()
    style.configure("Treeview", font=("Arial", 11), rowheight=25)
    style.configure("Treeview.Heading", font=("Arial", 12, "bold"))

    # Add a heading
    tree.heading("#0", text="University Resources", anchor="w")

    # Insert root node
    root_node = tree.insert("", "end", text="Smart University", open=True)

    # Populate the tree
    for faculty, departments in university_structure.items():
        faculty_id = tree.insert(root_node, "end", text=faculty, open=False)
        for dept, courses in departments.items():
            dept_id = tree.insert(faculty_id, "end", text=dept, open=False)
            for course in courses:
                tree.insert(dept_id, "end", text=course, open=False)

    return tree
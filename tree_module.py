# tree_module.py

# Node class for Tree
class TreeNode:
    def __init__(self, name):
        self.name = name
        self.children = []

    def add_child(self, child):
        self.children.append(child)

    def display(self, level=0):
        print("   " * level + "- " + self.name)
        for child in self.children:
            child.display(level + 1)

# Example: University Resource Hierarchy
def build_university_tree():
    root = TreeNode("University")

    # Faculty of Computing
    computing = TreeNode("Faculty of Computing")
    computing.add_child(TreeNode("BSc in Software Engineering"))
    computing.add_child(TreeNode("BSc in Data Science"))

    # Faculty of Business
    business = TreeNode("Faculty of Business")
    business.add_child(TreeNode("BBA in Marketing"))
    business.add_child(TreeNode("BBA in HR"))

    root.add_child(computing)
    root.add_child(business)

    return root

if __name__ == "__main__":
    university_tree = build_university_tree()
    print("📘 University Resources:")
    university_tree.display()

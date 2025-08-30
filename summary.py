from tabulate import tabulate

def print_summary():
    data = [
        [1, "Navigation", "Graph", "Start & Destination", "Shortest path"],
        [2, "Resource Management", "Tree", "Faculty, Dept, Courses", "Hierarchical listing"],
        [3, "History/Events", "Linked List", "Recently visited items", "Ordered history"],
        [4, "Integration & Interface", "(All modules)", "User commands", "Unified system output"]
    ]
    headers = ["Member", "Module", "Data Structure", "Input", "Output"]
    print(tabulate(data, headers=headers, tablefmt="grid"))

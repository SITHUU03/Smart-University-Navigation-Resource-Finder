# linked_history.py
class Node:
    def __init__(self, data):
        self.data = data
        self.next = None

class LinkedHistory:
    def __init__(self, max_entries=None):
        self.head = None
        self.tail = None
        self.max_entries = max_entries
        self.size = 0

    def add(self, item):
        """Add new history entry at the end."""
        new_node = Node(item)
        if not self.head:
            self.head = self.tail = new_node
        else:
            self.tail.next = new_node
            self.tail = new_node

        self.size += 1

        # Maintain max_entries
        if self.max_entries and self.size > self.max_entries:
            self.head = self.head.next
            self.size -= 1

    def get_all(self):
        """Return all history entries as a list."""
        result = []
        current = self.head
        while current:
            result.append(current.data)
            current = current.next
        return result

    def clear(self):
        self.head = self.tail = None
        self.size = 0

    def search(self, keyword):
        result = []
        current = self.head
        while current:
            if keyword.lower() in current.data.lower():
                result.append(current.data)
            current = current.next
        return result

    def export_to_file(self, filename):
        with open(filename, "w") as f:
            current = self.head
            while current:
                f.write(current.data + "\n")
                current = current.next

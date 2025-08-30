# navigation.py 
import heapq

class Navigation:
    def __init__(self):
        self.graph = {
            "Main Gate": [("Library", 200), ("Admin Block", 150)],
            "Library": [("Main Gate", 200), ("Canteen", 100), ("Engineering Faculty", 250)],
            "Admin Block": [("Main Gate", 150), ("Auditorium", 300)],
            "Canteen": [("Library", 100), ("Hostel", 400)],
            "Engineering Faculty": [("Library", 250), ("IT Faculty", 200)],
            "IT Faculty": [("Engineering Faculty", 200), ("Science Faculty", 350)],
            "Science Faculty": [("IT Faculty", 350), ("Auditorium", 300)],
            "Auditorium": [("Admin Block", 300), ("Science Faculty", 300)],
            "Hostel": [("Canteen", 400)]
        }

    def shortest_path(self, start, destination):
        if start not in self.graph or destination not in self.graph:
            return None, float("inf")

        distances = {node: float("inf") for node in self.graph}
        distances[start] = 0
        pq = [(0, start)]
        prev = {}

        while pq:
            current_distance, current_node = heapq.heappop(pq)
            if current_distance > distances[current_node]:
                continue
            for neighbor, weight in self.graph[current_node]:
                distance = current_distance + weight
                if distance < distances[neighbor]:
                    distances[neighbor] = distance
                    prev[neighbor] = current_node
                    heapq.heappush(pq, (distance, neighbor))

        # Reconstruct path
        path = []
        node = destination
        while node in prev:
            path.insert(0, node)
            node = prev[node]
        if path:
            path.insert(0, start)
        return path, distances[destination]

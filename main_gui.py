# main_gui.py
import tkinter as tk
from tkinter import ttk, messagebox, filedialog, simpledialog
from navigation import Navigation
from map_visualization import draw_campus
import calendar
from datetime import datetime

# ---------------- Linked List for History/Events ----------------
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
        new_node = Node(item)
        if not self.head:
            self.head = self.tail = new_node
        else:
            self.tail.next = new_node
            self.tail = new_node
        self.size += 1
        if self.max_entries and self.size > self.max_entries:
            self.head = self.head.next
            self.size -= 1

    def get_all(self):
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

# ---------------- Resource Management ----------------
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
    tree = ttk.Treeview(parent, columns=("Type",), show="tree headings", height=20)
    style = ttk.Style()
    style.configure("Treeview", font=("Segoe UI", 11), rowheight=25)
    style.configure("Treeview.Heading", font=("Segoe UI", 12, "bold"))

    tree.heading("#0", text="University Resources", anchor="w")
    root_node = tree.insert("", "end", text="Smart University", open=True)

    for faculty, departments in university_structure.items():
        faculty_id = tree.insert(root_node, "end", text=faculty, open=False)
        for dept, courses in departments.items():
            dept_id = tree.insert(faculty_id, "end", text=dept, open=False)
            for course in courses:
                tree.insert(dept_id, "end", text=course, open=False)

    return tree

# ---------------- Main GUI ----------------
class UniversityApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Smart University App")
        self.root.geometry("1000x700")
        self.root.configure(bg="#F5F5F5")

        self.notebook = ttk.Notebook(root)
        self.notebook.pack(fill="both", expand=True)

        self.nav = Navigation()
        self.history = LinkedHistory(max_entries=100)
        self.events = LinkedHistory(max_entries=100)

        # ---------------- Sample Events ----------------
        sample_events = [
            "Orientation Day - 2025-09-01",
            "Guest Lecture: AI in Modern Software - 2025-09-10",
            "Workshop: Database Systems - 2025-09-15",
            "Sports Meet - 2025-09-20",
            "Annual Cultural Festival - 2025-09-25",
            "Hackathon: Smart Campus Solutions - 2025-09-30"
        ]
        for event in sample_events:
            self.events.add(event)

        # Button style
        style = ttk.Style()
        style.configure(
            "Rounded.TButton",
            font=("Segoe UI", 11),
            padding=8,
            foreground="#000000",
            background="#6D4C41",
        )
        style.map(
            "Rounded.TButton",
            background=[("active", "#8D6E63")],
            foreground=[("active", "#333333")]
        )

        self.create_navigation_tab()
        self.create_resources_tab()
        self.create_history_tab()
        self.create_event_tab()
        self.refresh_event_tab()

    # ---------------- Navigation Tab ----------------
    def create_navigation_tab(self):
        nav_frame = tk.Frame(self.notebook, bg="#F5F5F5")
        self.notebook.add(nav_frame, text="Navigation")
        tk.Label(nav_frame, text="Navigation", font=("Segoe UI", 16, "bold"), bg="#F5F5F5").pack(pady=10)
        tk.Label(nav_frame, text="Select Start Location:", font=("Segoe UI", 12), bg="#F5F5F5").pack(pady=5)
        self.start_var = tk.StringVar()
        self.start_cb = ttk.Combobox(nav_frame, textvariable=self.start_var, values=list(self.nav.graph.keys()))
        self.start_cb.pack(pady=5)
        tk.Label(nav_frame, text="Select Destination:", font=("Segoe UI", 12), bg="#F5F5F5").pack(pady=5)
        self.end_var = tk.StringVar()
        self.end_cb = ttk.Combobox(nav_frame, textvariable=self.end_var, values=list(self.nav.graph.keys()))
        self.end_cb.pack(pady=5)
        btns = tk.Frame(nav_frame, bg="#F5F5F5")
        btns.pack(pady=10)
        ttk.Button(btns, text="Find Path", style="Rounded.TButton", command=self.find_path).grid(row=0, column=0, padx=5)
        ttk.Button(btns, text="Show Map", style="Rounded.TButton", command=self.show_map_only).grid(row=0, column=1, padx=5)
        ttk.Button(btns, text="Show Path", style="Rounded.TButton", command=self.show_map_with_path).grid(row=0, column=2, padx=5)
        self.nav_result = tk.Text(nav_frame, height=8, width=70, wrap="word",
                                  bg="#FFFFFF", fg="#333333", font=("Segoe UI", 11), relief="solid", bd=1)
        self.nav_result.pack(pady=10)

    def find_path(self):
        start, end = self.start_var.get(), self.end_var.get()
        if not start or not end:
            messagebox.showerror("Error", "Please select both start and destination.")
            return
        path, dist = self.nav.shortest_path(start, end)
        if path:
            result = f"Shortest Path from {start} to {end}:\n{' -> '.join(path)}\nDistance: {dist} meters"
            self.nav_result.delete("1.0", tk.END)
            self.nav_result.insert(tk.END, result)
            self.last_path = path
            self.history.add(f"Path {start} -> {end}")
            self.refresh_history_tab()
        else:
            messagebox.showerror("Error", "Invalid path selected.")

    def show_map_only(self):
        try:
            draw_campus(self.nav.graph)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to draw map: {e}")

    def show_map_with_path(self):
        path = getattr(self, "last_path", None)
        if not path or len(path) < 2:
            messagebox.showinfo("Info", "Find a path first.")
            return
        try:
            draw_campus(self.nav.graph, path=path)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to draw map: {e}")

    # ---------------- Resources Tab ----------------
    def create_resources_tab(self):
        res_frame = tk.Frame(self.notebook, bg="#F5F5F5")
        self.notebook.add(res_frame, text="Resources")
        tree = build_resource_tree(res_frame)
        scrollbar = ttk.Scrollbar(res_frame, orient="vertical", command=tree.yview)
        tree.configure(yscroll=scrollbar.set)
        tree.pack(side="left", fill="both", expand=True, padx=10, pady=10)
        scrollbar.pack(side="right", fill="y")

    # ---------------- History Tab ----------------
    def create_history_tab(self):
        hist_frame = tk.Frame(self.notebook, bg="#F5F5F5")
        self.notebook.add(hist_frame, text="History")
        self.history_box = tk.Listbox(hist_frame, height=20, width=70,
                                      font=("Segoe UI", 11), bg="#FFFFFF", fg="#333333", bd=1, relief="solid")
        self.history_box.pack(padx=10, pady=10)
        btn_frame = tk.Frame(hist_frame, bg="#F5F5F5")
        btn_frame.pack(pady=5)
        ttk.Button(btn_frame, text="Refresh", style="Rounded.TButton", command=self.refresh_history_tab).grid(row=0, column=0, padx=5)
        ttk.Button(btn_frame, text="Clear All", style="Rounded.TButton", command=self.clear_history_tab).grid(row=0, column=1, padx=5)
        ttk.Button(btn_frame, text="Search", style="Rounded.TButton", command=self.search_history_tab).grid(row=0, column=2, padx=5)
        ttk.Button(btn_frame, text="Export", style="Rounded.TButton", command=self.export_history_tab).grid(row=0, column=3, padx=5)

    def refresh_history_tab(self):
        self.history_box.delete(0, tk.END)
        for item in self.history.get_all():
            self.history_box.insert(tk.END, item)

    def clear_history_tab(self):
        if messagebox.askyesno("Confirm", "Clear all history?"):
            self.history.clear()
            self.refresh_history_tab()

    def search_history_tab(self):
        keyword = simpledialog.askstring("Search History", "Enter keyword:")
        if keyword:
            results = self.history.search(keyword)
            self.history_box.delete(0, tk.END)
            for item in results:
                self.history_box.insert(tk.END, item)

    def export_history_tab(self):
        filename = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt")])
        if filename:
            self.history.export_to_file(filename)
            messagebox.showinfo("Success", f"History exported to {filename}")

    # ---------------- Event Tab (Calendar Style) ----------------
    def create_event_tab(self):
        self.event_frame = tk.Frame(self.notebook, bg="#F5F5F5")
        self.notebook.add(self.event_frame, text="Events")
        top_frame = tk.Frame(self.event_frame, bg="#F5F5F5")
        top_frame.pack(pady=5)
        self.month_var = tk.IntVar(value=datetime.now().month)
        self.year_var = tk.IntVar(value=datetime.now().year)
        ttk.Button(top_frame, text="Prev Month", command=lambda:self.change_month(-1)).pack(side="left", padx=5)
        ttk.Button(top_frame, text="Next Month", command=lambda:self.change_month(1)).pack(side="left", padx=5)
        self.calendar_frame = tk.Frame(self.event_frame, bg="#F5F5F5")
        self.calendar_frame.pack(padx=10, pady=10, fill="both", expand=True)

    def change_month(self, delta):
        month = self.month_var.get() + delta
        year = self.year_var.get()
        if month < 1:
            month = 12
            year -= 1
        elif month > 12:
            month = 1
            year += 1
        self.month_var.set(month)
        self.year_var.set(year)
        self.refresh_event_tab()

    def refresh_event_tab(self):
        # Clear calendar
        for widget in self.calendar_frame.winfo_children():
            widget.destroy()

        month = self.month_var.get()
        year = self.year_var.get()
        cal = calendar.Calendar()
        tk.Label(self.calendar_frame, text=f"{calendar.month_name[month]} {year}", font=("Segoe UI", 16, "bold")).grid(row=0, column=0, columnspan=7, pady=10)

        # Weekday headers
        for i, day in enumerate(["Mon","Tue","Wed","Thu","Fri","Sat","Sun"]):
            tk.Label(self.calendar_frame, text=day, font=("Segoe UI", 11, "bold"), borderwidth=1, relief="solid", width=12, height=2).grid(row=1, column=i)

        # Dates
        events_dict = {}
        for e in self.events.get_all():
            try:
                name, date_str = e.split(" - ")
                date_obj = datetime.strptime(date_str, "%Y-%m-%d")
                events_dict.setdefault(date_obj.day, []).append(name)
            except:
                continue

        row = 2
        col = 0
        for day in cal.itermonthdays(year, month):
            if day == 0:
                tk.Label(self.calendar_frame, text="", borderwidth=1, relief="solid", width=12, height=5).grid(row=row, column=col)
            else:
                frame = tk.Frame(self.calendar_frame, borderwidth=1, relief="solid", width=12*8, height=60)
                frame.grid_propagate(False)
                frame.grid(row=row, column=col, padx=1, pady=1)
                tk.Label(frame, text=str(day), anchor="nw").pack(fill="x")
                for evt in events_dict.get(day, []):
                    color = "#FFECB3" if "Lecture" in evt else "#C8E6C9" if "Workshop" in evt else "#FFCDD2" if "Sports" in evt else "#D1C4E9" if "Festival" in evt else "#B3E5FC"
                    tk.Label(frame, text=evt, bg=color, wraplength=90, justify="left").pack(fill="x", pady=1)
            col += 1
            if col > 6:
                col = 0
                row += 1

# ---------------- Run the App ----------------
if __name__ == "__main__":
    root = tk.Tk()
    app = UniversityApp(root)
    root.mainloop()

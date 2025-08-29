

import tkinter as tk
from tkinter import ttk, messagebox, filedialog


# Linked List: History / Events

class HistoryNode:
    def __init__(self, data):
        self.data = data
        self.next = None

class History:
    def __init__(self, max_items=50):
        self.head = None
        self.size = 0
        self.max_items = max_items

    def add(self, item: str):
        node = HistoryNode(item)
        node.next = self.head
        self.head = node
        self.size += 1
        if self.size > self.max_items:
            self._trim_tail()

    def _trim_tail(self):
        prev, cur = None, self.head
        count = 1
        while cur and count < self.size:
            prev, cur = cur, cur.next
            count += 1
        if prev:
            prev.next = None
        self.size -= 1

    def to_list(self):
        out, cur = [], self.head
        while cur:
            out.append(cur.data)
            cur = cur.next
        return out

    def search(self, term: str):
        term = term.lower()
        return [item for item in self.to_list() if term in item.lower()]


# Tkinter UI for History

class HistoryApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("History / Events ")
        self.geometry("600x500")
        
        self.history = History(max_items=50)
        
        self.build_ui()
        self.log("Application started")

    def build_ui(self):
        # Top frame: add new history
        top = ttk.Frame(self)
        top.pack(fill="x", padx=10, pady=10)

        ttk.Label(top, text="Add Event:").pack(side="left", padx=(0,6))
        self.ent_event = ttk.Entry(top, width=40)
        self.ent_event.pack(side="left", padx=(0,6))
        ttk.Button(top, text="Add", command=self.on_add_event).pack(side="left")
        
        # Middle frame: search
        mid = ttk.Frame(self)
        mid.pack(fill="x", padx=10, pady=5)

        ttk.Label(mid, text="Search History:").pack(side="left", padx=(0,6))
        self.ent_search = ttk.Entry(mid, width=30)
        self.ent_search.pack(side="left", padx=(0,6))
        ttk.Button(mid, text="Search", command=self.on_search).pack(side="left")
        ttk.Button(mid, text="Clear Search", command=self.refresh_history).pack(side="left", padx=(6,0))
        
        # Listbox for history
        self.lst_history = tk.Listbox(self, height=20)
        self.lst_history.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Bottom frame: actions
        bottom = ttk.Frame(self)
        bottom.pack(fill="x", padx=10, pady=(0,10))

        ttk.Button(bottom, text="Refresh", command=self.refresh_history).pack(side="left")
        ttk.Button(bottom, text="Clear All", command=self.clear_history).pack(side="left", padx=6)
        ttk.Button(bottom, text="Delete Selected", command=self.delete_selected).pack(side="left", padx=6)
        ttk.Button(bottom, text="Export to File", command=self.export_history).pack(side="left", padx=6)

    
    # Event Handlers
  
    def log(self, text):
        self.history.add(text)
        self.refresh_history()

    def on_add_event(self):
        event = self.ent_event.get().strip()
        if event:
            self.log(event)
            self.ent_event.delete(0, "end")

    def refresh_history(self):
        self.lst_history.delete(0, "end")
        for item in self.history.to_list():
            self.lst_history.insert("end", item)

    def clear_history(self):
        if messagebox.askyesno("Confirm", "Clear all history?"):
            self.history = History(max_items=50)
            self.refresh_history()

    def delete_selected(self):
        sel = self.lst_history.curselection()
        if not sel:
            messagebox.showwarning("No selection", "Please select an item to delete.")
            return
        # Remove from linked list
        selected_item = self.lst_history.get(sel[0])
        self._remove_from_linked_list(selected_item)
        self.refresh_history()

    def _remove_from_linked_list(self, target):
        dummy = HistoryNode(None)
        dummy.next = self.history.head
        prev, cur = dummy, self.history.head
        while cur:
            if cur.data == target:
                prev.next = cur.next
                self.history.size -= 1
                break
            prev, cur = cur, cur.next
        self.history.head = dummy.next

    def on_search(self):
        term = self.ent_search.get().strip()
        self.lst_history.delete(0, "end")
        if not term:
            return
        results = self.history.search(term)
        if results:
            for item in results:
                self.lst_history.insert("end", item)
        else:
            self.lst_history.insert("end", "No matches.")

    def export_history(self):
        path = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("Text files","*.txt"),("All files","*.*")],
            title="Save History"
        )
        if path:
            try:
                with open(path, "w", encoding="utf-8") as f:
                    for item in self.history.to_list():
                        f.write(item + "\n")
                messagebox.showinfo("Success", f"History saved to {path}")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to save file: {e}")


if __name__ == "__main__":
    HistoryApp().mainloop()

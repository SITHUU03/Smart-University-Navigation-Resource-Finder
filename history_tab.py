import tkinter as tk
from tkinter import ttk, messagebox, filedialog, simpledialog
from constants import *


class HistoryTab:
    def __init__(self, notebook, app):
        self.app = app
        self.tab = tk.Frame(notebook, bg=BACKGROUND_COLOR)
        notebook.add(self.tab, text="📜 History")
        
        # Header
        header_frame = tk.Frame(self.tab, bg=PRIMARY_COLOR, height=100)
        header_frame.pack(fill="x", pady=(0, 15))
        header_frame.pack_propagate(False)
        tk.Label(header_frame, text="Navigation History", font=("Segoe UI", 20, "bold"), 
                bg=PRIMARY_COLOR, fg="white").pack(expand=True)
        
        content_frame = tk.Frame(self.tab, bg=BACKGROUND_COLOR)
        content_frame.pack(fill="both", expand=True, padx=25, pady=15)
        
        # Card for history
        history_card = tk.Frame(content_frame, bg=CARD_COLOR, padx=10, pady=10, relief="flat", bd=0)
        history_card.pack(fill="both", expand=True)
        
        tk.Label(history_card, text="Recent Paths", font=("Segoe UI", 16, "bold"), 
                bg=CARD_COLOR, fg=TEXT_COLOR).pack(anchor="w", pady=(0, 15))
        
        # Create listbox with scrollbar
        list_frame = tk.Frame(history_card, bg=CARD_COLOR)
        list_frame.pack(fill="both", expand=True, pady=10)
        
        self.history_box = tk.Listbox(list_frame, height=20, width=70,
                                     font=("Segoe UI", 11), bg="#F7F9FA", 
                                     fg=TEXT_COLOR, bd=0, relief="flat", highlightthickness=0,
                                     selectbackground=HIGHLIGHT_COLOR, selectforeground="white")
        
        scrollbar = ttk.Scrollbar(list_frame, orient="vertical", command=self.history_box.yview)
        self.history_box.configure(yscrollcommand=scrollbar.set)
        
        self.history_box.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Button frame
        btn_frame = tk.Frame(history_card, bg=CARD_COLOR)
        btn_frame.pack(pady=10)
        
        ttk.Button(btn_frame, text="Refresh", style="Secondary.TButton", 
                  command=self.refresh_history_tab).grid(row=0, column=0, padx=5)
        ttk.Button(btn_frame, text="Clear All", style="Accent.TButton", 
                  command=self.clear_history_tab).grid(row=0, column=1, padx=5)
        ttk.Button(btn_frame, text="Search", style="Secondary.TButton", 
                  command=self.search_history_tab).grid(row=0, column=2, padx=5)
        ttk.Button(btn_frame, text="Export", style="Secondary.TButton", 
                  command=self.export_history_tab).grid(row=0, column=3, padx=5)
        ttk.Button(btn_frame, text="Reuse", style="Success.TButton", 
                  command=self.reuse_history_item).grid(row=0, column=4, padx=5)
        
        # Load history immediately instead of showing placeholder
        self.refresh_history_tab()

    def refresh_history_tab(self):
        """Refresh the history tab content"""
        self.history_box.delete(0, tk.END)
        try:
            history_items = self.app.history.get_all()
            
            if not history_items:
                self.history_box.insert(tk.END, "No history records yet. Start navigating to build history!")
                self.history_box.itemconfig(0, fg="#7f8c8d")
            else:
                for i, item in enumerate(history_items):
                    self.history_box.insert(tk.END, f"{i+1}. {item}")
            
            self.app.update_status("History refreshed")
        except Exception as e:
            self.history_box.insert(tk.END, "Error loading history")
            self.history_box.itemconfig(0, fg=ACCENT_COLOR)
            print(f"Error refreshing history: {e}")

    def clear_history_tab(self):
        """Clear all history"""
        if messagebox.askyesno("Confirm Clear", "Are you sure you want to clear all history?"):
            try:
                self.app.history.clear()
                self.refresh_history_tab()
                self.app.update_status("History cleared")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to clear history: {str(e)}")

    def search_history_tab(self):
        """Search history items"""
        keyword = simpledialog.askstring("Search History", "Enter keyword to search:")
        if keyword:
            try:
                results = self.app.history.search(keyword)
                self.history_box.delete(0, tk.END)
                
                if not results:
                    self.history_box.insert(tk.END, f"No results found for '{keyword}'")
                    self.history_box.itemconfig(0, fg="#7f8c8d")
                else:
                    for i, item in enumerate(results):
                        self.history_box.insert(tk.END, f"{i+1}. {item}")
                
                self.app.update_status(f"Found {len(results)} results for '{keyword}'")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to search history: {str(e)}")

    def export_history_tab(self):
        """Export history to file"""
        filename = filedialog.asksaveasfilename(
            defaultextension=".txt", 
            filetypes=[("Text files", ".txt"), ("All files", ".*")],
            title="Export History To"
        )
        if filename:
            try:
                self.app.history.export_to_file(filename)
                messagebox.showinfo("Success", f"History exported to {filename}")
                self.app.update_status(f"History exported to {filename}")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to export history: {str(e)}")

    def reuse_history_item(self):
        """Reuse a selected history item"""
        selection = self.history_box.curselection()
        if not selection:
            messagebox.showwarning("Warning", "Please select a history item first")
            return
        
        item = self.history_box.get(selection[0])
        
        # Check if it's the placeholder message
        if "No history records" in item or "Error loading" in item:
            messagebox.showwarning("Warning", "No valid history item selected")
            return
        
        
        if "Navigation: " in item and " → " in item:
            try:
                parts = item.split("Navigation: ")[1].split(" → ")
                start = parts[0].strip()
                end = parts[1].split(" (")[0].strip()
                
                # Set the values in navigation tab
                self.app.navigation_tab.start_var.set(start)
                self.app.navigation_tab.end_var.set(end)
                self.app.notebook.select(0)  # Switch to navigation tab
                self.app.update_status(f"Loaded route: {start} to {end}")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to parse history item: {str(e)}")
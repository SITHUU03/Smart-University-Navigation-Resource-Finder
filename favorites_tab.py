import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
from constants import *


class FavoritesTab:
    def __init__(self, notebook, app):
        self.app = app
        self.tab = tk.Frame(notebook, bg=BACKGROUND_COLOR)
        notebook.add(self.tab, text="⭐ Favorites")
        
        # Header
        header_frame = tk.Frame(self.tab, bg=PRIMARY_COLOR, height=100)
        header_frame.pack(fill="x", pady=(0, 15))
        header_frame.pack_propagate(False)
        tk.Label(header_frame, text="Favorite Locations & Routes", font=("Segoe UI", 20, "bold"), 
                bg=PRIMARY_COLOR, fg="white").pack(expand=True)
        
        content_frame = tk.Frame(self.tab, bg=BACKGROUND_COLOR)
        content_frame.pack(fill="both", expand=True, padx=25, pady=15)
        
        # Create notebook for favorites
        fav_notebook = ttk.Notebook(content_frame)
        fav_notebook.pack(fill="both", expand=True)
        
        # Locations tab
        loc_frame = tk.Frame(fav_notebook, bg=BACKGROUND_COLOR)
        fav_notebook.add(loc_frame, text="Locations")
        
        # Routes tab
        route_frame = tk.Frame(fav_notebook, bg=BACKGROUND_COLOR)
        fav_notebook.add(route_frame, text="Routes")
        
        # Populate locations tab
        tk.Label(loc_frame, text="Favorite Locations", 
                font=("Segoe UI", 16, "bold"), bg=BACKGROUND_COLOR, fg=TEXT_COLOR).pack(pady=10)
        
        loc_list_frame = tk.Frame(loc_frame, bg=BACKGROUND_COLOR)
        loc_list_frame.pack(fill="both", expand=True, padx=20, pady=10)
        
        self.loc_listbox = tk.Listbox(loc_list_frame, font=("Segoe UI", 11), 
                                     bg="white", selectmode="single")
        self.loc_listbox.pack(side="left", fill="both", expand=True)
        
        loc_scrollbar = ttk.Scrollbar(loc_list_frame, orient="vertical", command=self.loc_listbox.yview)
        self.loc_listbox.configure(yscrollcommand=loc_scrollbar.set)
        loc_scrollbar.pack(side="right", fill="y")
        
        # Location buttons
        loc_btn_frame = tk.Frame(loc_frame, bg=BACKGROUND_COLOR)
        loc_btn_frame.pack(pady=10)
        
        ttk.Button(loc_btn_frame, text="Add Current", style="Secondary.TButton",
                  command=self.add_current_to_favorites).pack(side="left", padx=5)
        ttk.Button(loc_btn_frame, text="Use as Start", style="Success.TButton",
                  command=lambda: self.use_favorite_location("start")).pack(side="left", padx=5)
        ttk.Button(loc_btn_frame, text="Use as Destination", style="Success.TButton",
                  command=lambda: self.use_favorite_location("end")).pack(side="left", padx=5)
        ttk.Button(loc_btn_frame, text="Remove", style="Secondary.TButton",
                  command=self.remove_favorite_location).pack(side="left", padx=5)
        
        # Populate routes tab
        tk.Label(route_frame, text="Favorite Routes", 
                font=("Segoe UI", 16, "bold"), bg=BACKGROUND_COLOR, fg=TEXT_COLOR).pack(pady=10)
        
        route_list_frame = tk.Frame(route_frame, bg=BACKGROUND_COLOR)
        route_list_frame.pack(fill="both", expand=True, padx=20, pady=10)
        
        self.route_listbox = tk.Listbox(route_list_frame, font=("Segoe UI", 11), 
                                       bg="white", selectmode="single")
        self.route_listbox.pack(side="left", fill="both", expand=True)
        
        route_scrollbar = ttk.Scrollbar(route_list_frame, orient="vertical", command=self.route_listbox.yview)
        self.route_listbox.configure(yscrollcommand=route_scrollbar.set)
        route_scrollbar.pack(side="right", fill="y")
        
        # Route buttons
        route_btn_frame = tk.Frame(route_frame, bg=BACKGROUND_COLOR)
        route_btn_frame.pack(pady=10)
        
        ttk.Button(route_btn_frame, text="Use Route", style="Success.TButton",
                  command=self.use_favorite_route).pack(side="left", padx=5)
        ttk.Button(route_btn_frame, text="Remove", style="Secondary.TButton",
                  command=self.remove_favorite_route).pack(side="left", padx=5)
        
        # Initial refresh
        self.refresh_favorites_tab()

    def refresh_favorites_tab(self):
        """Refresh favorites tab content"""
        # Refresh locations
        self.loc_listbox.delete(0, tk.END)
        for loc in self.app.favorites.get("locations", []):
            self.loc_listbox.insert(tk.END, loc)
        
        # Refresh routes
        self.route_listbox.delete(0, tk.END)
        for route in self.app.favorites.get("routes", []):
            self.route_listbox.insert(tk.END, f"{route['name']}: {route['start']} → {route['end']}")

    def add_current_to_favorites(self):
        """Add current location to favorites"""
        if not self.app.navigation_tab.start_var.get():
            messagebox.showwarning("Warning", "Please select a location first")
            return
        
        location = self.app.navigation_tab.start_var.get()
        if location not in self.app.favorites.get("locations", []):
            if "locations" not in self.app.favorites:
                self.app.favorites["locations"] = []
            self.app.favorites["locations"].append(location)
            self.app.save_favorites()
            self.refresh_favorites_tab()
            messagebox.showinfo("Success", f"Added {location} to favorites")
        else:
            messagebox.showinfo("Info", f"{location} is already in your favorites")

    def use_favorite_location(self, target):
        """Use favorite location as start or end"""
        selection = self.loc_listbox.curselection()
        if not selection:
            messagebox.showwarning("Warning", "Please select a location first")
            return
        
        location = self.loc_listbox.get(selection[0])
        if target == "start":
            self.app.navigation_tab.start_var.set(location)
        else:
            self.app.navigation_tab.end_var.set(location)
        
        self.app.notebook.select(0)  # Switch to navigation tab
        self.app.update_status(f"Set {target} to {location}")

    def remove_favorite_location(self):
        """Remove favorite location"""
        selection = self.loc_listbox.curselection()
        if not selection:
            messagebox.showwarning("Warning", "Please select a location first")
            return
        
        location = self.loc_listbox.get(selection[0])
        if messagebox.askyesno("Confirm", f"Remove {location} from favorites?"):
            if location in self.app.favorites.get("locations", []):
                self.app.favorites["locations"].remove(location)
                self.app.save_favorites()
                self.refresh_favorites_tab()
                self.app.update_status(f"Removed {location} from favorites")

    def use_favorite_route(self):
        """Use favorite route"""
        selection = self.route_listbox.curselection()
        if not selection:
            messagebox.showwarning("Warning", "Please select a route first")
            return
        
        route_str = self.route_listbox.get(selection[0])
        # Extract start and end from route string
        # Format: "Name: Start → End"
        parts = route_str.split(": ")
        if len(parts) >= 2:
            route_parts = parts[1].split(" → ")
            if len(route_parts) >= 2:
                self.app.navigation_tab.start_var.set(route_parts[0])
                self.app.navigation_tab.end_var.set(route_parts[1])
                self.app.notebook.select(0)  # Switch to navigation tab
                self.app.update_status(f"Loaded route: {route_str}")

    def remove_favorite_route(self):
        """Remove favorite route"""
        selection = self.route_listbox.curselection()
        if not selection:
            messagebox.showwarning("Warning", "Please select a route first")
            return
        
        route_str = self.route_listbox.get(selection[0])
        # Find the route in favorites
        route_name = route_str.split(": ")[0]
        for i, route in enumerate(self.app.favorites.get("routes", [])):
            if route["name"] == route_name:
                if messagebox.askyesno("Confirm", f"Remove {route_name} from favorites?"):
                    del self.app.favorites["routes"][i]
                    self.app.save_favorites()
                    self.refresh_favorites_tab()
                    self.app.update_status(f"Removed {route_name} from favorites")
                return
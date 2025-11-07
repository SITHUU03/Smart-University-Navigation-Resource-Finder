import tkinter as tk
from tkinter import ttk, messagebox
import calendar
from datetime import datetime, date
from constants import *


class EventsTab:
    def __init__(self, notebook, app):
        self.app = app
        self.tab = tk.Frame(notebook, bg=BACKGROUND_COLOR)
        notebook.add(self.tab, text="📅 Events")
        
        # Header
        header_frame = tk.Frame(self.tab, bg=PRIMARY_COLOR, height=100)
        header_frame.pack(fill="x", pady=(0, 15))
        header_frame.pack_propagate(False)
        tk.Label(header_frame, text="University Events", font=("Segoe UI", 20, "bold"), 
                bg=PRIMARY_COLOR, fg="white").pack(expand=True)
        
        content_frame = tk.Frame(self.tab, bg=BACKGROUND_COLOR)
        content_frame.pack(fill="both", expand=True, padx=25, pady=15)
        
        # Card for calendar
        calendar_card = tk.Frame(content_frame, bg=CARD_COLOR, padx=10, pady=10, relief="flat", bd=0)
        calendar_card.pack(fill="both", expand=True)
        
        # Month navigation
        nav_frame = tk.Frame(calendar_card, bg=CARD_COLOR)
        nav_frame.pack(fill="x", pady=(0, 10))
        
        self.month_var = tk.IntVar(value=datetime.now().month)
        self.year_var = tk.IntVar(value=datetime.now().year)
        
        ttk.Button(nav_frame, text="◀ Previous Month", style="Secondary.TButton", 
                  command=lambda: self.change_month(-1)).pack(side="left", padx=5)
        
        # Today button
        ttk.Button(nav_frame, text="Today", style="Secondary.TButton", 
                  command=self.go_to_today).pack(side="left", padx=5)
        
        # Month-Year display
        self.month_year_label = tk.Label(nav_frame, text="", font=("Segoe UI", 12, "bold"), 
                                        bg=CARD_COLOR, fg=TEXT_COLOR)
        self.month_year_label.pack(side="left", padx=20, expand=True)
        
        ttk.Button(nav_frame, text="Next Month ▶", style="Secondary.TButton", 
                  command=lambda: self.change_month(1)).pack(side="right", padx=5)
        
        # Add event button
        ttk.Button(nav_frame, text="+ Add Event", style="Success.TButton", 
                  command=self.add_event).pack(side="right", padx=5)
        
        # Create a tooltip label
        self.tooltip = tk.Label(calendar_card, text="", bg="lightyellow", relief="solid", borderwidth=1,
                               font=("Segoe UI", 10), justify="left")
        self.tooltip.place_forget()  # Hide initially
        
        # Calendar container
        self.calendar_container = tk.Frame(calendar_card, bg=CARD_COLOR)
        self.calendar_container.pack(fill="both", expand=True)
        
        # Initial refresh
        self.refresh_event_tab()

    def go_to_today(self):
        """Go to current month and year"""
        now = datetime.now()
        self.month_var.set(now.month)
        self.year_var.set(now.year)
        self.refresh_event_tab()
        self.app.update_status("Viewing current month")

    def add_event(self):
        """Add a new event"""
        dialog = tk.Toplevel(self.app.root)
        dialog.title("Add New Event")
        dialog.geometry("400x300")
        dialog.configure(bg=BACKGROUND_COLOR)
        dialog.transient(self.app.root)
        dialog.grab_set()
        
        tk.Label(dialog, text="Add New Event", font=("Segoe UI", 16, "bold"), 
                bg=BACKGROUND_COLOR, fg=TEXT_COLOR).pack(pady=20)
        
        # Event name
        tk.Label(dialog, text="Event Name:", font=("Segoe UI", 11, "bold"), 
                bg=BACKGROUND_COLOR, fg=TEXT_COLOR).pack(anchor="w", padx=50)
        name_var = tk.StringVar()
        name_entry = ttk.Entry(dialog, textvariable=name_var, font=("Segoe UI", 11))
        name_entry.pack(fill="x", padx=50, pady=5)
        
        # Event date
        tk.Label(dialog, text="Date (YYYY-MM-DD):", font=("Segoe UI", 11, "bold"), 
                bg=BACKGROUND_COLOR, fg=TEXT_COLOR).pack(anchor="w", padx=50, pady=(10, 0))
        date_var = tk.StringVar()
        date_entry = ttk.Entry(dialog, textvariable=date_var, font=("Segoe UI", 11))
        date_entry.pack(fill="x", padx=50, pady=5)
        
        # Event location
        tk.Label(dialog, text="Location:", font=("Segoe UI", 11, "bold"), 
                bg=BACKGROUND_COLOR, fg=TEXT_COLOR).pack(anchor="w", padx=50, pady=(10, 0))
        location_var = tk.StringVar()
        location_combo = ttk.Combobox(dialog, textvariable=location_var, 
                                     values=list(self.app.nav.graph.keys()), 
                                     font=("Segoe UI", 11))
        location_combo.pack(fill="x", padx=50, pady=5)
        
        def save_event():
            if not name_var.get() or not date_var.get():
                messagebox.showerror("Error", "Please fill in all required fields")
                return
            
            event_str = f"{name_var.get()} - {date_var.get()}"
            if location_var.get():
                event_str += f" - {location_var.get()}"
            
            self.app.events.add(event_str)
            self.refresh_event_tab()
            dialog.destroy()
            messagebox.showinfo("Success", "Event added successfully")
        
        btn_frame = tk.Frame(dialog, bg=BACKGROUND_COLOR)
        btn_frame.pack(pady=20)
        
        ttk.Button(btn_frame, text="Save", style="Success.TButton", 
                  command=save_event).pack(side="left", padx=10)
        ttk.Button(btn_frame, text="Cancel", style="Secondary.TButton", 
                  command=dialog.destroy).pack(side="left", padx=10)

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
        self.app.update_status(f"Viewing {calendar.month_name[month]} {year}")

    def refresh_event_tab(self):
        # Clear calendar container
        for widget in self.calendar_container.winfo_children():
            widget.destroy()
            
        month = self.month_var.get()
        year = self.year_var.get()
        
        # Update month-year label
        self.month_year_label.config(text=f"{calendar.month_name[month]} {year}")
        
        cal = calendar.Calendar(firstweekday=0)  # 0 = Monday, 6 = Sunday
        
        # Parse events with location information
        events_dict = {}
        for e in self.app.events.get_all():
            try:
                # Split event into name, date, and location
                parts = e.split(" - ")
                if len(parts) >= 3:
                    name = parts[0]
                    date_str = parts[1]
                    location = parts[2]
                    date_obj = datetime.strptime(date_str, "%Y-%m-%d")
                    # Only show events for the current month/year
                    if date_obj.month == month and date_obj.year == year:
                        events_dict.setdefault(date_obj.day, []).append((name, location))
            except:
                continue

        # Create weekday headers
        weekdays_frame = tk.Frame(self.calendar_container, bg=CARD_COLOR)
        weekdays_frame.pack(fill="x")
        
        weekdays = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
        for i, day in enumerate(weekdays):
            cell = tk.Frame(weekdays_frame, bg=PRIMARY_COLOR, height=30)
            cell.grid(row=0, column=i, sticky="nsew", padx=1, pady=1)
            cell.grid_propagate(False)
            tk.Label(cell, text=day, font=("Segoe UI", 10, "bold"), 
                    bg=PRIMARY_COLOR, fg="white").pack(expand=True)
            weekdays_frame.columnconfigure(i, weight=1)

        # Create calendar grid
        calendar_grid = tk.Frame(self.calendar_container, bg=CARD_COLOR)
        calendar_grid.pack(fill="both", expand=True)
        
        # Configure grid
        for i in range(7):  # 7 columns for days
            calendar_grid.columnconfigure(i, weight=1)
        for i in range(6):  # 6 rows for weeks
            calendar_grid.rowconfigure(i, weight=1)
        
        # Get the days for the month
        month_days = cal.monthdayscalendar(year, month)
        
        # Create day cells
        for row, week in enumerate(month_days):
            for col, day in enumerate(week):
                cell = tk.Frame(calendar_grid, bg=CARD_COLOR, relief="raised", bd=1)
                cell.grid(row=row, column=col, sticky="nsew", padx=1, pady=1)
                
                if day == 0:
                    # Empty cell for days not in current month
                    continue
                
                # Day number
                day_frame = tk.Frame(cell, bg=CARD_COLOR)
                day_frame.pack(fill="x")
                
                day_label = tk.Label(day_frame, text=str(day), font=("Segoe UI", 10, "bold"), 
                                    bg=CARD_COLOR, fg=TEXT_COLOR)
                day_label.pack(anchor="ne", padx=5, pady=2)
                
                # Check if this day has events
                day_events = events_dict.get(day, [])
                
                if day_events:
                    # Highlight today if it has events
                    if day == date.today().day and month == date.today().month and year == date.today().year:
                        day_label.config(bg=HIGHLIGHT_COLOR, fg="white")
                        day_frame.config(bg=HIGHLIGHT_COLOR)
                    
                    # Add events
                    for evt_name, evt_location in day_events:
                        color = "#FFECB3" if "Lecture" in evt_name else "#C8E6C9" if "Workshop" in evt_name else "#FFCDD2" if "Sports" in evt_name else "#D1C4E9" if "Festival" in evt_name else "#B3E5FC"
                        
                        # Create event label with hover functionality
                        event_label = tk.Label(cell, text=evt_name, bg=color, wraplength=100, 
                                             justify="left", font=("Segoe UI", 8), padx=2, pady=1)
                        event_label.pack(fill="x", padx=2, pady=1)
                        
                        # Store location information in the label object
                        event_label.location = evt_location
                        
                        # Bind hover events to show location
                        event_label.bind("<Enter>", self.show_event_location_tooltip)
                        event_label.bind("<Leave>", self.hide_event_tooltip)
                        
                # Bind click event to show event details
                cell.bind("<Button-1>", lambda e, d=day: self.show_day_events(d, month, year))

    def show_event_location_tooltip(self, event):
        # Get the location from the widget
        location = event.widget.location
        
        # Position the tooltip near the cursor
        x = event.widget.winfo_rootx() + 10
        y = event.widget.winfo_rooty() + 10
        
        # Update tooltip text
        self.tooltip.config(text=f"Location: {location}")
        
        # Show the tooltip
        self.tooltip.place(x=x, y=y)
        self.tooltip.lift()

    def hide_event_tooltip(self, event):
        # Hide the tooltip
        self.tooltip.place_forget()

    def show_day_events(self, day, month, year):
        """Show events for a specific day"""
        events_on_day = []
        for e in self.app.events.get_all():
            try:
                parts = e.split(" - ")
                if len(parts) >= 2:
                    date_str = parts[1]
                    date_obj = datetime.strptime(date_str, "%Y-%m-%d")
                    if date_obj.day == day and date_obj.month == month and date_obj.year == year:
                        events_on_day.append(e)
            except:
                continue
        
        if not events_on_day:
            messagebox.showinfo("Events", f"No events on {day}/{month}/{year}")
            return
        
        # Create dialog to show events
        dialog = tk.Toplevel(self.app.root)
        dialog.title(f"Events on {day}/{month}/{year}")
        dialog.geometry("500x300")
        dialog.configure(bg=BACKGROUND_COLOR)
        dialog.transient(self.app.root)
        dialog.grab_set()
        
        tk.Label(dialog, text=f"Events on {day}/{month}/{year}", 
                font=("Segoe UI", 14, "bold"), bg=BACKGROUND_COLOR).pack(pady=10)
        
        # Create listbox for events
        list_frame = tk.Frame(dialog, bg=BACKGROUND_COLOR)
        list_frame.pack(fill="both", expand=True, padx=20, pady=10)
        
        event_list = tk.Listbox(list_frame, font=("Segoe UI", 11), 
                               bg="white", selectmode="single")
        event_list.pack(side="left", fill="both", expand=True)
        
        scrollbar = ttk.Scrollbar(list_frame, orient="vertical", command=event_list.yview)
        event_list.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side="right", fill="y")
        
        for event in events_on_day:
            event_list.insert(tk.END, event)
        
        # Button frame
        btn_frame = tk.Frame(dialog, bg=BACKGROUND_COLOR)
        btn_frame.pack(pady=10)
        
        ttk.Button(btn_frame, text="OK", style="Success.TButton", 
                  command=dialog.destroy).pack(side="left", padx=10)
        
        ttk.Button(btn_frame, text="Navigate to Event", style="Secondary.TButton",
                  command=lambda: self.navigate_to_event(event_list, dialog)).pack(side="left", padx=10)

    def navigate_to_event(self, event_list, dialog):
        """Navigate to selected event location"""
        selection = event_list.curselection()
        if not selection:
            messagebox.showwarning("Warning", "Please select an event first")
            return
        
        event = event_list.get(selection[0])
        parts = event.split(" - ")
        if len(parts) >= 3:  # Event has location
            location = parts[2]
            self.app.navigation_tab.start_var.set("Main Entrance")  # Default start point
            self.app.navigation_tab.end_var.set(location)
            self.app.notebook.select(0)  # Switch to navigation tab
            dialog.destroy()
            self.app.update_status(f"Setting destination to {location}")
        else:
            messagebox.showinfo("Info", "This event doesn't have a specified location")
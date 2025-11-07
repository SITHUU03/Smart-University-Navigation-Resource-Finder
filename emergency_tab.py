import tkinter as tk
from tkinter import ttk, messagebox
from constants import *


class EmergencyTab:
    def __init__(self, notebook, app):
        self.app = app
        self.tab = tk.Frame(notebook, bg=BACKGROUND_COLOR)
        notebook.add(self.tab, text="🚨 Emergency")
        
        # Header
        header_frame = tk.Frame(self.tab, bg=PRIMARY_COLOR, height=100)
        header_frame.pack(fill="x", pady=(0, 15))
        header_frame.pack_propagate(False)
        tk.Label(header_frame, text="Emergency Services & Information", font=("Segoe UI", 20, "bold"), 
                bg=PRIMARY_COLOR, fg="white").pack(expand=True)
        
        content_frame = tk.Frame(self.tab, bg=BACKGROUND_COLOR)
        content_frame.pack(fill="both", expand=True, padx=25, pady=15)
        
        # Emergency contacts
        contacts_frame = tk.Frame(content_frame, bg=CARD_COLOR, padx=20, pady=20)
        contacts_frame.pack(fill="x", pady=10)
        
        tk.Label(contacts_frame, text="Emergency Contacts", 
                font=("Segoe UI", 16, "bold"), bg=CARD_COLOR, fg=TEXT_COLOR).pack(anchor="w", pady=(0, 15))
        
        contacts = [
            ("Campus Security", "555-1234", "24/7 emergency line"),
            ("Medical Center", "555-5678", "Open 8AM-8PM"),
            ("Counseling Services", "555-9012", "Open 9AM-5PM"),
            ("Emergency", "911", "Police, Fire, Ambulance")
        ]
        
        for i, (name, number, hours) in enumerate(contacts):
            contact_frame = tk.Frame(contacts_frame, bg=CARD_COLOR)
            contact_frame.pack(fill="x", pady=5)
            
            tk.Label(contact_frame, text=name, font=("Segoe UI", 11, "bold"), 
                    bg=CARD_COLOR, fg=TEXT_COLOR, width=20, anchor="w").pack(side="left")
            tk.Label(contact_frame, text=number, font=("Segoe UI", 11), 
                    bg=CARD_COLOR, fg=ACCENT_COLOR, width=10, anchor="w").pack(side="left")
            tk.Label(contact_frame, text=hours, font=("Segoe UI", 11), 
                    bg=CARD_COLOR, fg=TEXT_COLOR, anchor="w").pack(side="left")
            
            # Call button
            ttk.Button(contact_frame, text="Call", style="Secondary.TButton",
                      command=lambda n=number: self.simulate_call(n)).pack(side="right")
        
        # Emergency procedures
        procedures_frame = tk.Frame(content_frame, bg=CARD_COLOR, padx=20, pady=20)
        procedures_frame.pack(fill="x", pady=10)
        
        tk.Label(procedures_frame, text="Emergency Procedures", 
                font=("Segoe UI", 16, "bold"), bg=CARD_COLOR, fg=TEXT_COLOR).pack(anchor="w", pady=(0, 15))
        
        procedures = [
            ("Medical Emergency", "Call campus medical center and provide location details"),
            ("Fire Emergency", "Activate nearest fire alarm and evacuate building"),
            ("Security Threat", "Call campus security and follow their instructions"),
            ("Weather Emergency", "Seek shelter in designated safe areas")
        ]
        
        for name, procedure in procedures:
            proc_frame = tk.Frame(procedures_frame, bg=CARD_COLOR)
            proc_frame.pack(fill="x", pady=5)
            
            tk.Label(proc_frame, text=name, font=("Segoe UI", 11, "bold"), 
                    bg=CARD_COLOR, fg=TEXT_COLOR, width=20, anchor="w").pack(side="left")
            tk.Label(proc_frame, text=procedure, font=("Segoe UI", 11), 
                    bg=CARD_COLOR, fg=TEXT_COLOR, anchor="w", wraplength=600, justify="left").pack(side="left", fill="x", expand=True)
        
        # Emergency locations
        locations_frame = tk.Frame(content_frame, bg=CARD_COLOR, padx=20, pady=20)
        locations_frame.pack(fill="x", pady=10)
        
        tk.Label(locations_frame, text="Emergency Locations", 
                font=("Segoe UI", 16, "bold"), bg=CARD_COLOR, fg=TEXT_COLOR).pack(anchor="w", pady=(0, 15))
        
        emergency_locations = [
            ("Medical Center", "Main Campus, Building A"),
            ("Security Office", "North Campus, Building C"),
            ("Emergency Assembly", "South Parking Lot"),
            ("First Aid Stations", "All main building entrances")
        ]
        
        for name, location in emergency_locations:
            loc_frame = tk.Frame(locations_frame, bg=CARD_COLOR)
            loc_frame.pack(fill="x", pady=5)
            
            tk.Label(loc_frame, text=name, font=("Segoe UI", 11, "bold"), 
                    bg=CARD_COLOR, fg=TEXT_COLOR, width=20, anchor="w").pack(side="left")
            tk.Label(loc_frame, text=location, font=("Segoe UI", 11), 
                    bg=CARD_COLOR, fg=TEXT_COLOR, anchor="w").pack(side="left")
            
            # Navigate button
            ttk.Button(loc_frame, text="Navigate", style="Secondary.TButton",
                      command=lambda l=name: self.navigate_to_emergency(l)).pack(side="right")
        
        # Quick actions
        actions_frame = tk.Frame(content_frame, bg=CARD_COLOR, padx=20, pady=20)
        actions_frame.pack(fill="x", pady=20)
        
        ttk.Button(actions_frame, text="🆘 Emergency Call", style="Primary.TButton",
                  command=lambda: self.simulate_call("911"), width=20).pack(side="left", padx=10)
        ttk.Button(actions_frame, text="📍 Share My Location", style="Secondary.TButton",
                  command=self.share_location, width=20).pack(side="left", padx=10)
        ttk.Button(actions_frame, text="ℹ Emergency Info", style="Secondary.TButton",
                  command=self.show_emergency_info, width=20).pack(side="left", padx=10)

    def simulate_call(self, number):
        """Simulate a phone call (would integrate with phone system in real app)"""
        messagebox.showinfo("Emergency Call", f"Simulating call to {number}\n\nIn a real application, this would dial the number.")

    def navigate_to_emergency(self, location):
        """Navigate to emergency location"""
        self.app.navigation_tab.start_var.set("Main Entrance")  # Default start point
        self.app.navigation_tab.end_var.set(location)
        self.app.notebook.select(0)  # Switch to navigation tab
        self.app.update_status(f"Setting destination to {location}")

    def share_location(self):
        """Share current location (simulated)"""
        if not self.app.navigation_tab.start_var.get():
            messagebox.showwarning("Warning", "Please set your current location first")
            return
        
        messagebox.showinfo("Share Location", f"Sharing your location: {self.app.navigation_tab.start_var.get()}\n\nIn a real application, this would share via SMS or email.")

    def show_emergency_info(self):
        """Show emergency information"""
        info = """EMERGENCY PROCEDURES

1. MEDICAL EMERGENCY:
   - Call Campus Medical Center: 555-5678
   - Provide exact location and nature of emergency
   - Stay with the person until help arrives

2. FIRE EMERGENCY:
   - Activate the nearest fire alarm
   - Evacuate the building immediately
   - Do not use elevators
   - Assemble at designated emergency assembly point

3. SECURITY THREAT:
   - Call Campus Security: 555-1234
   - Follow instructions from security personnel
   - Avoid the area of threat

4. WEATHER EMERGENCY:
   - Seek shelter in designated safe areas
   - Monitor weather alerts
   - Follow instructions from university officials

Remember: Your safety is the top priority."""
        
        dialog = tk.Toplevel(self.app.root)
        dialog.title("Emergency Information")
        dialog.geometry("600x500")
        dialog.configure(bg=BACKGROUND_COLOR)
        dialog.transient(self.app.root)
        dialog.grab_set()
        
        text_widget = tk.Text(dialog, wrap="word", font=("Segoe UI", 11), 
                             bg=BACKGROUND_COLOR, padx=20, pady=20)
        text_widget.insert("1.0", info)
        text_widget.config(state="disabled")
        text_widget.pack(fill="both", expand=True)
        
        ttk.Button(dialog, text="Close", style="Success.TButton", 
                  command=dialog.destroy).pack(pady=10)
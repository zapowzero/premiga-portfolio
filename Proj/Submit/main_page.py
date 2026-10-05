import tkinter as tk
from tkinter import messagebox, Label, Button, Text, ttk, Menu
import json
import tkinter.filedialog as filedialog
import random
from datetime import datetime  # Import datetime for date handling

from login import EmployeeSystem

class MainPage(tk.Tk):
    def __init__(self, user_data):
        super().__init__()

        self.user_data = user_data
        self.title("Main Page")
        self.geometry("1800x1000")
        self.is_fullscreen = False  # Track full-screen state

        # Configure grid for dynamic resizing
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # Set background color for the window
        self.config(bg="#FF8C00")

        # Left panel
        self.left_frame = tk.Frame(self, bg="#FF8C00", width=250)  # Changed to instance variable
        self.left_frame.pack(side="left", fill="y", padx=20)  # Added margin space

        # Bind F11 key for toggling fullscreen
        self.bind("<F11>", lambda event: self.toggle_fullscreen())

        # Load user data from JSON file
        self.load_user_data()

        # Emoji Frame
        emoji_frame = tk.Frame(self.left_frame, bg="#FF8C00", width=250, height=150)
        emoji_frame.pack(fill="x", pady=10)

        # Emoji Profile Picture
        emoji = self.user_data.get("profile_picture", "😀")  # Default emoji if not provided
        self.emoji_label = tk.Label(emoji_frame, text=emoji, font=("Helvetica", 50), bg="#FF8C00", fg="white", cursor="hand2")

        # Store the original position
        self.emoji_original_x = 73  # Example x-coordinate
        self.emoji_original_y = 50  # Example y-coordinate
        self.emoji_label.place(x=self.emoji_original_x, y=self.emoji_original_y)  # Use place() for positioning

        # Bind left-click to change emoji
        self.emoji_label.bind("<Button-1>", lambda e: self.change_emoji())  # Left-click to change emoji

        # Bind right-click hold to allow dragging
        self.emoji_label.bind("<ButtonPress-3>", self.start_drag)  # Right-click to start dragging
        self.emoji_label.bind("<B3-Motion>", self.do_drag)  # Right-click and drag to move

        # Bind right-click release to reset emoji position
        self.emoji_label.bind("<ButtonRelease-3>", lambda e: self.reset_emoji_position())  # Right-click to reset position

        # User Label
        self.user_label = tk.Label(
            self.left_frame,
            text=f"{self.user_data.get('first_name', 'Unknown')} {self.user_data.get('last_name', '')}\n",
            font=("Helvetica", 14, "bold"),
            bg="#FF8C00",
            fg="white",
            justify="left",  # Align the text to the left
            cursor="hand2"
        )
        self.user_label.pack(pady=10, padx=55, anchor="w")  # Align to the left with padding

        # Bind click event to show employee information
        self.user_label.bind("<Button-1>", lambda e: self.show_profile_info())

        button_style = {"font": ("Helvetica", 12, "bold"), "bg": "#ffffff", "fg": "#FF8C00", "relief": "flat", "width": 20, "height": 2}

        self.contact_button = tk.Button(self.left_frame, text="Contact List", **button_style, command=self.contact_list)
        self.contact_button.pack(pady=10, padx=10, anchor="w")  # Adjusted alignment

        self.approve_button = tk.Button(self.left_frame, text="Request & Approve", **button_style, command=self.show_approve)
        self.approve_button.pack(pady=10, padx=10, anchor="w")  # Adjusted alignment

        # Only show the Helpdesk button if the user has the "Support" position
        if self.user_data.get("position") == "Support":
            self.helpdesk_button = tk.Button(self.left_frame, text="Helpdesk", **button_style, command=self.helpdesk)
            self.helpdesk_button.pack(pady=10, padx=10, anchor="w")  # Adjusted alignment

        # Create a frame for bottom-aligned buttons
        bottom_frame = tk.Frame(self.left_frame, bg="#FF8C00")
        bottom_frame.pack(side="bottom", anchor="sw", fill="x", pady=20)

        self.report_button = tk.Button(bottom_frame, text="Report", **button_style, command=self.show_report)
        self.report_button.pack(pady=10, padx=10, anchor="w")  # Adjusted alignment

        self.logout_button = tk.Button(bottom_frame, text="Log Out", **button_style, command=self.logout)
        self.logout_button.pack(pady=10, padx=10, anchor="w")  # Adjusted alignment

        # Right panel for the sections
        self.right_frame = tk.Frame(self, bg="#F8F8F8", width=950, height=700)
        self.right_frame.pack(side="right", fill="both", expand=True)
        self.right_frame.pack_forget()  # Initially hidden

        # Create menu bar
        self.create_menu_bar()
        
    def load_user_data(self):
        """Load user data from the JSON file."""
        try:
            with open(r'D:\Class\Interact_Prog\Proj\users.json', 'r') as file:
                users = json.load(file)
                email = self.user_data.get("email", "")
                self.user_data = users.get(email, self.user_data)  # Update user_data with JSON data
        except (FileNotFoundError, json.JSONDecodeError):
            messagebox.showerror("Error", "Unable to load user data.")

    #toolbar
    def create_menu_bar(self):
        """Creates the menu bar with fullscreen toggle options and Help menu."""
        menu_bar = Menu(self)

        # View Menu
        view_menu = Menu(menu_bar, tearoff=0)

        # Mode Submenu
        mode_menu = Menu(view_menu, tearoff=0)
        mode_menu.add_command(label="Full Screen (F11)", command=self.toggle_fullscreen)
        mode_menu.add_command(label="Exit Full Screen (F11)", command=self.toggle_fullscreen)

        view_menu.add_cascade(label="Mode", menu=mode_menu)
        menu_bar.add_cascade(label="View", menu=view_menu)

        # Help Menu
        help_menu = Menu(menu_bar, tearoff=0)
        help_menu.add_command(label="CMS ver.0.1")
        menu_bar.add_cascade(label="Help", menu=help_menu)

        self.config(menu=menu_bar)

    def toggle_fullscreen(self):
        """Toggle fullscreen mode."""
        self.is_fullscreen = not self.is_fullscreen
        self.attributes("-fullscreen", self.is_fullscreen)
        self.geometry("1920x1080" if self.is_fullscreen else "1800x1000")
        self.update_layout()

    def exit_fullscreen(self):
        """Exit fullscreen and return to normal size."""
        self.is_fullscreen = False
        self.attributes("-fullscreen", False)
        self.geometry("1800x1000")  # Restore to smaller size
        self.update_layout()  # Call without passing self explicitly

    def update_layout(self):
        """Adjust layout dynamically based on fullscreen mode."""
        if self.is_fullscreen:
            self.left_frame.config(width=300)  # Adjust width for fullscreen
        else:
            self.left_frame.config(width=200)  # Adjust width for normal mode

    #contact list function
    def contact_list(self):
        """Display the Contact List section."""
        self.right_frame.pack(side="right", fill="both", expand=True)
        for widget in self.right_frame.winfo_children():
            widget.destroy()

        # Title (Aligned to the left)
        title_label = tk.Label(self.right_frame, text="Contact List", font=("tahoma", 18, "bold"), bg="#F8F8F8", fg="black", anchor="w")
        title_label.pack(anchor="w", padx=10, pady=10)

        # Search Box (Aligned to the left)
        search_frame = tk.Frame(self.right_frame, bg="#F8F8F8")
        search_frame.pack(anchor="w", padx=10, pady=5)

        search_label = tk.Label(search_frame, text="Search by Employee ID:", font=("tahoma", 12), bg="#F8F8F8", fg="black")
        search_label.pack(side="left", padx=5)

        self.search_entry = ttk.Entry(search_frame, width=30)
        self.search_entry.pack(side="left", padx=5)
        self.search_entry.bind("<Return>", lambda event: self.search_employee())  # Bind Enter key to search

        search_button = tk.Button(search_frame, text="Search", font=("tahoma", 10, "bold"), bg="#000000", fg="white",
                                   command=self.search_employee)
        search_button.pack(side="left", padx=5)

        # Results Display
        self.results_frame = tk.Frame(self.right_frame, bg="#F8F8F8")
        self.results_frame.pack(fill="both", expand=True, padx=10, pady=10, anchor="w")

        # Check if the logged-in user is in "Support" or "Human Resources" positions
        logged_in_position = self.user_data.get("position", "")
        if logged_in_position in ["Support", "Human Resources"]:
            # Save and Reset Buttons (Aligned to the left)
            self.button_frame = tk.Frame(self.results_frame, bg="#F8F8F8")
            self.button_frame.pack(anchor="w", pady=10)

    def search_employee(self):
        """Search for an employee by Employee ID."""
        employee_id = self.search_entry.get().strip()
        if not employee_id:
            messagebox.showerror("Error", "Please enter an Employee ID to search.")
            return

        # Load users from the JSON file
        try:
            with open(r'D:\Class\Interact_Prog\Proj\users.json', 'r') as file:
                users = json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            messagebox.showerror("Error", "Unable to load employee data.")
            return

        # Find the employee by Employee ID
        employee = next((user for user in users.values() if user.get("employee_id") == employee_id), None)

        if not employee:
            messagebox.showerror("Error", "Employee not found.")
            return

        # Clear the results frame
        for widget in self.results_frame.winfo_children():
            widget.destroy()

        # Recreate the button frame to avoid referencing a destroyed widget
        self.button_frame = tk.Frame(self.results_frame, bg="#F8F8F8")
        self.button_frame.pack(anchor="w", pady=10)

        # Display employee information
        self.editable_entries = {}  # Store editable entries for saving
        allowed_keys = ["position", "first name", "email"]  # Keys visible to non-Support/HR users
        is_restricted = self.user_data.get("position") not in ["Support", "Human Resources"]

        for key, value in employee.items():
            if is_restricted and key not in allowed_keys:
                continue  # Skip keys not allowed for restricted users

            row_frame = tk.Frame(self.results_frame, bg="#F8F8F8", padx=10, pady=5)
            row_frame.pack(anchor="w", fill="x", pady=2)

            label = tk.Label(row_frame, text=f"{key.capitalize()}:", font=("Poppins", 12), bg="#F8F8F8", fg="black")
            label.pack(side="left", padx=5)

            if key == "profile_picture":
                # Display emoji as a label
                emoji_label = tk.Label(row_frame, text=value, font=("Poppins", 12), bg="#F8F8F8", fg="black")
                emoji_label.pack(side="left", padx=5)
            else:
                entry = ttk.Entry(row_frame, width=40, font=("Poppins", 12))
                entry.insert(0, value)
                entry.pack(side="left", padx=5)
                self.editable_entries[key] = entry

                # Disable the entry if the user is restricted
                if is_restricted:
                    entry.config(state="disabled")

        # Create Save and Reset buttons dynamically after a successful search
        if self.user_data.get("position") in ["Support", "Human Resources"]:
            save_button = tk.Button(self.button_frame, text="Save", font=("Poppins", 11, "bold"), bg="black", fg="white",
                                    command=lambda: self.save_employee_data(employee_id))
            save_button.pack(side="left", padx=5)

            reset_button = tk.Button(self.button_frame, text="Reset", font=("Poppins", 11, "bold"), bg="orange", fg="white",
                                     command=lambda: self.reset_employee_data(employee_id))
            reset_button.pack(side="left", padx=5)

    #approve function
    def show_approve(self):
        """Display the Request & Approve section with separate panels for requests and approvals."""
        self.right_frame.pack(side="right", fill="both", expand=True)
        for widget in self.right_frame.winfo_children():
            widget.destroy()

        # Split into two panels: Request (left) and Approve (right)
        request_panel = tk.Frame(self.right_frame, bg="#F8F8F8", width=450)
        request_panel.pack(side="left", fill="both", expand=True, padx=10, pady=10)

        approve_panel = tk.Frame(self.right_frame, bg="#F8F8F8", width=450)
        approve_panel.pack(side="right", fill="both", expand=True, padx=10, pady=10)

        # Request Section
        self.setup_request_section(request_panel)

        # Approve Section
        self.setup_approve_section(approve_panel)

    def setup_request_section(self, parent):
        """Set up the Request section."""
        tk.Label(parent, text="Request", font=("Arial", 16, "bold"), bg="#F8F8F8").pack(anchor="w", padx=10, pady=10)

        # To Box
        to_frame = tk.Frame(parent, bg="#F8F8F8")
        to_frame.pack(anchor="w", padx=10, pady=5)
        tk.Label(to_frame, text="To:", font=("Arial", 12), bg="#F8F8F8").pack(side="left")
        self.to_combobox = ttk.Combobox(to_frame, font=("Arial", 12))
        self.to_combobox['values'] = self.get_employee_ids()
        self.to_combobox.pack(side="left", padx=10)
        self.to_combobox.bind("<<ComboboxSelected>>", self.update_to_name)

        self.to_name_label = tk.Label(to_frame, text="", font=("Arial", 12), bg="#F8F8F8", fg="blue")
        self.to_name_label.pack(side="left")

        # CC Box
        cc_frame = tk.Frame(parent, bg="#F8F8F8")
        cc_frame.pack(anchor="w", padx=10, pady=5)
        self.cc_var = tk.BooleanVar()
        cc_checkbox = tk.Checkbutton(cc_frame, text="CC", variable=self.cc_var, bg="#F8F8F8", command=self.toggle_cc)
        cc_checkbox.pack(side="left")

        self.cc_combobox = ttk.Combobox(cc_frame, font=("Arial", 12), state="disabled")
        self.cc_combobox['values'] = self.get_employee_ids()
        self.cc_combobox.pack(side="left", padx=10)
        self.cc_combobox.bind("<<ComboboxSelected>>", self.update_cc_name)

        self.cc_name_label = tk.Label(cc_frame, text="", font=("Arial", 12), bg="#F8F8F8", fg="blue")
        self.cc_name_label.pack(side="left")

        # Header Box
        tk.Label(parent, text="Header:", font=("Arial", 12), bg="#F8F8F8").pack(anchor="w", padx=10, pady=5)
        self.header_entry = ttk.Entry(parent, font=("Arial", 12), width=50)
        self.header_entry.pack(anchor="w", padx=10, pady=5)

        # Detail Box
        tk.Label(parent, text="Detail:", font=("Arial", 12), bg="#F8F8F8").pack(anchor="w", padx=10, pady=5)
        self.detail_text = tk.Text(parent, font=("Arial", 12), height=10, width=50)
        self.detail_text.pack(anchor="w", padx=10, pady=5)

        # File Attachment
        tk.Label(parent, text="Attachment:", font=("Arial", 12), bg="#F8F8F8").pack(anchor="w", padx=10, pady=5)
        attachment_frame = tk.Frame(parent, bg="#F8F8F8")
        attachment_frame.pack(anchor="w", padx=10, pady=5)

        self.attachment_label = tk.Label(attachment_frame, text="No file selected", font=("Arial", 10), bg="#F8F8F8", fg="gray")
        self.attachment_label.pack(side="left", padx=5)

        browse_button = tk.Button(attachment_frame, text="Browse", font=("Arial", 10), bg="blue", fg="white",
                                   command=self.browse_file)
        browse_button.pack(side="left", padx=5)

        # Send Button
        send_button = tk.Button(parent, text="Send Request", font=("Arial", 12, "bold"), bg="black", fg="white",
                                 command=self.send_request)
        send_button.pack(anchor="center", padx=10, pady=10)

    def setup_approve_section(self, parent):
        """Set up the Approve section."""
        # Title and Refresh Button
        title_frame = tk.Frame(parent, bg="#F8F8F8")
        title_frame.pack(fill="x", padx=10, pady=5)

        tk.Label(title_frame, text="Approve Requests", font=("Arial", 16, "bold"), bg="#F8F8F8").pack(side="left", padx=10)

        refresh_button = tk.Button(title_frame, text="Refresh", font=("Arial", 10, "bold"), bg="blue", fg="white",
                                    command=self.show_approve)
        refresh_button.pack(side="right", padx=10)

        # Requests List
        requests_frame = tk.Frame(parent, bg="#F8F8F8")
        requests_frame.pack(fill="both", expand=True, padx=10, pady=10)

        # Load Requests
        requests = self.load_requests()

        # Filter requests for the approver or CC recipient
        logged_in_employee_id = self.user_data.get("employee_id")
        approver_requests = [
            req for req in requests
            if req["status"] == "Pending" and
            (req["to_id"] == logged_in_employee_id or req.get("cc_id") == logged_in_employee_id)
        ]

        # Display requests for the approver
        for request in approver_requests:
            row_frame = tk.Frame(requests_frame, bg="#F8F8F8")
            row_frame.pack(fill="x", pady=5)

            # Request Header
            tk.Label(row_frame, text=f"Header: {request['header']}", font=("Arial", 12), bg="#F8F8F8").pack(side="left", padx=10)

            # Status
            tk.Label(row_frame, text=f"Status: {request['status']}", font=("Arial", 12, "italic"), bg="#F8F8F8", fg="gray").pack(side="left", padx=10)

            # Details Button
            details_button = tk.Button(row_frame, text="Details", font=("Arial", 10), bg="blue", fg="white",
                                        command=lambda req=request: self.show_request_detail(req))
            details_button.pack(side="left", padx=10)

            # Show action buttons only for the approver, not for CC recipients
            if request["to_id"] == logged_in_employee_id:
                # Approve Button
                approve_button = tk.Button(row_frame, text="Approve", font=("Arial", 10), bg="green", fg="white",
                                            command=lambda req=request: self.handle_approval(req, "Approved", approve_button, deny_button, row_frame))
                approve_button.pack(side="left", padx=10)

                # Deny Button
                deny_button = tk.Button(row_frame, text="Deny", font=("Arial", 10), bg="red", fg="white",
                                         command=lambda req=request: self.handle_approval(req, "Denied", approve_button, deny_button, row_frame))
                deny_button.pack(side="left", padx=10)

    #def expand_fya_text(self):
        #self.fya_label.config(text=self.fya_text)
        #self.fya_label.config(height=4, wraplength=600)
        #self.id_label.config(height=4)
        #self.approve_frame.config(height=4)
    
    def accept_request(self):
        messagebox.showinfo("Approval", "Request Accepted")
    
    def deny_request(self):
        messagebox.showinfo("Approval", "Request Denied")

    def send_approval_request(self):
        messagebox.showinfo("Approval Request Sent", "Your request has been sent for approval.")
        self.right_frame.pack_forget() # Hide panel after clicking OK

    def send_request(self):
        """Handle sending a request."""
        # Get the values from the input fields
        to_id = self.to_combobox.get().strip()
        cc_id = self.cc_combobox.get().strip() if self.cc_var.get() else None
        header = self.header_entry.get().strip()
        detail = self.detail_text.get("1.0", tk.END).strip()
        attachment = getattr(self, "selected_file", None)  # Get the selected file path

        # Validate the input fields
        if not to_id:
            messagebox.showerror("Error", "Please select a recipient (To).")
            return
        if not header:
            messagebox.showerror("Error", "Please enter a header for the request.")
            return
        if not detail:
            messagebox.showerror("Error", "Please enter the details of the request.")
            return

        # Load existing requests from request_context.json
        try:
            with open(r'D:\Class\Interact_Prog\Proj\request_context.json', 'r') as file:
                requests = json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            requests = []

        # Create a new request
        new_request = {
            "from_id": self.user_data.get("employee_id"),
            "from_name": f"{self.user_data.get('first_name')} {self.user_data.get('last_name')}",
            "to_id": to_id,
            "to_name": self.get_employee_name(to_id),
            "cc_id": cc_id,
            "cc_name": self.get_employee_name(cc_id) if cc_id else None,
            "header": header,
            "detail": detail,
            "attachment": attachment,  # Include the file path
            "status": "Pending",
            "date_sent": datetime.now().strftime("%Y-%m-%d %H:%M:%S")  # Add the current date and time
        }

        # Add the new request to the list
        requests.append(new_request)

        # Save the updated requests to request_context.json
        try:
            with open(r'D:\Class\Interact_Prog\Proj\request_context.json', 'w') as file:
                json.dump(requests, file, indent=4)
            messagebox.showinfo("Success", "Request sent successfully!")

            # Clear all fields after sending the request
            self.to_combobox.set("")
            self.cc_combobox.set("")
            self.header_entry.delete(0, tk.END)
            self.detail_text.delete("1.0", tk.END)
            self.cc_var.set(False)
            self.toggle_cc()  # Disable CC combobox if it was enabled
            self.attachment_label.config(text="No file selected", fg="gray")  # Reset the attachment label
            self.selected_file = None  # Clear the selected file
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred while saving the request: {str(e)}")

    def load_requests(self):
        """Load requests from the request_context.json file."""
        try:
            with open(r'D:\Class\Interact_Prog\Proj\request_context.json', 'r') as file:
                requests = json.load(file)
                return requests
        except (FileNotFoundError, json.JSONDecodeError):
            return []

    def show_request_detail(self, request):
        """Display the details of a specific request."""
        # Create a new window to show the request details
        detail_window = tk.Toplevel(self)
        detail_window.title("Request Details")
        detail_window.geometry("600x700")
        detail_window.config(bg="#F8F8F8")

        # Display the request details
        tk.Label(detail_window, text="Request Details", font=("Arial", 16, "bold"), bg="#F8F8F8").pack(pady=10)

        # From
        tk.Label(detail_window, text=f"From: {request['from_id']} ({request['from_name']})", font=("Arial", 12), bg="#F8F8F8").pack(anchor="w", padx=10, pady=5)

        # To
        tk.Label(detail_window, text=f"To: {request['to_id']} ({request['to_name']})", font=("Arial", 12), bg="#F8F8F8").pack(anchor="w", padx=10, pady=5)

        # CC (if applicable)
        if request.get("cc_id"):
            tk.Label(detail_window, text=f"CC: {request['cc_id']} ({request['cc_name']})", font=("Arial", 12), bg="#F8F8F8").pack(anchor="w", padx=10, pady=5)

        # Date Sent
        tk.Label(detail_window, text=f"Date Sent: {request['date_sent']}", font=("Arial", 12), bg="#F8F8F8").pack(anchor="w", padx=10, pady=5)

        # Header
        tk.Label(detail_window, text=f"Header: {request['header']}", font=("Arial", 12), bg="#F8F8F8").pack(anchor="w", padx=10, pady=5)

        # Detail
        tk.Label(detail_window, text="Detail:", font=("Arial", 12, "bold"), bg="#F8F8F8").pack(anchor="w", padx=10, pady=5)
        detail_text = tk.Text(detail_window, font=("Arial", 12), height=10, width=50, wrap="word")
        detail_text.insert("1.0", request["detail"])
        detail_text.config(state="disabled")  # Make the text box read-only
        detail_text.pack(padx=10, pady=5)

        # Download Attachment Button
        if request.get("attachment"):
            download_button = tk.Button(detail_window, text="Download Attachment", font=("Arial", 12, "bold"), bg="blue", fg="white",
                                         command=lambda: self.download_attachment(request["attachment"]))
            download_button.pack(pady=10)

        # Close Button
        close_button = tk.Button(detail_window, text="Close", font=("Arial", 12, "bold"), bg="red", fg="white",
                                  command=detail_window.destroy)
        close_button.pack(pady=10)

    def download_attachment(self, file_path):
        """Download the attached file."""
        try:
            filedialog.asksaveasfilename(initialfile=file_path.split("/")[-1], title="Save File")
            messagebox.showinfo("Download", "Attachment downloaded successfully!")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to download attachment: {str(e)}")

    def approve_request(self, request):
        """Handle approving or viewing a request."""
        # Create a new window for approval actions
        approval_window = tk.Toplevel(self)
        approval_window.title("Approve Request")
        approval_window.geometry("400x300")
        approval_window.config(bg="#F8F8F8")

        # Display request details
        tk.Label(approval_window, text="Approve Request", font=("Arial", 16, "bold"), bg="#F8F8F8").pack(pady=10)
        tk.Label(approval_window, text=f"From: {request['from_id']} ({request['from_name']})", font=("Arial", 12), bg="#F8F8F8").pack(anchor="center", padx=10, pady=5)
        tk.Label(approval_window, text=f"Header: {request['header']}", font=("Arial", 12), bg="#F8F8F8").pack(anchor="center", padx=10, pady=5)
        tk.Label(approval_window, text="Detail:", font=("Arial", 12, "bold"), bg="#F8F8F8").pack(anchor="center", padx=10, pady=5)

        detail_text = tk.Text(approval_window, font=("Arial", 12), height=5, width=40, wrap="word")
        detail_text.insert("1.0", request["detail"])
        detail_text.config(state="disabled")  # Make the text box read-only
        detail_text.pack(padx=10, pady=5)

        # Approve and Deny buttons
        button_frame = tk.Frame(approval_window, bg="#F8F8F8")
        button_frame.pack(pady=10)

        approve_button = tk.Button(button_frame, text="Approve", font=("Arial", 12, "bold"), bg="green", fg="white",
                                    command=lambda: self.handle_approval(request, "Approved", approve_button, deny_button))
        approve_button.pack(side="left", padx=10)

        deny_button = tk.Button(button_frame, text="Deny", font=("Arial", 12, "bold"), bg="red", fg="white",
                                 command=lambda: self.handle_approval(request, "Denied", approval_window, approve_button, deny_button))
        deny_button.pack(side="left", padx=10)

    def handle_approval(self, request, status, approve_button, deny_button, row_frame):
        """Update the request status, save it, and handle UI updates."""
        # Update the request status
        request["status"] = status

        # Load existing requests
        try:
            with open(r'D:\Class\Interact_Prog\Proj\request_context.json', 'r') as file:
                requests = json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            requests = []

        # Update the specific request in the list
        for req in requests:
            if req["from_id"] == request["from_id"] and req["header"] == request["header"]:
                req["status"] = status
                break

        # Save the updated requests back to the file
        try:
            with open(r'D:\Class\Interact_Prog\Proj\request_context.json', 'w') as file:
                json.dump(requests, file, indent=4)
            messagebox.showinfo("Success", f"Request has been {status.lower()}!")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred while saving the request: {str(e)}")

        # Hide the buttons after action
        approve_button.pack_forget()
        deny_button.pack_forget()

        # If the request is approved or denied, remove it from the approver's view
        if status in ["Approved", "Denied"]:
            row_frame.pack_forget()

        # Refresh the Approve section
        self.show_approve()

    def deny_request(self, request):
        """Handle denying a request."""
        # Confirm the denial action
        if not messagebox.askyesno("Deny Request", "Are you sure you want to deny this request?"):
            return

        # Update the request status to "Denied"
        request["status"] = "Denied"

        # Load existing requests
        try:
            with open(r'D:\Class\Interact_Prog\Proj\request_context.json', 'r') as file:
                requests = json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            requests = []

        # Update the specific request in the list
        for req in requests:
            if req["from_id"] == request["from_id"] and req["header"] == request["header"]:
                req["status"] = "Denied"
                break

        # Save the updated requests back to the file
        try:
            with open(r'D:\Class\Interact_Prog\Proj\request_context.json', 'w') as file:
                json.dump(requests, file, indent=4)
            messagebox.showinfo("Success", "Request has been denied.")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred while saving the request: {str(e)}")

        # Refresh the Approve section
        self.show_approve()

    #helpdesk function
    def helpdesk(self):
        """Display the Helpdesk section for Support users."""
        if self.user_data.get("position") != "Support":
            messagebox.showerror("Access Denied", "You do not have permission to access the Helpdesk.")
            return

        self.right_frame.pack(side="right", fill="both", expand=True)
        for widget in self.right_frame.winfo_children():
            widget.destroy()

        # Title
        tk.Label(self.right_frame, text="Helpdesk", font=("Arial", 16, "bold"), bg="#F8F8F8").pack(pady=10)

        # Load Problems
        try:
            with open(r'D:\Class\Interact_Prog\Proj\report_problem.json', 'r') as file:
                problems = json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            problems = []

        # Display Problems Table
        for problem in problems:
            row_frame = tk.Frame(self.right_frame, bg="#F8F8F8")
            row_frame.pack(fill="x", pady=5)

            # Problem Subject
            tk.Label(row_frame, text=f"Subject: {problem['subject']}", font=("Arial", 12), bg="#F8F8F8").pack(side="left", padx=10)

            # Employee ID and Name
            tk.Label(row_frame, text=f"Employee: {problem['employee_id']} ({problem['employee_name']})", font=("Arial", 12), bg="#F8F8F8").pack(side="left", padx=10)

            # Status
            tk.Label(row_frame, text=f"Status: {problem['status']}", font=("Arial", 12), bg="#F8F8F8").pack(side="left", padx=10)

            # Details Button
            details_button = tk.Button(row_frame, text="Details", font=("Arial", 10), bg="blue", fg="white",
                                        command=lambda prob=problem: self.show_problem_details(prob))
            details_button.pack(side="left", padx=10)

            # Finish Button
            finish_button = tk.Button(row_frame, text="Finish", font=("Arial", 10), bg="green", fg="white",
                                       command=lambda prob=problem: self.finish_problem(prob))
            finish_button.pack(side="left", padx=10)

    def finish_problem(self, problem):
        """Mark a problem as finished and save it in report_problem.json."""
        try:
            # Load existing problems
            with open(r'D:\Class\Interact_Prog\Proj\report_problem.json', 'r') as file:
                problems = json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            problems = []

        # Remove the problem from the active list
        problems = [p for p in problems if p != problem]

        # Save the updated list back to the file
        with open(r'D:\Class\Interact_Prog\Proj\report_problem.json', 'w') as file:
            json.dump(problems, file, indent=4)

        # Save the finished problem in a separate file
        try:
            with open(r'D:\Class\Interact_Prog\Proj\finished_problems.json', 'r') as file:
                finished_problems = json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            finished_problems = []

        finished_problems.append(problem)

        with open(r'D:\Class\Interact_Prog\Proj\finished_problems.json', 'w') as file:
            json.dump(finished_problems, file, indent=4)

        messagebox.showinfo("Success", "Problem marked as finished.")
        self.helpdesk()
        
    def show_problem_details(self, problem):
        """Display the details of a specific problem."""
        # Create a new window to show the problem details
        detail_window = tk.Toplevel(self)
        detail_window.title("Problem Details")
        detail_window.geometry("600x400")
        detail_window.config(bg="#F8F8F8")

        # Title
        tk.Label(detail_window, text="Problem Details", font=("Arial", 16, "bold"), bg="#F8F8F8").pack(pady=10)

        # Subject
        tk.Label(detail_window, text=f"Subject: {problem['subject']}", font=("Arial", 12), bg="#F8F8F8").pack(anchor="w", padx=10, pady=5)

        # Employee ID and Name
        tk.Label(detail_window, text=f"Employee: {problem['employee_id']} ({problem['employee_name']})", font=("Arial", 12), bg="#F8F8F8").pack(anchor="w", padx=10, pady=5)

        # Date Reported
        tk.Label(detail_window, text=f"Date Reported: {problem['date_reported']}", font=("Arial", 12), bg="#F8F8F8").pack(anchor="w", padx=10, pady=5)

        # Status
        tk.Label(detail_window, text=f"Status: {problem['status']}", font=("Arial", 12), bg="#F8F8F8").pack(anchor="w", padx=10, pady=5)

        # Details
        tk.Label(detail_window, text="Details:", font=("Arial", 12, "bold"), bg="#F8F8F8").pack(anchor="w", padx=10, pady=5)
        detail_text = tk.Text(detail_window, font=("Arial", 12), height=10, width=50, wrap="word")
        detail_text.insert("1.0", problem["details"])
        detail_text.config(state="disabled")  # Make the text box read-only
        detail_text.pack(padx=10, pady=5)

        # Close Button
        close_button = tk.Button(detail_window, text="Close", font=("Arial", 12, "bold"), bg="red", fg="white",
                                  command=detail_window.destroy)
        close_button.pack(pady=10)

    #report function   
    def show_report(self):
        """Display the Report section."""
        self.right_frame.pack(side="right", fill="both", expand=True)
        for widget in self.right_frame.winfo_children():
            widget.destroy()

        # Title
        tk.Label(self.right_frame, text="Report a Problem", font=("Arial", 16, "bold"), bg="#F8F8F8").pack(anchor="w", padx=20, pady=10)

        # Subject Dropdown
        tk.Label(self.right_frame, text="Subject:", font=("Arial", 12), bg="#F8F8F8").pack(anchor="w", padx=20, pady=5)
        self.subject_combobox = ttk.Combobox(self.right_frame, font=("Arial", 12))
        self.subject_combobox['values'] = ["Hardware", "Software", "Network", "Other"]
        self.subject_combobox.pack(anchor="w", padx=20, pady=5)

        # Details Text Box
        tk.Label(self.right_frame, text="Details:", font=("Arial", 12), bg="#F8F8F8").pack(anchor="w", padx=20, pady=5)
        self.details_text = tk.Text(self.right_frame, font=("Arial", 12), height=10, width=60)
        self.details_text.pack(anchor="w", padx=20, pady=5)

        # Send Button
        send_button = tk.Button(self.right_frame, text="Send", font=("Arial", 12, "bold"), bg="black", fg="white",
                                 command=self.send_report)
        send_button.pack(anchor="w", padx=20,pady=10)

    def send_report(self):
        """Send the problem report."""
        subject = self.subject_combobox.get().strip()
        details = self.details_text.get("1.0", tk.END).strip()
        employee_id = self.user_data.get("employee_id")
        employee_name = f"{self.user_data.get('first_name')} {self.user_data.get('last_name')}"

        # Validate input
        if not subject:
            messagebox.showerror("Error", "Please select a subject.")
            return
        if not details:
            messagebox.showerror("Error", "Please enter the details.")
            return

        # Load existing problems
        try:
            with open(r'D:\Class\Interact_Prog\Proj\report_problem.json', 'r') as file:
                problems = json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            problems = []

        # Add the new problem
        new_problem = {
            "subject": subject,
            "details": details,
            "employee_id": employee_id,
            "employee_name": employee_name,  # Add employee name
            "status": "Pending",
            "date_reported": datetime.now().strftime("%Y-%m-%d %H:%M:%S")  # Add the current date and time
        }
        problems.append(new_problem)

        # Save the updated list
        with open(r'D:\Class\Interact_Prog\Proj\report_problem.json', 'w') as file:
            json.dump(problems, file, indent=4)

        messagebox.showinfo("Success", "Your report has been sent.")
        self.right_frame.pack_forget()

    #logout function
    def logout(self):
        if messagebox.askyesno("Log Out", "Are you sure you want to log out?"):
            self.destroy()
            EmployeeSystem().run()

    def get_employee_ids(self):
        """Retrieve all employee IDs from users.json."""
        try:
            with open(r'D:\Class\Interact_Prog\Proj\users.json', 'r') as file:
                users = json.load(file)
                return [user["employee_id"] for user in users.values()]
        except (FileNotFoundError, json.JSONDecodeError):
            return []

    def update_to_name(self, event):
        """Update the name label for the selected 'To' employee."""
        selected_id = self.to_combobox.get()
        self.to_name_label.config(text=self.get_employee_name(selected_id))

    def update_cc_name(self, event):
        """Update the name label for the selected 'CC' employee."""
        selected_id = self.cc_combobox.get()
        self.cc_name_label.config(text=self.get_employee_name(selected_id))

    def toggle_cc(self):
        """Enable or disable the CC combobox based on the checkbox."""
        if self.cc_var.get():
            self.cc_combobox.config(state="normal")
        else:
            self.cc_combobox.config(state="disabled")
            self.cc_name_label.config(text="")

    def get_employee_name(self, employee_id):
        """Retrieve the name of an employee by their ID."""
        try:
            with open(r'D:\Class\Interact_Prog\Proj\users.json', 'r') as file:
                users = json.load(file)
                for user in users.values():
                    if user["employee_id"] == employee_id:
                        return f"{user['first_name']} {user['last_name']}"
        except (FileNotFoundError, json.JSONDecodeError):
            return "Unknown"
        return "Unknown"

    def browse_file(self):
        """Open a file dialog to select a file."""
        file_types = [
            ("Text Files", "*.txt"),
            ("Image Files", "*.jpeg;*.jpg;*.png"),
            ("Audio Files", "*.mp3"),
            ("Video Files", "*.mp4"),
            ("All Files", "*.*")
        ]
        file_path = filedialog.askopenfilename(title="Select a File", filetypes=file_types)

        if file_path:
            self.attachment_label.config(text=file_path, fg="black")  # Update the label with the selected file path
            self.selected_file = file_path  # Store the file path for further processing
        else:
            self.attachment_label.config(text="No file selected", fg="gray")
            self.selected_file = None

    def show_profile_info(self):
        """Display the user's profile information."""
        profile_window = tk.Toplevel(self)
        profile_window.title("Profile Information")
        profile_window.geometry("400x400")
        profile_window.config(bg="#F8F8F8")

        # Title
        tk.Label(profile_window, text="Profile Information", font=("Arial", 16, "bold"), bg="#F8F8F8").pack(pady=10)

        # Display user details
        for key, value in self.user_data.items():
            row_frame = tk.Frame(profile_window, bg="#F8F8F8")
            row_frame.pack(anchor="w", padx=10, pady=5)

            tk.Label(row_frame, text=f"{key.capitalize()}: ", font=("Arial", 12, "bold"), bg="#F8F8F8").pack(side="left")
            tk.Label(row_frame, text=value if value else "", font=("Arial", 12), bg="#F8F8F8").pack(side="left")

        # Close Button
        close_button = tk.Button(profile_window, text="Close", font=("Arial", 12, "bold"), bg="red", fg="white",
                                  command=profile_window.destroy)
        close_button.pack(pady=20)

    def save_employee_data(self, employee_id):
        """Save the edited employee data."""
        try:
            # Load the users from the JSON file
            with open(r'D:\Class\Interact_Prog\Proj\users.json', 'r') as file:
                users = json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            messagebox.showerror("Error", "Unable to load employee data.")
            return

        # Find the user by employee_id
        user_email = None
        for email, user_data in users.items():
            if user_data.get("employee_id") == employee_id:
                user_email = email
                break

        if not user_email:
            messagebox.showerror("Error", f"Employee with ID {employee_id} not found.")
            return

        # Update the employee data with the edited values
        for key, entry in self.editable_entries.items():
            users[user_email][key] = entry.get()

        # Save the updated data back to the JSON file
        try:
            with open(r'D:\Class\Interact_Prog\Proj\users.json', 'w') as file:
                json.dump(users, file, indent=4)
            messagebox.showinfo("Success", "Employee data saved successfully.")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save employee data: {str(e)}")

    def reset_employee_data(self, employee_id):
        """Reset the employee data to the last saved state."""
        self.search_employee()  # Reload the employee data from the JSON file
        messagebox.showinfo("Reset", "Employee data has been reset to the last saved state.")

    def start_drag(self, event):
        """Start dragging the emoji."""
        self.emoji_label._drag_start_x = event.x
        self.emoji_label._drag_start_y = event.y

    def do_drag(self, event):
        """Perform the drag operation."""
        if hasattr(self.emoji_label, "_drag_start_x") and hasattr(self.emoji_label, "_drag_start_y"):
            x = self.emoji_label.winfo_x() - self.emoji_label._drag_start_x + event.x
            y = self.emoji_label.winfo_y() - self.emoji_label._drag_start_y + event.y
            self.emoji_label.place(x=x, y=y)
        else:
            # If attributes are not set, ignore the drag
            return

    def change_emoji(self):
        """Randomly change the emoji and update the profile picture in users.json."""
        emojis = ["😀", "😄", "😁", "😆", "😅", "😂", "🤣", "😊", "😇", "🙂", "🙃", "😉", "😌", "😍", "🥰", "😘", "😗", "😙", "😚"
                  , "😎", "🤓", "😇", "🥳", "😴", "🤖", "👻", "🐱", "🐶", "🦄"]
        new_emoji = random.choice(emojis)
        self.emoji_label.config(text=new_emoji)  # Update the emoji label

        # Update the profile picture in user_data
        self.user_data["profile_picture"] = new_emoji

        # Save the updated profile picture to users.json
        try:
            with open(r'D:\Class\Interact_Prog\Proj\users.json', 'r') as file:
                users = json.load(file)
            email = self.user_data.get("email", "")
            if email in users:
                users[email]["profile_picture"] = new_emoji
            with open(r'D:\Class\Interact_Prog\Proj\users.json', 'w') as file:
                json.dump(users, file, indent=4)
        except (FileNotFoundError, json.JSONDecodeError):
            messagebox.showerror("Error", "Unable to update profile picture.")

    def reset_emoji_position(self):
        """Reset the emoji's position to its original location."""
        self.emoji_label.place(x=self.emoji_original_x, y=self.emoji_original_y)  # Reset to original position

if __name__ == "__main__":
    user_data = {}
    app = MainPage(user_data)


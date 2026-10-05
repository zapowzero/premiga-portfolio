import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
from tkinter import *
import re
import json
from PIL import Image, ImageTk
from tkcalendar import Calendar


class EmployeeSystem:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("MYP")
        self.root.geometry("1000x1000")
        
        # Define positions and their ID ranges
        self.positions = {
            "Support": range(1001, 2000),
            "Board": range(2001, 3000),
            "Human Resources": range(3001, 4000),
            "Manager": range(4001, 5000),
            "Worker": range(5001, 6000)
        }
        
        # Load and set the background image
        self.set_background_image()

        self.setup_login_frame()

    def set_background_image(self):
        # Load the image
        image_path = r"D:\Class\Interact_Prog\Proj\CMS.webp"
        bg_image = Image.open(image_path)
        bg_image = bg_image.resize((1000, 1000), Image.Resampling.LANCZOS)  # Resize to fit the window
        self.bg_photo = ImageTk.PhotoImage(bg_image)

        # Create a label to display the image
        bg_label = tk.Label(self.root, image=self.bg_photo)
        bg_label.place(x=0, y=0, relwidth=1, relheight=1)  # Cover the entire window

    def setup_login_frame(self):
        # Load the image
        image_path = r"D:\Class\Interact_Prog\Proj\CMS.webp"
        bg_image = Image.open(image_path)
        bg_image = bg_image.resize((1000, 1000), Image.Resampling.LANCZOS)  # Resize to fit the window
        self.bg_photo = ImageTk.PhotoImage(bg_image)

        # Create a label to display the image
        bg_label = tk.Label(self.root, image=self.bg_photo)
        bg_label.place(x=0, y=0, relwidth=1, relheight=1)  # Cover the entire window

    def setup_login_frame(self):
    # Create the login frame with the original color scheme but modern design
        self.login_frame = tk.Frame(self.root, bg="#FFC07C", width=500, height=650, 
                                highlightbackground="black", highlightthickness=2, 
                                bd=0, relief="flat")
        self.login_frame.place(x=450, y=200)
        self.login_frame.propagate(False)

    # Login Title
        title_label = tk.Label(self.login_frame, text="Member Login", font=("Poppins", 27, "bold"), 
                           bg="#FFC07C", fg="black")
        title_label.place(x=127, y=60)

        welcome_label = tk.Label(self.login_frame, text="Welcome to Make Your Problem", 
                             font=("Poppins", 12), bg="#FFC07C", fg="black")
        welcome_label.place(x=133, y=105)

    # Login Fields
        self.entries = {}
        fields = ["Employee ID or Email :", "Password :"]
        for i, field in enumerate(fields):
        # Field Label
            label = tk.Label(self.login_frame, text=field, font=("Poppins", 12), 
                         bg="#FFC07C", fg="black", anchor="w")
            label.place(x=100, y=190 + (i * 90))

        # Entry Field
            entry = ttk.Entry(self.login_frame, width=30, font=("Poppins", 12), 
                          show="*" if "Password" in field else "")
            entry.place(x=100, y=220 + (i * 90), height=35)
            self.entries[field] = entry

        # Bind Enter key to trigger login for each entry
            entry.bind("<Return>", lambda event: self.login())

    # Login Button
        login_button = tk.Button(self.login_frame, text="Sign In", font=("Poppins", 12, "bold"), 
                                bg="#000000", fg="white", width=30, bd=0, 
                                activebackground="#333333", activeforeground="white", 
                                command=self.login)
        login_button.place(x=110, y=450, height=40)
        # Register Link
        regis_label = tk.Label(self.login_frame, text="Don't have an account yet? , Register", 
                               font=("Poppins", 10), fg="#007BFF", bg="#FFC07C", cursor="hand2")
        regis_label.place(x=150, y=510)
        regis_label.bind("<Button-1>", lambda _: self.show_register_frame())

    def setup_register_frame(self):
    # Create the register frame with a more intense orange background and black border
        self.register_frame = tk.Frame(self.root, bg="#FFC07C", width=500, height=800,  # Increased height
                                   highlightbackground="black", highlightthickness=2)
        self.register_frame.place(x=450, y=50)  # Adjusted position
        self.register_frame.propagate(False)

    # Progress Bar
        self.progress_var = tk.IntVar(value=0)  # Initialize progress at 0%
        self.progress_style = ttk.Style()
        self.progress_style.theme_use('default')
        self.progress_style.configure("Red.Horizontal.TProgressbar", troughcolor="#FFC07C", background="red")
        self.progress_style.configure("Green.Horizontal.TProgressbar", troughcolor="#FFC07C", background="green")

        self.progress_bar = ttk.Progressbar(self.register_frame, orient="horizontal", length=380, mode="determinate", 
                                       variable=self.progress_var, style="Red.Horizontal.TProgressbar")
        self.progress_bar.place(x=60, y=20)  # Centered within the frame

    # Progress Percentage Label
        self.progress_label = tk.Label(self.register_frame, text="0%", font=("Poppins", 10), bg="#FFC07C", fg="black")
        self.progress_label.place(x=450, y=20)  # Positioned to the right of the progress bar

    # Register Title
        title_label = tk.Label(self.register_frame, text="Register", font=("Poppins", 18, "bold"), bg="#FFC07C", fg="black")
        title_label.place(x=200, y=45)

    # Position Selection
        position_label = tk.Label(self.register_frame, text="Position :", font=("Poppins", 12), bg="#FFC07C", fg="black")
        position_label.place(x=100, y=80)

        self.position_var = tk.StringVar()
        position_combo = ttk.Combobox(self.register_frame, textvariable=self.position_var, 
                                  values=list(self.positions.keys()), state='readonly', font=("Poppins", 12))
        position_combo.place(x=100, y=110, width=300)
        self.position_var.trace_add('write', lambda *_: (self.validate_step("position"), self.update_employee_id()))

    # Employee ID
        employee_id_label = tk.Label(self.register_frame, text="Employee ID :", font=("Poppins", 12), bg="#FFC07C", fg="black")
        employee_id_label.place(x=100, y=150)
        self.employee_id_entry = ttk.Entry(self.register_frame, state='readonly', font=("Poppins", 12))
        self.employee_id_entry.place(x=100, y=180, width=300)

    # Name Fields
        name_label = tk.Label(self.register_frame, text="Name :", font=("Poppins", 12), bg="#FFC07C", fg="black")
        name_label.place(x=100, y=220)
        self.first_name_entry = ttk.Entry(self.register_frame, width=15, font=("Poppins", 12))
        self.first_name_entry.place(x=100, y=250)
        self.first_name_entry.insert(0, "First Name")
        self.last_name_entry = ttk.Entry(self.register_frame, width=15, font=("Poppins", 12))
        self.last_name_entry.place(x=250, y=250)
        self.last_name_entry.insert(0, "Last Name")

    # Bind Enter key to validate first and last name
        self.first_name_entry.bind("<Return>", lambda _: self.validate_step("first_name"))
        self.last_name_entry.bind("<Return>", lambda _: self.validate_step("last_name"))

    # Profile Picture Selection
        profile_label = tk.Label(self.register_frame, text="Profile Picture:", font=("Poppins", 12), bg="#FFC07C", fg="black")
        profile_label.place(x=100, y=290)

        self.profile_var = tk.StringVar(value="😀")  # Default emoji
        emojis = ["😀", "😎", "😊", "🤓", "😇", "🥳", "😴", "🤖", "👻", "🐱", "🐶", "🦄"]
        emoji_frame = tk.Frame(self.register_frame, bg="#FFC07C")
        emoji_frame.place(x=100, y=320)

        for i, emoji in enumerate(emojis):
            emoji_button = tk.Radiobutton(emoji_frame, text=emoji, variable=self.profile_var, value=emoji, 
                                      indicatoron=False, font=("Poppins", 14), bg="#FFC07C", fg="black", width=3)
            emoji_button.grid(row=i // 6, column=i % 6, padx=5, pady=5)
        self.profile_var.trace_add('write', lambda *_: self.validate_step("profile_picture"))

    # Birthday Selection
        birthday_label = tk.Label(self.register_frame, text="Birthday :", font=("Poppins", 12), bg="#FFC07C", fg="black")
        birthday_label.place(x=100, y=420)

    # Entry to display the selected birthday
        self.birthday_entry = ttk.Entry(self.register_frame, state='readonly', width=10, font=("Poppins", 12))
        self.birthday_entry.place(x=100, y=450, width=200)  # Adjusted width to make space for the button

    # Move the "Select Birthday" button to the side of the birthday_entry
        birthday_button = tk.Button(self.register_frame, text="Select", font=("Poppins", 10), bg="#000000", fg="white",
                                 command=self.open_birthday_calendar)
        birthday_button.place(x=310, y=447)  # Positioned to the right of the birthday_entry

    # Email
        email_label = tk.Label(self.register_frame, text="Email :", font=("Poppins", 12), bg="#FFC07C", fg="black")
        email_label.place(x=100, y=480)  # Adjusted y-coordinate
        self.email_entry = ttk.Entry(self.register_frame, width=10, font=("Poppins", 12))
        self.email_entry.place(x=100, y=510)  # Adjusted y-coordinate
        domain_label = tk.Label(self.register_frame, text="@myp.com", font=("Poppins", 12), bg="#FFC07C", fg="black")
        domain_label.place(x=200, y=507)  # Adjusted y-coordinate

    # Bind Enter key to validate email
        self.email_entry.bind("<Return>", lambda _: self.validate_step("email"))

    # Password
        password_label = tk.Label(self.register_frame, text="Password :", font=("Poppins", 12), bg="#FFC07C", fg="black")
        password_label.place(x=100, y=540)  # Adjusted y-coordinate
        self.password_entry = ttk.Entry(self.register_frame, show="*", font=("Poppins", 12))
        self.password_entry.place(x=100, y=570, width=300)  # Adjusted y-coordinate

    # Bind Enter key to validate password
        self.password_entry.bind("<Return>", lambda _: self.validate_step("password"))

    # Register Button
        register_button = tk.Button(self.register_frame, text="Register", font=("Poppins", 12, "bold"),
                                bg="#000000", fg="white", width=30, command=self.save_registration)
        register_button.place(x=100, y=630, height=40)  # Adjusted y-coordinate

    # Back to Login Link
        back_label = tk.Label(self.register_frame, text="Already have an account? Login",
                          font=("Poppins", 10), fg="#007BFF", bg="#FFC07C", cursor="hand2")
        back_label.place(x=160, y=680)  # Adjusted y-coordinate
        back_label.bind("<Button-1>", lambda _: self.show_login_frame())

    def show_register_frame(self):
        self.login_frame.place_forget()
        self.setup_register_frame()
        self.update_progress(0)  # Reset progress bar to 0%

    def show_login_frame(self):
        self.register_frame.destroy()
        self.login_frame.place(x=450, y=200)

    def update_employee_id(self, *_):
        selected_position = self.position_var.get()
        if (selected_position in self.positions):
            users = self.load_users()
            used_ids = set()

            for user in users.values():
                try:
                    if user.get('employee_id') and user['employee_id'].strip():
                        used_ids.add(int(user['employee_id']))
                except (ValueError, KeyError):
                    continue

            # Find the first available ID in the range for the selected position
            for emp_id in self.positions[selected_position]:
                if emp_id not in used_ids:
                    self.employee_id_entry.config(state='normal')
                    self.employee_id_entry.delete(0, tk.END)
                    self.employee_id_entry.insert(0, str(emp_id))
                    self.employee_id_entry.config(state='readonly')
                    break

    def load_users(self):
        try:
            with open(r'D:\Class\Interact_Prog\Proj\users.json', 'r') as file:
                return json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            return {}

    def validate_registration(self):
        if not self.first_name_entry.get() or not self.last_name_entry.get():
            messagebox.showerror("Error", "Please enter both first and last name")
            return False

        # Validate birthday
        try:
            if not hasattr(self, 'birthday') or not self.birthday:
                messagebox.showerror("Error", "Please select a valid birthday")
                return False

            birth_date = datetime.strptime(self.birthday, "%Y-%m-%d")
            if birth_date > datetime.now():
                messagebox.showerror("Error", "Invalid birth date")
                return False
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred while validating the birthday: {str(e)}")
            return False

        # Validate email
        email = self.email_entry.get()
        if not email or not re.match("^[a-zA-Z0-9_.-]+$", email):
            messagebox.showerror("Error", "Invalid email format")
            return False

        # Validate password
        password = self.password_entry.get()
        if len(password) < 8:
            messagebox.showerror("Error", "Password must be at least 8 characters long")
            return False
        if not re.search("[a-z]", password):
            messagebox.showerror("Error", "Password must contain at least one lowercase letter")
            return False
        if not re.search("[A-Z]", password):
            messagebox.showerror("Error", "Password must contain at least one uppercase letter")
            return False
        if not re.search("[0-9]", password):
            messagebox.showerror("Error", "Password must contain at least one number")
            return False

        return True

    def save_registration(self):
        if not self.validate_registration():
            return

        user_data = {
            "position": self.position_var.get(),
            "employee_id": self.employee_id_entry.get(),
            "first_name": self.first_name_entry.get(),
            "last_name": self.last_name_entry.get(),
            "profile_picture": self.profile_var.get(),  # Save the selected emoji
            "birthday": self.birthday,  # Use the selected birthday
            "email": f"{self.email_entry.get()}@myp.com",
            "password": self.password_entry.get()
        }

        try:
            users = self.load_users()
            email = f"{self.email_entry.get()}@myp.com"
            
            if email in users:
                messagebox.showerror("Error", "Email already registered")
                return

            users[email] = user_data
            
            # Save the updated users to the file
            with open(r'D:\Class\Interact_Prog\Proj\users.json', 'w') as file:
                json.dump(users, file, indent=4)
            
            # Reload the users from the file to ensure the latest data is available
            self.users = self.load_users()

            messagebox.showinfo("Success", "Registration successful!")
            self.show_login_frame()

        except Exception as e:
            messagebox.showerror("Error", f"An error occurred while saving: {str(e)}")

    def login(self):
        input_value = self.entries["Employee ID or Email :"].get().strip().lower()
        password = self.entries["Password :"].get().strip()

        users = self.load_users()

        # Check if the input is an Employee ID, email name, or full email
        if input_value.isdigit():  # If the input is numeric, treat it as an Employee ID
            user = next((user for user in users.values() if user.get("employee_id") == input_value), None)
        elif "@" not in input_value:  # If no '@', treat it as the email name
            email = f"{input_value}@myp.com"
            user = users.get(email)
        else:  # Otherwise, treat it as the full email
            user = users.get(input_value)

        # Validate the user and password
        if user and user.get("password") == password:
            self.show_status_popup("Login Success", f"Welcome {user.get('first_name', 'User')}!", "green")
            self.root.destroy()  # Close login window
            self.open_main_page(user)  # Open main page
        else:
            self.show_status_popup("Login Failed", "Invalid Employee ID, email, or password.", "red")

     
    def open_main_page(self, user_data):
        from main_page import MainPage
        main_app = MainPage(user_data)  # Pass user data
        main_app.mainloop()

    
    # Status Popup
    # Status Popup
    def show_status_popup(self, title, message, color):
        popup = tk.Toplevel(self.root)
        popup.title(title)
        popup.geometry("350x200")
        popup.configure(bg="#FFFFFF")  # พื้นหลังสีขาว

    # Title Label
        tk.Label(popup, text=title, font=("Poppins", 14, "bold"), bg="#FFFFFF", fg="#FF0000").pack(pady=25)

    # Date & Time Label
        tk.Label(popup, text=f"Date & Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", 
             font=("Poppins", 10, "bold"), bg="#FFFFFF", fg="#000000").pack(pady=1)

    # Message Label
        tk.Label(popup, text=message, fg="#000000", font=("Poppins", 10, "bold"), bg="#FFFFFF").pack(pady=1)

    # OK Button
        ok_button = tk.Button(popup, text="OK", command=popup.destroy, 
                          font=("Poppins", 10, "bold"), bg="#000000", fg="white", 
                          activebackground="#333333", activeforeground="white", 
                          bd=0, relief="flat", width=10)
        ok_button.pack(pady=15)


    def update_progress(self, value):
        """Update the progress bar value, change its color, and update the percentage label."""
        current_progress = self.progress_var.get()
        new_progress = current_progress + value
        if new_progress > 100:
            new_progress = 100
        self.progress_var.set(new_progress)
        self.progress_label.config(text=f"{new_progress}%")  # Update the percentage label
        if new_progress < 100:
            self.progress_style.configure("Red.Horizontal.TProgressbar", background="red")
            self.progress_bar.configure(style="Red.Horizontal.TProgressbar")
        else:
            self.progress_style.configure("Green.Horizontal.TProgressbar", background="green")
            self.progress_bar.configure(style="Green.Horizontal.TProgressbar")

    def validate_step(self, step):
        """Validate each step and update the progress bar."""
        progress_map = {
            "position": 10,
            "first_name": 15,
            "last_name": 15,
            "profile_picture": 30,
            "birthday": 10,
            "email": 10,
            "password": 10
        }

        # Track completed steps to prevent duplicate progress updates
        if not hasattr(self, 'completed_steps'):
            self.completed_steps = set()

        if step == "position" and self.position_var.get() and step not in self.completed_steps:
            self.update_progress(progress_map["position"])
            self.completed_steps.add(step)
        elif step == "first_name" and self.first_name_entry.get().strip() and step not in self.completed_steps:
            self.update_progress(progress_map["first_name"])
            self.completed_steps.add(step)
        elif step == "last_name" and self.last_name_entry.get().strip() and step not in self.completed_steps:
            self.update_progress(progress_map["last_name"])
            self.completed_steps.add(step)
        elif step == "profile_picture" and self.profile_var.get() and step not in self.completed_steps:
            self.update_progress(progress_map["profile_picture"])
            self.completed_steps.add(step)
        elif step == "birthday" and hasattr(self, 'birthday') and self.birthday and step not in self.completed_steps:
            self.update_progress(progress_map["birthday"])
            self.completed_steps.add(step)
        elif step == "email" and self.email_entry.get().strip() and step not in self.completed_steps:
            self.update_progress(progress_map["email"])
            self.completed_steps.add(step)
        elif step == "password" and len(self.password_entry.get().strip()) >= 8 and step not in self.completed_steps:
            self.update_progress(progress_map["password"])
            self.completed_steps.add(step)

    def open_birthday_calendar(self):
        """Open a popup with a calendar to select the birthday."""
        popup = tk.Toplevel(self.root)
        popup.title("Select Birthday")
        popup.geometry("400x350")
        popup.configure(bg="white")

        min_date = datetime(1955, 1, 1)
        max_date = datetime(2002, 12, 31)

        calendar = Calendar(popup, date_pattern="yyyy-mm-dd", mindate=min_date, maxdate=max_date
                            ,font=("Poppins", 10),
                    background="black", foreground="white", 
                    selectbackground="#FFA500", selectforeground="#FFFFFF",
                    headersbackground="#FFC07C", headersforeground="#000000",  # ปรับสีหัวข้อ
                    normalbackground="#FFFFFF", normalforeground="#000000",  # ปรับสีปกติ
                    weekendbackground="#FFFFFF", weekendforeground="#FF0000",  # ปรับสีวันหยุด
                    bordercolor="#000000", selectmode="day")
        calendar.pack(pady=40)

        def select_date():
            self.birthday = calendar.get_date()
            self.birthday_entry.config(state='normal')  # Enable editing temporarily
            self.birthday_entry.delete(0, tk.END)  # Clear the entry
            self.birthday_entry.insert(0, self.birthday)  # Insert the selected date
            self.birthday_entry.config(state='readonly')  # Set back to readonly
            popup.destroy()
            self.validate_step("birthday")

        select_button = tk.Button(popup, text="Select", font=("poppins", 12), bg="#000000", fg="white", command=select_date)
        select_button.pack(pady=5)

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = EmployeeSystem()
    app.run()
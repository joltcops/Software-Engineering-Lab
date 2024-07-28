import tkinter as tk
from tkinter import messagebox
import re
from datetime import datetime
import pickle

class AcademicUnit:
    class Person:
        def __init__(self, user_id, password, reg_time):
            self.user_id = user_id
            self.password = password
            self.attempts = 0
            self.active = True
            self.reg_time = reg_time

    class Teacher(Person):
        def __init__(self, user_id, password, designation, reg_time):
            super().__init__(user_id, password, reg_time)
            self.designation = designation

    class Student(Person):
        def __init__(self, user_id, password, category, reg_time):
            super().__init__(user_id, password, reg_time)
            self.category = category

    class Profile(Person):
        def __init__(self, user_id, password, name, dob, address, contact, department, roll):
            super().__init__(user_id, password, self.reg_time)
            self.name = name
            self.dob = dob
            self.address = address
            self.email = user_id
            self.contact = contact
            self.roll = roll
            self.department = department

    def __init__(self):
        self.users = []
        self.profiles = []

        self.retrieve_users_from_file()

    def retrieve_users_from_file(self):
        try:
            # Load user data from a file
            with open("user_data.pkl", "rb") as file:
                self.users = pickle.load(file)
        except FileNotFoundError:
            # Create an empty file if it doesn't exist
            with open("user_data.pkl", "wb") as file:
                pickle.dump([], file)

    def store_user_in_file(self):
        # Store user information in a file using pickle
        with open("user_data.pkl", "wb") as file:
            pickle.dump(self.users, file)

    def register_user(self, user_id, password, user_type, designation_category):
        user_type = user_type.lower()
        current_time = datetime.now().time()
        if user_type == "teacher" and self.is_valid_password(password):
            user = self.Teacher(user_id, password, designation_category, current_time)

        elif user_type == "student" and self.is_valid_password(password):
            if designation_category.upper() == 'UG' or designation_category.upper() == 'PG':
                user = self.Student(user_id, password, designation_category, current_time)
        else:
            messagebox.showerror("Error", "Invalid user type and/or password. Registration failed. Password policy:\n1. It should be within 8-12 characters long.\n2. It should contain at least one uppercase, one digit, and one lowercase.\n3. It should contain one or more special character(s) from the list [! @ # $ % & *]\n4. No blank space will be allowed.")
            return
        self.users.append(user)
        self.profiles.append(user)
        self.store_user_in_file()
        messagebox.showinfo("Success", f"User registered successfully: {user_id} ({user_type})\nRegistered on: {current_time}")

    def is_valid_password(self, password):
        # Password criteria: 8 to 12 characters, 1 uppercase, 1 lowercase, 1 digit, no blank spaces, and 1 special character
        if re.match(r'^(?=.*[A-Z])(?=.*[a-z])(?=.*\d)(?=.*[!@#$%&*])[^\s]{8,12}$', password):
            return True
        return False

    def sign_in(self, user_id, password):
        user = next((u for u in self.users if u.user_id == user_id), None)

        if user and user.active and user.password == password:
            messagebox.showinfo("Success", f"Welcome, {user_id}!")
            user.attempts = 0  # Reset the attempt counter on successful sign-in
        else:
            messagebox.showerror("Error", "Invalid credentials.")
            if user:
                user.attempts += 1
                if user.attempts >= 3:
                    user.active = False
                    messagebox.showwarning("Warning", f"Account for {user_id} deactivated due to too many wrong attempts.")

    def update_Profile(self, user_id, password, name, dob, address, contact, department, roll):
        user = next((u for u in self.profiles if u.user_id == user_id), None)
        if user and user.active and user.password == password:
            messagebox.showinfo("Success", f"Details for {user_id} updated successfully!")
            user = self.Profile(user_id, password, name, dob, address, contact, department, roll)
        else:
            messagebox.showerror("Error", "Invalid credentials. Not an authenticated user.")

    def delete_user(self, user_id):
        user = next((u for u in self.users if u.user_id == user_id), None)

        if user:
            self.users.remove(user)
            self.store_user_in_file()
            messagebox.showinfo("Success", f"User {user_id} deleted successfully.")
        else:
            messagebox.showerror("Error", f"User {user_id} not found.")

class RegisterWindow:
    def __init__(self, academic_unit):
        self.academic_unit = academic_unit
        self.register_window = tk.Toplevel(bg='coral')
        self.register_window.title("Register User")

        tk.Label(self.register_window, text="User ID (Active E Mail ID):", bg='gold', fg='brown').grid(row=0, column=0, padx=10, pady=5)
        self.user_id_entry = tk.Entry(self.register_window)
        self.user_id_entry.grid(row=0, column=1, padx=10, pady=0)

        tk.Label(self.register_window, text="Password:", bg='gold', fg='brown').grid(row=1, column=0, padx=10, pady=5)
        self.password_entry = tk.Entry(self.register_window, show="*")
        self.password_entry.grid(row=1, column=1, padx=10, pady=5)

        tk.Label(self.register_window, text="User Type [Not case sensitive]:", bg='gold', fg='brown').grid(row=2, column=0, padx=10, pady=5)
        self.user_type_entry = tk.Entry(self.register_window)
        self.user_type_entry.grid(row=2, column=1, padx=10, pady=5)

        tk.Label(self.register_window, text="Designation(for Teacher)/Category(for Student) [Not case sensitive]:", bg='gold', fg='brown').grid(row=3, column=0, padx=10, pady=5)
        self.designation_category_entry = tk.Entry(self.register_window)
        self.designation_category_entry.grid(row=3, column=1, padx=10, pady=5)

        tk.Button(self.register_window, text="Register", command=self.register_user, bg='gold', fg='brown').grid(row=4, column=1, pady=10)
    def register_user(self):
        user_id = self.user_id_entry.get()
        password = self.password_entry.get()
        user_type = self.user_type_entry.get()
        designation_category = self.designation_category_entry.get()

        self.academic_unit.register_user(user_id, password, user_type, designation_category)
        self.register_window.destroy()

class SignInWindow:
    def __init__(self, academic_unit):
        self.academic_unit = academic_unit
        self.sign_in_window = tk.Toplevel(bg='khaki')
        self.sign_in_window.title("Sign In")

        tk.Label(self.sign_in_window, text="User ID:", fg='darkviolet', bg='lemonchiffon').grid(row=0, column=0, padx=10, pady=5)
        self.sign_in_user_id_entry = tk.Entry(self.sign_in_window)
        self.sign_in_user_id_entry.grid(row=0, column=1, padx=10, pady=5)

        tk.Label(self.sign_in_window, text="Password:", fg='darkviolet', bg='lemonchiffon').grid(row=1, column=0, padx=10, pady=5)
        self.sign_in_password_entry = tk.Entry(self.sign_in_window, show="*")
        self.sign_in_password_entry.grid(row=1, column=1, padx=10, pady=5)

        tk.Button(self.sign_in_window, text="Sign In", command=self.sign_in, fg='darkviolet', bg='lemonchiffon').grid(row=2, column=1, pady=10)
        

    def sign_in(self):
        user_id = self.sign_in_user_id_entry.get()
        password = self.sign_in_password_entry.get()

        self.academic_unit.sign_in(user_id, password)
        self.sign_in_window.destroy()

class UpdateProfileWindow:
    def __init__(self, academic_unit):
        self.academic_unit = academic_unit
        self.update_profile_window = tk.Toplevel(bg='aqua')
        self.update_profile_window.title("Update Profile")

        tk.Label(self.update_profile_window, text="Enter User ID:", bg='greenyellow', fg='fuchsia').grid(row=0, column=0, padx=10, pady=5)
        self.profile_id_entry = tk.Entry(self.update_profile_window)
        self.profile_id_entry.grid(row=0, column=1, padx=10, pady=0)

        tk.Label(self.update_profile_window, text="Enter Password:", bg='greenyellow', fg='fuchsia').grid(row=1, column=0, padx=10, pady=5)
        self.profile_pass_entry = tk.Entry(self.update_profile_window, show="*")
        self.profile_pass_entry.grid(row=1, column=1, padx=10, pady=0)

        tk.Label(self.update_profile_window, text="Name:", bg='greenyellow', fg='fuchsia').grid(row=2, column=0, padx=10, pady=5)
        self.profile_name_entry = tk.Entry(self.update_profile_window)
        self.profile_name_entry.grid(row=2, column=1, padx=10, pady=0)

        tk.Label(self.update_profile_window, text="Date of Birth:", bg='greenyellow', fg='fuchsia').grid(row=3, column=0, padx=10, pady=5)
        self.profile_dob_entry = tk.Entry(self.update_profile_window)
        self.profile_dob_entry.grid(row=3, column=1, padx=10, pady=0)

        tk.Label(self.update_profile_window, text="Address:", bg='greenyellow', fg='fuchsia').grid(row=4, column=0, padx=10, pady=5)
        self.profile_addr_entry = tk.Entry(self.update_profile_window)
        self.profile_addr_entry.grid(row=4, column=1, padx=10, pady=0)

        tk.Label(self.update_profile_window, text="Contact:", bg='greenyellow', fg='fuchsia').grid(row=5, column=0, padx=10, pady=5)
        self.profile_cont_entry = tk.Entry(self.update_profile_window)
        self.profile_cont_entry.grid(row=5, column=1, padx=10, pady=0)

        tk.Label(self.update_profile_window, text="Roll No.:", bg='greenyellow', fg='fuchsia').grid(row=6, column=0, padx=10, pady=5)
        self.profile_roll_entry = tk.Entry(self.update_profile_window)
        self.profile_roll_entry.grid(row=6, column=1, padx=10, pady=0)

        tk.Label(self.update_profile_window, text="Department:", bg='greenyellow', fg='fuchsia').grid(row=7, column=0, padx=10, pady=5)
        self.profile_dept_entry = tk.Entry(self.update_profile_window)
        self.profile_dept_entry.grid(row=7, column=1, padx=10, pady=0)

        tk.Button(self.update_profile_window, text="Authenticate Yourself", command=self.update_prf, bg='greenyellow', fg='fuchsia').grid(row=8, column=1, pady=10)

    def update_prf(self):
        user_id = self.profile_id_entry.get()
        password = self.profile_pass_entry.get()
        name = self.profile_name_entry.get()
        dob = self.profile_dob_entry.get()
        address = self.profile_addr_entry.get()
        contact = self.profile_cont_entry.get()
        department = self.profile_dept_entry.get()
        roll = self.profile_roll_entry.get()

        self.academic_unit.update_Profile(user_id, password, name, dob, address, contact, department, roll)
        self.update_profile_window.destroy()

class DeleteUserWindow:
    def __init__(self, academic_unit):
        self.academic_unit = academic_unit
        self.delete_user_window = tk.Toplevel(bg='plum')
        self.delete_user_window.title("Delete User")

        tk.Label(self.delete_user_window, text="Enter User ID to be deleted:", bg='white', fg='red').grid(row=0, column=0, padx=10, pady=5)
        self.delete_id_entry=tk.Entry(self.delete_user_window)
        self.delete_id_entry.grid(row=0, column=1, padx=10, pady=5)
        
        tk.Label(self.delete_user_window, text="Are you sure you want to delete user?", bg='white', fg='maroon').grid(row=3, column=0, pady=10)
        tk.Button(self.delete_user_window, text="Yes", command=self.delete_user, bg='crimson').grid(row=3, column=1, pady=10)

    def delete_user(self):
        user_id = self.delete_id_entry.get()
        self.academic_unit.delete_user(user_id)
        self.delete_user_window.destroy()

class AcademicUnitGUI:
    def __init__(self, master):
        self.master = master
        self.master.title("Academic Unit System")

        self.academic_unit = AcademicUnit()

        tk.Button(self.master, text="Register", command=self.open_register_window).pack()
        tk.Button(self.master, text="Sign In", command=self.open_sign_in_window).pack()
        tk.Button(self.master, text="Update Profile", command=self.open_update_profile_window).pack()
        tk.Button(self.master, text="Delete User", command=self.open_delete_user_window).pack()

    def open_register_window(self):
        RegisterWindow(self.academic_unit)

    def open_sign_in_window(self):
        SignInWindow(self.academic_unit)

    def open_update_profile_window(self):
        UpdateProfileWindow(self.academic_unit)

    def open_delete_user_window(self):
        DeleteUserWindow(self.academic_unit)

    def close_app(self):
        self.academic_unit.store_user_in_file()
        self.master.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = AcademicUnitGUI(root)
    root.protocol("WM_DELETE_WINDOW", app.close_app)
    root.mainloop()

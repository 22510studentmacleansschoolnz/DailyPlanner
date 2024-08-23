import tkinter as tk
from tkinter import messagebox, ttk, simpledialog, filedialog
from tkcalendar import Calendar
import re
import json
import os
import csv

class DailyPlanner:
    def __init__(self, master):
        self.master = master
        self.master.title("Daily Planner")
        self.master.geometry("800x600")

        # Store user credentials
        self.users = self.load_users()
        self.current_user = None
        self.tasks = {}

        self.create_signin_page()

    def load_users(self):
        if os.path.exists('users.json'):
            with open('users.json', 'r') as f:
                return json.load(f)
        return {}

    def save_users(self):
        with open('users.json', 'w') as f:
            json.dump(self.users, f)

    def load_tasks(self):
        if os.path.exists(f'{self.current_user}_tasks.json'):
            with open(f'{self.current_user}_tasks.json', 'r') as f:
                return json.load(f)
        return {}

    def save_tasks(self):
        with open(f'{self.current_user}_tasks.json', 'w') as f:
            json.dump(self.tasks, f)

    def create_signin_page(self):
        self.signin_frame = tk.Frame(self.master)
        self.signin_frame.pack(expand=True, fill='both')

        self.username_label = tk.Label(self.signin_frame, text="Username:")
        self.username_label.pack(pady=(20, 5))
        self.username_entry = tk.Entry(self.signin_frame)
        self.username_entry.pack()

        self.password_label = tk.Label(self.signin_frame, text="Password:")
        self.password_label.pack(pady=(10, 5))
        self.password_entry = tk.Entry(self.signin_frame, show="*")
        self.password_entry.pack()

        self.sign_in_button = tk.Button(self.signin_frame, text="Sign In", command=self.sign_in)
        self.sign_in_button.pack(pady=(20, 0))

        self.sign_up_button = tk.Button(self.signin_frame, text="Sign Up", command=self.create_signup_page)
        self.sign_up_button.pack(pady=(10, 0))

    def create_signup_page(self):
        self.signin_frame.destroy()
        self.signup_frame = tk.Frame(self.master)
        self.signup_frame.pack(expand=True, fill='both')

        self.email_label = tk.Label(self.signup_frame, text="Email:")
        self.email_label.pack(pady=(20, 5))
        self.email_entry = tk.Entry(self.signup_frame)
        self.email_entry.pack()

        self.new_username_label = tk.Label(self.signup_frame, text="Username:")
        self.new_username_label.pack(pady=(10, 5))
        self.new_username_entry = tk.Entry(self.signup_frame)
        self.new_username_entry.pack()

        self.new_password_label = tk.Label(self.signup_frame, text="Password:")
        self.new_password_label.pack(pady=(10, 5))
        self.new_password_entry = tk.Entry(self.signup_frame, show="*")
        self.new_password_entry.pack()

        self.confirm_password_label = tk.Label(self.signup_frame, text="Confirm Password:")
        self.confirm_password_label.pack(pady=(10, 5))
        self.confirm_password_entry = tk.Entry(self.signup_frame, show="*")
        self.confirm_password_entry.pack()

        self.create_account_button = tk.Button(self.signup_frame, text="Create Account", command=self.create_account)
        self.create_account_button.pack(pady=(20, 0))

        self.back_button = tk.Button(self.signup_frame, text="Back to Sign In", command=self.back_to_signin)
        self.back_button.pack(pady=(10, 0))

    def back_to_signin(self):
        self.signup_frame.destroy()
        self.create_signin_page()

    def create_account(self):
        email = self.email_entry.get()
        username = self.new_username_entry.get()
        password = self.new_password_entry.get()
        confirm_password = self.confirm_password_entry.get()

        # Validate email
        if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            messagebox.showerror("Error", "Invalid email address")
            return

        # Validate username (alphanumeric, 3-20 characters)
        if not re.match(r"^[a-zA-Z0-9]{3,20}$", username):
            messagebox.showerror("Error", "Username must be 3-20 alphanumeric characters")
            return

        # Validate password (minimum 8 characters)
        if len(password) < 8:
            messagebox.showerror("Error", "Password must be at least 8 characters long")
            return

        if password != confirm_password:
            messagebox.showerror("Error", "Passwords do not match")
            return

        # Save the user information
        self.users[username] = {"email": email, "password": password}
        self.save_users()

        messagebox.showinfo("Success", "Account created successfully!")
        self.back_to_signin()

    def sign_in(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        # Check the credentials against the stored users
        if username in self.users and self.users[username]["password"] == password:
            self.current_user = username
            self.tasks = self.load_tasks()
            self.signin_frame.destroy()
            self.create_planner_page()
        else:
            messagebox.showerror("Error", "Invalid username or password")

    def logout(self):
        self.current_user = None
        self.planner_frame.destroy()
        self.create_signin_page()

    def create_planner_page(self):
        self.planner_frame = tk.Frame(self.master)
        self.planner_frame.pack(expand=True, fill='both')

        # Create top frame for logout and switch user buttons
        top_frame = tk.Frame(self.planner_frame)
        top_frame.pack(side='top', fill='x')

        # Logout button in top right corner
        logout_button = tk.Button(top_frame, text="Logout", command=self.logout)
        logout_button.pack(side='right', padx=10, pady=10)

        # Switch user button to the left of logout button
        switch_user_button = tk.Button(top_frame, text="Switch User", command=self.show_user_list)
        switch_user_button.pack(side='right', padx=10, pady=10)

        # Export data button
        export_button = tk.Button(top_frame, text="Export Data", command=self.export_data)
        export_button.pack(side='right', padx=10, pady=10)

        # Import data button
        import_button = tk.Button(top_frame, text="Import Data", command=self.import_data)
        import_button.pack(side='right', padx=10, pady=10)

        # Create left and right frames
        left_frame = tk.Frame(self.planner_frame, width=400)
        left_frame.pack(side='left', fill='both', expand=True)
        right_frame = tk.Frame(self.planner_frame, width=400)
        right_frame.pack(side='right', fill='both', expand=True)

        # Calendar
        self.cal = Calendar(left_frame, selectmode='day', date_pattern='yyyy-mm-dd')
        self.cal.pack(pady=20)

        # Time dropdown
        time_frame = tk.Frame(left_frame)
        time_frame.pack(pady=10)

        hours = [f"{h:02d}" for h in range(1, 13)]
        minutes = [f"{m:02d}" for m in range(0, 60, 5)]
        am_pm = ["AM", "PM"]

        self.hour_var = tk.StringVar()
        self.minute_var = tk.StringVar()
        self.ampm_var = tk.StringVar()

        hour_dropdown = ttk.Combobox(time_frame, textvariable=self.hour_var, values=hours, width=5)
        minute_dropdown = ttk.Combobox(time_frame, textvariable=self.minute_var, values=minutes, width=5)
        ampm_dropdown = ttk.Combobox(time_frame, textvariable=self.ampm_var, values=am_pm, width=5)

        hour_dropdown.set("12")
        minute_dropdown.set("00")
        ampm_dropdown.set("PM")

        hour_dropdown.pack(side='left', padx=5)
        minute_dropdown.pack(side='left', padx=5)
        ampm_dropdown.pack(side='left', padx=5)

        # Task list
        self.task_listbox = tk.Listbox(left_frame, width=50, height=10)
        self.task_listbox.pack(pady=10)

        # Populate task list
        for date, tasks in self.tasks.items():
            for task in tasks:
                self.task_listbox.insert(tk.END, f"{date}: {task}")

        # Add task entry and buttons
        task_frame = tk.Frame(left_frame)
        task_frame.pack(fill='x', padx=10)

        self.task_entry = tk.Entry(task_frame, width=40)
        self.task_entry.pack(side='left')

        add_task_button = tk.Button(task_frame, text="Add Task", command=self.add_task)
        add_task_button.pack(side='left', padx=(10, 5))

        remove_task_button = tk.Button(task_frame, text="Remove Task", command=self.remove_task)
        remove_task_button.pack(side='left', padx=(5, 5))

        modify_task_button = tk.Button(task_frame, text="Modify Task", command=self.modify_task)
        modify_task_button.pack(side='left', padx=(5, 0))

        # Notes section
        notes_label = tk.Label(right_frame, text="Notes:")
        notes_label.pack(pady=(20, 5))
        self.notes_text = tk.Text(right_frame, width=50, height=20)
        self.notes_text.pack(pady=10)

        # Load saved notes
        self.load_notes()

        # Save button
        save_button = tk.Button(right_frame, text="Save Notes", command=self.save_notes)
        save_button.pack(pady=10)

    def show_user_list(self):
        # Remove all widgets from the main window
        for widget in self.master.winfo_children():
            widget.destroy()

        user_list_frame = tk.Frame(self.master)
        user_list_frame.pack(expand=True, fill='both')

        if len(self.users) <= 1:
            message = tk.Label(user_list_frame, text="There are no users to show here")
            message.pack(pady=20)
        else:
            for username in self.users:
                if username != self.current_user:
                    user_button = tk.Button(user_list_frame, text=username,
                                            command=lambda u=username: self.switch_to_user(u))
                    user_button.pack(pady=5)

        back_button = tk.Button(user_list_frame, text="Back to Main Page",
                                command=self.back_to_planner)
        back_button.pack(pady=20)

    def switch_to_user(self, username):
        password = simpledialog.askstring("Password", f"Enter password for {username}:", show='*')
        if password == self.users[username]["password"]:
            result = messagebox.askyesno("Warning", "Please ensure you have saved previous tasks. If you proceed, all unsaved work will be lost. Do you want to continue?")
            if result:
                self.current_user = username
                self.tasks = self.load_tasks()
                self.back_to_planner()
        else:
            messagebox.showerror("Error", "Incorrect password")

    def back_to_planner(self):
        # Destroy all widgets in the main window
        for widget in self.master.winfo_children():
            widget.destroy()
        # Create the planner page
        self.create_planner_page()

    def add_task(self):
        task = self.task_entry.get()
        if task:
            date = self.cal.get_date()
            time = f"{self.hour_var.get()}:{self.minute_var.get()} {self.ampm_var.get()}"
            datetime = f"{date} {time}"
            if date not in self.tasks:
                self.tasks[date] = []
            self.tasks[date].append(f"{time} - {task}")
            self.task_listbox.insert(tk.END, f"{datetime}: {task}")
            self.task_entry.delete(0, tk.END)
            self.save_tasks()

    def remove_task(self):
        selection = self.task_listbox.curselection()
        if selection:
            index = selection[0]
            task = self.task_listbox.get(index)
            date, time_task = task.split(': ', 1)
            if date in self.tasks:
                self.tasks[date].remove(time_task)
                if not self.tasks[date]:
                    del self.tasks[date]
            self.task_listbox.delete(index)
            self.save_tasks()

    def modify_task(self):
        selection = self.task_listbox.curselection()
        if selection:
            index = selection[0]
            task = self.task_listbox.get(index)
            date, time_task = task.split(': ', 1)
            new_task = simpledialog.askstring("Modify Task", "Enter the modified task:", initialvalue=time_task)
            if new_task:
                if date in self.tasks:
                    self.tasks[date].remove(time_task)
                    self.tasks[date].append(new_task)
                    self.task_listbox.delete(index)
                    self.task_listbox.insert(index, f"{date}: {new_task}")
                    self.save_tasks()

    def load_notes(self):
        notes_file = f'{self.current_user}_notes.txt'
        if os.path.exists(notes_file):
            with open(notes_file, 'r') as f:
                notes = f.read()
            self.notes_text.insert(tk.END, notes)

    def save_notes(self):
        notes = self.notes_text.get("1.0", tk.END)
        with open(f'{self.current_user}_notes.txt', 'w') as f:
            f.write(notes)
        messagebox.showinfo("Success", "Notes saved successfully!")

    def export_data(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".json",
                                                 filetypes=[("JSON files", "*.json"), ("CSV files", "*.csv")])
        if file_path:
            if file_path.endswith('.json'):
                self.export_json(file_path)
            elif file_path.endswith('.csv'):
                self.export_csv(file_path)

    def export_json(self, file_path):
        data = {
            'tasks': self.tasks,
            'notes': self.notes_text.get("1.0", tk.END)
        }
        with open(file_path, 'w') as f:
            json.dump(data, f, indent=2)
        messagebox.showinfo("Success", "Data exported successfully!")

    def export_csv(self, file_path):
        with open(file_path, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['Date', 'Time', 'Task'])
            for date, tasks in self.tasks.items():
                for task in tasks:
                    time, task_desc = task.split(' - ', 1)
                    writer.writerow([date, time, task_desc])
        messagebox.showinfo("Success", "Data exported successfully!")

    def import_data(self):
        file_path = filedialog.askopenfilename(filetypes=[("JSON files", "*.json"), ("CSV files", "*.csv")])
        if file_path:
            if file_path.endswith('.json'):
                self.import_json(file_path)
            elif file_path.endswith('.csv'):
                self.import_csv(file_path)

    def import_json(self, file_path):
        with open(file_path, 'r') as f:
            data = json.load(f)

        self.tasks = data['tasks']
        self.notes_text.delete("1.0", tk.END)
        self.notes_text.insert(tk.END, data['notes'])

        self.refresh_task_list()
        self.save_tasks()
        self.save_notes()
        messagebox.showinfo("Success", "Data imported successfully!")

    def import_csv(self, file_path):
        self.tasks = {}
        with open(file_path, 'r') as f:
            reader = csv.reader(f)
            next(reader)  # Skip header row
            for row in reader:
                date, time, task_desc = row
                if date not in self.tasks:
                    self.tasks[date] = []
                self.tasks[date].append(f"{time} - {task_desc}")

        self.refresh_task_list()
        self.save_tasks()
        messagebox.showinfo("Success", "Data imported successfully!")

    def refresh_task_list(self):
        self.task_listbox.delete(0, tk.END)
        for date, tasks in self.tasks.items():
            for task in tasks:
                self.task_listbox.insert(tk.END, f"{date}: {task}")

if __name__ == "__main__":
    root = tk.Tk()
    app = DailyPlanner(root)
    root.mainloop()
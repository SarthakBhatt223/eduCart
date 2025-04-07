import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import json
import os
import math

USER_FILE = "users.json"

def load_users():
    try:
        if os.path.exists(USER_FILE):
            with open(USER_FILE, "r") as file:
                return json.load(file)
        return {}
    except Exception as e:
        messagebox.showerror("Error", f"Failed to load users: {e}")
        return {}

def save_users(users):
    try:
        with open(USER_FILE, "w") as file:
            json.dump(users, file)
    except Exception as e:
        messagebox.showerror("Error", f"Failed to save users: {e}")

style = None

def set_custom_styles():
    global style
    if style is None:
        style = ttk.Style()

        style.configure("Custom.TButton", font=("Arial", 14), padding=5, relief="flat")
        style.map("Custom.TButton",
                  background=[("active", "#45a049"), ("!active", "#4CAF50")],
                  foreground=[("active", "white"), ("!active", "white")])

        style.configure("Custom.TEntry", font=("Arial", 12), relief="flat")
        style.map("Custom.TEntry",
                  fieldbackground=[("focus", "#ffffff"), ("!focus", "#f0f0f0")],
                  foreground=[("focus", "black"), ("!focus", "gray")])

def create_login_frame(root, switch_to_calculator):
    frame = tk.Frame(root, bg="#ffffff", bd=2, relief=tk.RAISED)
    frame.place(relx=0.5, rely=0.5, anchor="center")

    title_label = tk.Label(frame, text="Welcome to EduCart", font=("Arial", 24, "bold"), bg="#ffffff", fg="#333333")
    title_label.grid(row=0, column=0, columnspan=2, pady=20)

    subtitle_label = tk.Label(frame, text="Login to continue", font=("Arial", 14), bg="#ffffff", fg="#666666")
    subtitle_label.grid(row=1, column=0, columnspan=2, pady=10)

    username_frame = tk.Frame(frame, bg="#ffffff")
    username_frame.grid(row=2, column=0, columnspan=2, pady=10)

    tk.Label(username_frame, text="👤", font=("Arial", 14), bg="#ffffff", fg="#4CAF50").pack(side="left", padx=5)
    entry_username = ttk.Entry(username_frame, style="Custom.TEntry", width=25)
    entry_username.pack(side="left")
    entry_username.insert(0, "Username") 

    password_frame = tk.Frame(frame, bg="#ffffff")
    password_frame.grid(row=3, column=0, columnspan=2, pady=10)

    tk.Label(password_frame, text="🔒", font=("Arial", 14), bg="#ffffff", fg="#4CAF50").pack(side="left", padx=5)
    entry_password = ttk.Entry(password_frame, style="Custom.TEntry", width=25, show="*")
    entry_password.pack(side="left")
    entry_password.insert(0, "Password") 

    def on_entry_click(event, entry, placeholder):
        if entry.get() == placeholder:
            entry.delete(0, tk.END)
            if placeholder == "Password":
                entry.config(show="*")

    def on_focus_out(event, entry, placeholder):
        if entry.get() == "":
            entry.insert(0, placeholder)
            if placeholder == "Password":
                entry.config(show="")

    entry_username.bind("<FocusIn>", lambda e: on_entry_click(e, entry_username, "Username"))
    entry_username.bind("<FocusOut>", lambda e: on_focus_out(e, entry_username, "Username"))
    entry_password.bind("<FocusIn>", lambda e: on_entry_click(e, entry_password, "Password"))
    entry_password.bind("<FocusOut>", lambda e: on_focus_out(e, entry_password, "Password"))

    def login():
        username = entry_username.get()
        password = entry_password.get()

        if not username or not password or username == "Username" or password == "Password":
            messagebox.showerror("Error", "Please enter a valid username and password!")
            return

        if username in users and users[username] == password:
            messagebox.showinfo("Login Successful", f"Welcome, {username}!")
            switch_to_calculator(username)
        else:
            messagebox.showerror("Login Failed", "Invalid Username or Password")

    login_button = ttk.Button(frame, text="Login", style="Custom.TButton", command=login)
    login_button.grid(row=4, column=0, columnspan=2, pady=20)

    def switch_to_signin():
        new_username = simpledialog.askstring("Sign Up", "Enter a new username:")
        if new_username:
            new_password = simpledialog.askstring("Sign Up", "Enter a new password:", show="*")
            if new_password:
                users[new_username] = new_password
                save_users(users)
                messagebox.showinfo("Success", "Account created successfully!")

    signup_label = tk.Label(frame, text="Don't have an account? Sign Up", font=("Arial", 12), bg="#ffffff", fg="#4CAF50", cursor="hand2")
    signup_label.grid(row=5, column=0, columnspan=2, pady=10)
    signup_label.bind("<Button-1>", lambda e: switch_to_signin())

    # Exit button for login frame
    exit_button = ttk.Button(frame, text="Exit", style="Custom.TButton", command=root.destroy)
    exit_button.grid(row=6, column=0, columnspan=2, pady=10)

    return frame

def create_calculator_frame(root, username, switch_to_login):
    for widget in root.winfo_children():
        widget.destroy()

    top_bar = tk.Frame(root, bg="#333333")
    top_bar.pack(fill="x", pady=10)

    logout_button = ttk.Button(top_bar, text="Logout", style="Custom.TButton", command=switch_to_login)
    logout_button.pack(side="left", padx=10)

    change_details_button = ttk.Button(top_bar, text="Change User Details", style="Custom.TButton", command=lambda: change_user_details(username))
    change_details_button.pack(side="left", padx=10)

    theme_button = ttk.Button(top_bar, text="🌙", style="Custom.TButton", command=toggle_theme)
    theme_button.pack(side="right", padx=10)

    # Exit button for calculator frame
    exit_button = ttk.Button(top_bar, text="Exit", style="Custom.TButton", command=root.destroy)
    exit_button.pack(side="right", padx=10)

    display_var = tk.StringVar()
    display_var.set("0")
    display = tk.Entry(root, textvariable=display_var, font=("Arial", 36), justify="right", bd=20, relief=tk.FLAT, bg="#f0f0f0", fg="#000000")
    display.pack(fill="x", padx=10, pady=10)

    buttons_frame = tk.Frame(root, bg="#333333")
    buttons_frame.pack(fill="both", expand=True)

    buttons = [
        ('7', 0, 0), ('8', 0, 1), ('9', 0, 2), ('/', 0, 3),
        ('4', 1, 0), ('5', 1, 1), ('6', 1, 2), ('*', 1, 3),
        ('1', 2, 0), ('2', 2, 1), ('3', 2, 2), ('-', 2, 3),
        ('0', 3, 0), ('.', 3, 1), ('⌫', 3, 2), ('+', 3, 3),
        ('C', 4, 0), ('(', 4, 1), (')', 4, 2), ('=', 4, 3),
        ('√', 5, 0), ('^', 5, 1), ('log', 5, 2), ('ln', 5, 3),
        ('sin', 6, 0), ('cos', 6, 1), ('tan', 6, 2), ('π', 6, 3),
        ('!', 7, 0), ('e', 7, 1)
    ]

    for (text, row, col) in buttons:
        button = tk.Button(
            buttons_frame,
            text=text,
            font=("Arial", 20),  # Increased font size
            bg="#555555",  # Dark grey background
            fg="white",  
            bd=0,         
            relief=tk.FLAT,
            padx=20,
            pady=20,
            command=lambda t=text: button_click(t)
        )
        button.grid(row=row, column=col, sticky="nsew", padx=5, pady=5)

    def button_click(value):
        current_text = display_var.get()
        if value == 'C':
            display_var.set("0")
        elif value == '⌫':
            display_var.set(current_text[:-1] if current_text != "0" else "0")
        elif value == '=':
            try:
                result = str(eval(current_text))
                display_var.set(result)
            except Exception as e:
                display_var.set("Error")
        elif value == '√':
            try:
                result = str(math.sqrt(float(current_text)))
                display_var.set(result)
            except Exception as e:
                display_var.set("Error")
        elif value == '^':
            display_var.set(current_text + "**")
        elif value == 'π':
            display_var.set(current_text + str(math.pi))
        elif value == 'e':
            display_var.set(current_text + str(math.e))
        elif value == '!':
            try:
                result = str(math.factorial(int(float(current_text))))
                display_var.set(result)
            except Exception as e:
                display_var.set("Error")
        elif value == 'log':
            try:
                result = str(math.log10(float(current_text)))
                display_var.set(result)
            except Exception as e:
                display_var.set("Error")
        elif value == 'ln':
            try:
                result = str(math.log(float(current_text)))
                display_var.set(result)
            except Exception as e:
                display_var.set("Error")
        elif value in ['sin', 'cos', 'tan']:
            try:
                angle = float(current_text)
                if value == 'sin':
                    result = str(math.sin(math.radians(angle)))
                elif value == 'cos':
                    result = str(math.cos(math.radians(angle)))
                elif value == 'tan':
                    result = str(math.tan(math.radians(angle)))
                display_var.set(result)
            except Exception as e:
                display_var.set("Error")
        else:
            if current_text == "0" or current_text == "Error":
                display_var.set(value)
            else:
                display_var.set(current_text + value)

    for i in range(8):
        buttons_frame.grid_rowconfigure(i, weight=1)
    for j in range(4):
        buttons_frame.grid_columnconfigure(j, weight=1)

def change_user_details(username):
    new_password = simpledialog.askstring("Change Password", "Enter new password:", show="*")
    if new_password:
        users[username] = new_password
        save_users(users)
        messagebox.showinfo("Success", "Password updated successfully!")

dark_mode = False

def toggle_theme():
    global dark_mode
    dark_mode = not dark_mode
    apply_theme()

def apply_theme():
    bg_color = "#121212" if dark_mode else "#ffffff" 
    fg_color = "#ffffff" if dark_mode else "#000000"  
    button_bg = "#333333" if dark_mode else "#4CAF50" 

    # Apply theme to the root window
    root.config(bg=bg_color)

    # Apply theme to all widgets recursively
    for widget in root.winfo_children():
        apply_theme_to_widget(widget, bg_color, fg_color, button_bg)

    # Ensure the display entry field is updated
    display.config(bg=bg_color, fg=fg_color)

def apply_theme_to_widget(widget, bg_color, fg_color, button_bg):
    if isinstance(widget, (tk.Frame, tk.Label, tk.Entry, ttk.Entry, ttk.Button)):
        widget.config(bg=bg_color, fg=fg_color)
    elif isinstance(widget, tk.Button):
        widget.config(bg=button_bg, fg=fg_color)
    elif isinstance(widget, ttk.Style):
        style.configure("Custom.TButton", background=button_bg, foreground=fg_color)
        style.configure("Custom.TEntry", fieldbackground=bg_color, foreground=fg_color)

    for child in widget.winfo_children():
        apply_theme_to_widget(child, bg_color, fg_color, button_bg)

def main():
    global users, root, display
    users = load_users()

    root = tk.Tk()
    root.title("EduCart - Login")
    root.geometry("800x600")  # Larger window size
    root.configure(bg="#f0f8ff")

    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    x = (screen_width // 2) - (800 // 2)
    y = (screen_height // 2) - (600 // 2)
    root.geometry(f"800x600+{x}+{y}")

    set_custom_styles()

    def switch_to_calculator(username):
        create_calculator_frame(root, username, lambda: create_login_frame(root, switch_to_calculator))

    login_frame = create_login_frame(root, switch_to_calculator)
    login_frame.pack()

    root.mainloop()

if __name__ == "__main__":
    main()
import tkinter as tk
from tkinter import ttk

import sv_ttk

from views.LoginView import LoginView
from views.RegistrationView import RegistrationView


def open_login():
    login_window = tk.Toplevel(root)  # Create a new window for the login screen
    login_window.title("Login")  # Set the window title

    login_screen = LoginView(login_window)  # Create an instance of the LoginScreen class

    # Optionally, you can center the login window on the main window
    login_window.geometry("+{}+{}".format(
        root.winfo_rootx() + int((root.winfo_width() - login_window.winfo_width()) / 2),
        root.winfo_rooty() + int((root.winfo_height() - login_window.winfo_height()) / 2)
    ))

def on_theme_toggle():
    if sv_ttk.get_theme() == "dark":
        print("Setting theme to light")
        sv_ttk.use_light_theme()
    elif sv_ttk.get_theme() == "light":
        print("Setting theme to dark")
        sv_ttk.use_dark_theme()
    else:
        print("Not Sun Valley theme")

def open_registration():
    reg_window = tk.Toplevel(root)  # Create a new window for the login screen
    reg_window.title("Registration")  # Set the window title

    reg_screen = RegistrationView(reg_window)  # Create an instance of the LoginScreen class

    # Optionally, you can center the login window on the main window
    reg_window.geometry("+{}+{}".format(
        root.winfo_rootx() + int((root.winfo_width() - reg_window.winfo_width()) / 2),
        root.winfo_rooty() + int((root.winfo_height() - reg_window.winfo_height()) / 2)
    ))

def exit_prog() -> None:
    root.quit()

root = tk.Tk()

# Configure the main window
root.title("GUI User Authentication")
root.geometry("400x270")

# Set the dark theme as the default theme
sv_ttk.use_dark_theme()

# Create a frame for the main content
main_frame = ttk.Frame(root, padding="20")
main_frame.pack(fill="both", expand=True)

# Create the label
label = ttk.Label(main_frame, text="Select an option:")
label.pack(pady=10)

# Create the registration button
registration_button = ttk.Button(main_frame, text="Registration", command=open_registration)
registration_button.pack(pady=5)

# Create the login button
login_button = ttk.Button(main_frame, text="Login", command=open_login)
login_button.pack(pady=5)

exit_button = ttk.Button(main_frame, text="Exit", command=exit_prog)
exit_button.pack(pady=5)

# Create the theme toggle button
theme_button = ttk.Button(root, text="Toggle Theme", command=on_theme_toggle)
theme_button.pack(anchor="ne", padx=10, pady=10)

root.mainloop()
import base64
import json
import os
import random
import sqlite3
import tkinter as tk
from tkinter import messagebox, ttk

from PIL import Image, ImageTk


class LoginView:
    def __init__(self, root):
        self.root = root
        self.create_widgets()
        self.selected_images = []

    def create_widgets(self):
        # Create a frame for the login screen content
        self.login_frame = ttk.Frame(self.root, padding="20")
        self.login_frame.pack(fill="both", expand=True)

        # Create the username section frame
        username_frame = ttk.Frame(self.login_frame)
        username_frame.pack(pady=5)

        username_label = ttk.Label(username_frame, text="Username:")
        username_label.pack(side="left")
        self.username_entry = ttk.Entry(username_frame)
        self.username_entry.pack(side="left")

        # Create the login button
        login_button = ttk.Button(self.login_frame, text="Check", command=self.check_username)
        login_button.pack(pady=10)

        # Pack the login frame to make it visible
        self.login_frame.pack()

    def check_username(self):
        global username
        username = self.username_entry.get()
        password = self.fetch_password_from_database(username)

        if password:
            self.login_frame.destroy()
            self.create_password_selection(password)
        else:
            messagebox.showerror("Error", "Invalid username.")

    def fetch_password_from_database(self, username):
        # Connect to the database and fetch the password
        conn = sqlite3.connect("database.db")
        c = conn.cursor()
        c.execute("SELECT password FROM users WHERE username=?", (username,))
        password = c.fetchone()
        conn.close()
        return password[0] if password else None
    
    def create_image_dict(self, password_dict) -> list:
        image_list = []
        for _, value in password_dict.items():
            image_dict = {
                'id': int(value[:-4]),
                'image': value,
            }
            image_list.append(image_dict)
        return image_list

    def create_password_selection(self, password):
        # Create a list of image paths for password selection
        password_images = self.create_image_dict(self.decode_password(password))

        # Get additional images for selection
        additional_images = self.fetch_additional_images(self.decode_password(password))

        # Combine password images and additional images
        images = password_images + additional_images

        # Shuffle the images
        random.shuffle(images)

        # Create a frame for the image buttons
        image_buttons_frame = ttk.Frame(self.root, padding="20")
        image_buttons_frame.pack(fill="both", expand=True)

        # Create image buttons
        self.create_image_buttons(images, image_buttons_frame)

        # Create the login button
        login_button = ttk.Button(image_buttons_frame, text="Login", command=self.login)
        login_button.grid(row=len(images)//6, column=2, pady=10)

    def decode_password(self, password):
        # Decode the password from base64 and load as a dictionary
        decoded_password = base64.b64decode(password).decode("utf-8")
        password_dict = json.loads(decoded_password)
        return password_dict

    def fetch_additional_images(self, password_dict) -> list:
        image_list = list(password_dict.values())
        total_images = 90  # Total number of images

        # Generate the full list of image filenames
        all_images = [f"{str(i).zfill(3)}.jpg" for i in range(1, total_images + 1)]

        # Find the images that are not present in the given list
        missing_images = [image for image in all_images if image not in image_list]
        additional_images = []
        for image in missing_images:
            image_dict = {
                "id": int(image[:-4]),
                "image": image,
            }
            additional_images.append(image_dict)
        # Define additional images for selection
        return random.sample(additional_images, 12)

    def create_image_buttons(self, images, parent_frame):
        row_count = 0
        col_count = 0
        self.picture_selection = []

        for image_data in images:
            image_id = image_data["id"]
            image_path = image_data["image"]

            frame = ttk.Frame(parent_frame)
            frame.grid(row=row_count, column=col_count, padx=5, pady=5)

            # Open and display the image
            image = Image.open(os.path.join(os.getcwd(), "processed", image_path))
            image = image.resize((80, 80))
            tk_image = ImageTk.PhotoImage(image)

            # Create the image button
            image_button = ttk.Button(frame, image=tk_image,
                                      command=lambda id=image_id: self.select_image(id))
            image_button.image = tk_image
            image_button.pack()

            # Create and display the image label
            image_label = ttk.Label(frame, text="Not Selected", foreground="red")
            image_label.pack()

            self.picture_selection.append({"id": image_id, "button": image_button, "label": image_label, "selected": False})

            col_count += 1
            if col_count > 5:
                row_count += 1
                col_count = 0

    def select_image(self, image_id):
        for picture in self.picture_selection:
            if picture["id"] == image_id:
                if picture["selected"]:
                    picture["selected"] = False
                    picture["label"].config(text="Not Selected", foreground="red")
                else:
                    picture["selected"] = True
                    picture["label"].config(text="Selected", foreground="green")

                    # Append the selected image to the list
                    self.selected_images.append(picture)
                break
    
    def login(self):
        global username
        
        password_dict = self.decode_password(self.fetch_password_from_database(username))
        
        # Get the selected images
        selected_ids = [p["id"] for p in self.selected_images]
        
        if len(selected_ids) != 6:
            messagebox.showwarning("Invalid Selection", "Please select exactly 6 images.")
            return

        password_list = []
        for value in password_dict.values():
            password_list.append(int(value[:-4]))

        if password_list == selected_ids:
            self.login_frame.destroy()
            login_successful_window = tk.Toplevel(self.root)
            login_successful_window.title("Login Successful")

            welcome_label = ttk.Label(login_successful_window, text=f"Login Successful! Welcome Back {username}!",
                                    font=("Helvetica", 16, "bold"))
            welcome_label.pack(pady=10)
        else:
            messagebox.showerror("Invalid Login", "Invalid username or password.")
            self.root.quit()
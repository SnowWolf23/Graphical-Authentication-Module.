import base64
import json
import os
import random
import sqlite3
from tkinter import messagebox, ttk

from PIL import Image, ImageTk


class RegistrationView:
    def __init__(self, root):
        self.root = root
        self.create_widgets()

    def create_widgets(self):
        # Create a frame for the registration screen content
        self.registration_frame = ttk.Frame(self.root, padding="20")
        self.registration_frame.pack(fill="both", expand=True)

        # Create the username section
        username_label = ttk.Label(self.registration_frame, text="Username:")
        username_label.grid(row=0, column=0, padx=5, pady=5)
        self.username_entry = ttk.Entry(self.registration_frame)
        self.username_entry.grid(row=0, column=1, padx=5, pady=5)

        # Create the image selection pane
        self.create_image_selection()

        # Create the register button
        register_button = ttk.Button(self.registration_frame, text="Register", command=self.register)
        register_button.grid(row=8, column=0, columnspan=2, pady=10)

    def create_image_selection(self):
        # Create a frame for the image buttons and labels
        image_selection_frame = ttk.Frame(self.registration_frame)
        image_selection_frame.grid(row=1, column=0, columnspan=2, padx=5, pady=5)

        # Create a frame inside the image_selection_frame for the image buttons and labels
        image_frame = ttk.Frame(image_selection_frame)
        image_frame.pack()

        # Populate the image buttons and labels
        self.create_image_buttons(image_frame)

    def create_image_buttons(self, parent_frame):
        row_count = 0
        col_count = 0
        self.image_selection = []

        # Create a list of image IDs
        image_ids = list(range(1, 91))
        random.shuffle(image_ids)

        for image_id in image_ids:
            image_path = f"{image_id:03d}.jpg"

            frame = ttk.Frame(parent_frame)
            frame.grid(row=row_count, column=col_count, padx=5, pady=5)

            # Open and display the image
            image = Image.open(os.path.join(os.getcwd(), "processed", image_path))
            image = image.resize((60, 60))
            tk_image = ImageTk.PhotoImage(image)

            # Create the image button
            image_button = ttk.Button(frame, image=tk_image, command=lambda id=image_id: self.select_image(id))
            image_button.image = tk_image
            image_button.pack()

            # Create and display the image label
            image_label = ttk.Label(frame, text="Not Selected", foreground="red")
            image_label.pack()

            self.image_selection.append({"id": image_id, "button": image_button, "label": image_label, "selected": False})

            col_count += 1
            if col_count > 14:
                row_count += 1
                col_count = 0

        # Shuffle the image selection list
        random.shuffle(self.image_selection)

    def select_image(self, image_id):
        for image in self.image_selection:
            if image["id"] == image_id:
                if image["selected"]:
                    image["selected"] = False
                    image["label"].config(text="Not Selected", foreground="red")
                else:
                    image["selected"] = True
                    image["label"].config(text="Selected", foreground="green")
                break

    def register(self):
        # Get the entered username
        username = self.username_entry.get()

        # Get the selected images
        selected_images = [img["id"] for img in self.image_selection if img["selected"]]

        if len(selected_images) != 6:
            messagebox.showwarning("Invalid Selection", "Please select exactly 6 images.")
            return

        # Print the registration details for testing
        print("Username:", username)
        print("Selected Images:", selected_images)

        # Prepare the data dictionary
        data_dict = {str(i+1): f"{selected_images[i]:03d}.jpg" for i in range(6)}

        # Convert the data to JSON format
        json_data = json.dumps(data_dict)

        # Encode the JSON data in base64
        encoded_data = base64.b64encode(json_data.encode()).decode()

        # Insert the values into the users table
        conn = sqlite3.connect('database.db')
        c = conn.cursor()
        c.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, encoded_data))
        conn.commit()
        conn.close()

        # Show info message box
        messagebox.showinfo("Success", f"Data inserted successfully into the database.\nYour username is {username}")

        # Close the registration window
        self.root.destroy()
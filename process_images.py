import os
from PIL import Image

# Create a directory to store processed images
processed_dir = os.path.join(os.getcwd(), "processed")
os.makedirs(processed_dir, exist_ok=True)

# Path to the folder containing the images
folder_path = os.path.join(os.getcwd(), "images")

# Iterate over the files in the folder
for filename in os.listdir(folder_path):
    if filename.endswith(('.jpg', '.jpeg', '.png', '.gif')):
        # Open the image
        image_path = os.path.join(folder_path, filename)
        with Image.open(image_path) as image:
            # Resize the image to 20x20 pixels
            resized_image = image.resize((120, 120))
            
            # Convert the image to JPEG format
            if resized_image.mode != "RGB":
                resized_image = resized_image.convert("RGB")
            
            # Remove the original file extension from the filename
            filename_without_extension = os.path.splitext(filename)[0]
            
            # Save the processed image to the processed directory with the .jpg extension
            processed_filename = f"{filename_without_extension}.jpg"
            processed_path = os.path.join(processed_dir, processed_filename)
            resized_image.save(processed_path, "JPEG")

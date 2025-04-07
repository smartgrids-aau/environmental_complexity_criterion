from PIL import Image
import os

# Get the current directory of the script
current_directory = os.path.dirname(os.path.abspath(__file__))

# List all PNG files in the current directory
png_files = [filename for filename in os.listdir(current_directory) if filename.lower().endswith('.png')]

# Loop through each PNG file and process it
for filename in png_files:
    # Open the image
    with Image.open(filename) as img:
        # Get the original width and height
        original_width, original_height = img.size

        # Calculate the new width and height (4x larger)
        new_width = original_width * 4
        new_height = original_height * 4

        # Resize the image to the new dimensions
        img = img.resize((new_width, new_height), Image.NEAREST)

        # Save the resized image back to the same file
        img.save(filename)
        print(f"Resized {filename} to {new_width}x{new_height} pixels.")

from PIL import Image, ImageOps
import os

# Get a list of all PNG files in the current directory
png_files = [file for file in os.listdir() if file.endswith('.png')]

# Define the border size (in pixels)
border_size = 10

# Loop through each PNG file and resize and add a border
for file in png_files:
    # Open the image
    image = Image.open(file)
    
    # Get the original width and height
    width, height = image.size
    
    # Calculate the new width and height (20 times bigger)
    new_width = width * 20
    new_height = height * 20
    
    # Resize the image while keeping it binary
    image = image.resize((new_width, new_height), Image.NEAREST)
    
    # Add a black border
    image_with_border = ImageOps.expand(image, border=border_size, fill="black")
    
    # Save the resized image with the same filename
    image_with_border.save(file)

import cv2
import numpy as np
import requests
from io import BytesIO

# URL of the image you want to process
image_url = 'https://earthswonderfulhues.files.wordpress.com/2015/04/central-park-new-york-autumn-wallpaper-16605.jpg'

# Fetch the image from the URL
response = requests.get(image_url)
image_data = BytesIO(response.content)

# Load the image using OpenCV
image = cv2.imdecode(np.frombuffer(image_data.read(), np.uint8), -1)
B = image[:,:,0]
G = image[:,:,1]
R = image[:,:,2]

image[:,:,0] = G
image[:,:,1] = R
image[:,:,2] = B
# Show the modified image
cv2.imshow('Modified Image', image)
cv2.waitKey(0)
cv2.destroyAllWindows()

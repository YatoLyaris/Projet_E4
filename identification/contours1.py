import cv2
import matplotlib.pyplot as plt

# Load the image from file
file_path = 'image/plante2.jpg'
image = cv2.imread(file_path)

# Convert the image to gray scale
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# Use Canny edge detection to find edges
edges = cv2.Canny(gray, 100, 200)

# Find the contours in the edge-detected image
contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

# Filter contours to get those on the left side and with sufficient area
contours = [cnt for cnt in contours if cv2.contourArea(cnt) > 200 and cv2.boundingRect(cnt)[0] < gray.shape[1] // 2]

# Draw contours on the original image
image_with_contours = image.copy()
cv2.drawContours(image_with_contours, contours, -1, (0, 255, 0), 2)

# Convert the image to RGB format for matplotlib
image_with_contours_rgb = cv2.cvtColor(image_with_contours, cv2.COLOR_BGR2RGB)

# Show the original image, the edge-detected image, and the image with contours
fig, ax = plt.subplots(1, 3, figsize=(18, 6))
ax[0].imshow(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
ax[0].set_title('Original Image')
ax[0].axis('off')

ax[1].imshow(edges, cmap='gray')
ax[1].set_title('Canny Edges')
ax[1].axis('off')

ax[2].imshow(image_with_contours_rgb)
ax[2].set_title('Image with Contours')
ax[2].axis('off')

plt.show()

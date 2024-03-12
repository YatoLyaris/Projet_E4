import cv2
import numpy as np
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
import colorsys

bound_lower = np.array([25, 20, 20])
bound_upper = np.array([125, 255, 255])

# Charger l'image de la plante avec fond blanc
image = cv2.imread('images/plante2.jpg')

# Charger les points de contour de la plante
contour_points = np.loadtxt('detect_color/points.txt', dtype=int)

# Créer un masque à partir des points de contour
mask = np.zeros(image.shape[:2], dtype=np.uint8)
cv2.drawContours(mask, [contour_points], -1, (255), thickness=cv2.FILLED)

# Appliquer le masque sur l'image pour isoler la plante
plante_isolee = cv2.bitwise_and(image, image, mask=mask)

# Convertir l'image isolée en une liste de pixels pour KMeans
pixels = plante_isolee.reshape(-1, 3)

# Utiliser KMeans pour obtenir les couleurs dominantes
kmeans = KMeans(n_clusters=5, n_init="auto")  # Vous pouvez ajuster le nombre de clusters selon vos besoins
kmeans.fit(pixels)
dominant_colors = kmeans.cluster_centers_.astype(np.uint8)

filtered_palette = []
for color in dominant_colors:
    if (
        bound_lower[0] <= color[0] <= bound_upper[0] and
        bound_lower[1] <= color[1] <= bound_upper[1] and
        bound_lower[2] <= color[2] <= bound_upper[2]
    ):
        filtered_palette.append(color)

plt.imshow([[filtered_palette[i] for i in range(len(filtered_palette))]])
plt.show()

for color in filtered_palette:
    print(color)
    print(f"#{color[0]:02x}{color[1]:02x}{color[2]:02x}")
    print(colorsys.rgb_to_hsv(*color)) # (teinte, saturation, valeur)
    print(colorsys.rgb_to_hls(*color)) # (teinte, luminosité, saturation)

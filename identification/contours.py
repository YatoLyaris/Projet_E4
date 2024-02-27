import cv2
import numpy as np
import os

def draw_plant_outline(image_path, output_dir):
    # Charger l'image
    image = cv2.imread(image_path)
    if image is None:
        print(f"Erreur : l'image n'a pas pu être chargée depuis {image_path}.")
        return

    # Convertir en espace de couleur HSV
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

    # Définir la plage de couleur verte pour inclure la couleur de la plante
    lower_green = np.array([25, 40, 40])  # Valeurs ajustées pour inclure des verts plus foncés
    upper_green = np.array([85, 255, 255])
    mask_green = cv2.inRange(hsv, lower_green, upper_green)

    # Définir la plage de couleur pour le marron de la tige
    # Ces valeurs peuvent nécessiter un ajustement précis en fonction de la tige
    lower_brown = np.array([10, 100, 20])  # Ajusté pour capturer la couleur marron de la tige
    upper_brown = np.array([20, 255, 200])
    mask_brown = cv2.inRange(hsv, lower_brown, upper_brown)

    # Combiner les masques pour le vert et le marron
    mask_combined = cv2.bitwise_or(mask_green, mask_brown)

    # Appliquer des opérations morphologiques pour fermer les petits trous dans le masque
    kernel = np.ones((5, 5), np.uint8)
    mask_combined = cv2.morphologyEx(mask_combined, cv2.MORPH_CLOSE, kernel)

    # Appliquer un masque pour extraire la plante verte et la tige
    plant = cv2.bitwise_and(image, image, mask=mask_combined)

    # Convertir l'image de la plante masquée en nuances de gris et binariser
    gray_plant = cv2.cvtColor(plant, cv2.COLOR_BGR2GRAY)
    _, binary_plant = cv2.threshold(gray_plant, 1, 255, cv2.THRESH_BINARY)

    # Trouver les contours sur l'image binarisée
    contours, _ = cv2.findContours(binary_plant, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Dessiner les contours sur l'image
    contour_image = image.copy()
    cv2.drawContours(contour_image, contours, -1, (0, 255, 0), 2)

    # Vérifier si le dossier de sortie existe, sinon le créer
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Enregistrer l'image avec contours dans le dossier de sortie
    output_path = os.path.join(output_dir, 'outlined_plante2.jpg')
    cv2.imwrite(output_path, contour_image)

    print(f"L'image avec les contours a été enregistrée sous : {output_path}")

# Appeler la fonction avec le chemin de l'image téléchargée et le dossier de sortie
image_path = 'image/plante2.jpg'
output_dir = 'image/contours'

# Appeler la fonction avec le chemin de l'image et le dossier de sortie
draw_plant_outline(image_path, output_dir)
from PIL import Image

def appareil(image_path):
    try:
        image = Image.open(image_path)
        exif_data = image._getexif()
        s = ""
        if exif_data:
            fabricant = exif_data.get(271)
            model = exif_data.get(272)
            if fabricant:
                s += fabricant + " "
            if model:
                s += model
            return s
    except Exception as e:
        print("Erreur lors de la récupération du modèle d'appareil:", e)
    return None

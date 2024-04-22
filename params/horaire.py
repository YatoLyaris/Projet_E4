from PIL import Image
from datetime import datetime

def capture_time(image_path):
    try:
        image = Image.open(image_path)
        exif_data = image._getexif()
        if exif_data:
            capture_time = exif_data.get(36867)  # 36867 correspond à l'identifiant EXIF pour la date et l'heure de la prise de vue
            if capture_time:
                capture_time = datetime.strptime(capture_time, "%Y:%m:%d %H:%M:%S")
                return capture_time
    except Exception as e:
        print("Erreur lors de la récupération de l'heure de capture de la photo:", e)
    return None

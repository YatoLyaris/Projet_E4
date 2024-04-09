from picamera2 import Picamera2
import time
import os

def photo(path, i):
    picam2 = Picamera2()
    
    # Réglages de la résolution et du format du capteur
    picam2.sensor_resolution = (1296, 972)
    picam2.sensor_format = "SGBRG10_CSI2P"
    
    # Réglage de l'exposition pour éviter la surexposition
    picam2.exposure_mode = 'auto'  # Mode d'exposition automatique
    
    # Réglage de l'équilibre des blancs pour correspondre à l'éclairage ambiant
    picam2.awb_mode = 'auto'  # Balance des blancs automatique
    
    # Prendre une photo (ici angle 1, remplacez le 1 par le bon angle pour ne pas avoir des noms de photos dupliquées)
    name = f"photo{str(i)}_1.jpg"
    path_photo = os.path.join(path, name)
    
    picam2.start_and_capture_file(path_photo,
                                show_preview=False)
    
    picam2.close()
    print("Photo capturée:", path_photo)


def main():

    path = "../photos/"

    if not os.path.exists(path):
        os.makedirs(path)
    
    try:
        i = 1
        while True:
            photo(path, i)
            i += 1
            time.sleep(900)  # Capturer une photo toutes les 60 secondes
    except KeyboardInterrupt:
        print("Arrêt manuel du programme")
    finally:
        print("Arrêt du programme")

if __name__ == "__main__":
    main()


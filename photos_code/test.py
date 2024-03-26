from picamera2 import Picamera2
import time
import os

path = "../photos/"

if not os.path.exists(path):
    os.makedirs(path)

def photo(path):
    picam2 = Picamera2()
    
    # Réglages de la résolution et du format du capteur
    picam2.sensor_resolution = (1296, 972)
    picam2.sensor_format = "SGBRG10_CSI2P"
    
    # Réglage de l'exposition pour éviter la surexposition
    picam2.exposure_mode = 'auto'  # Mode d'exposition automatique
    
    # Réglage de l'équilibre des blancs pour correspondre à l'éclairage ambiant
    picam2.awb_mode = 'auto'  # Balance des blancs automatique
    
    # Prendre une photo
    name = "camera1_photo_" + str(int(time.time())) + ".jpg"
    path_photo = os.path.join(path, name)
    
    picam2.start_and_capture_file(path_photo,
                                show_preview=False)
    
    picam2.close()
    print("Photo capturée:", path_photo)

def main():
    try:
        while True:
            photo(path)
            time.sleep(60)  # Capturer une photo toutes les 60 secondes
    except KeyboardInterrupt:
        print("Arrêt manuel du programme")
    finally:
        print("Arrêt du programme")

if __name__ == "__main__":
    main()


from picamera2 import Picamera2
import time
import os

path = "../photos/"

if not os.path.exists(path):
    os.makedirs(path)

def photo(path):
    picam2 = Picamera2()
    #config = picam2.create_still_configuration({"size": (640, 480)})
    name = "camera4_photo_" + str(int(time.time())) + ".jpg"
    path_photo = os.path.join(path, name)
    picam2.start_and_capture_file(path_photo, 
                                delay=1, 
                                show_preview=False, 
                                #capture_mode=config
                                )
    picam2.close()
    print(path_photo)


def main():
    try:
        while True:
            photo(path)
            time.sleep(900)
    except KeyboardInterrupt:
        print("Arrêt manuel du programme")
    finally:
        print("Arrêt du programme")


if __name__ == "__main__":
    main()
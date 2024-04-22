import cv2

def luminosity(path):

    image = cv2.imread(path)

    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    mean_brightness_gray = round(gray_image.mean(), 3)

    return mean_brightness_gray

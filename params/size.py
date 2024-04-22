import cv2


def size_pixel(path):

    image = cv2.imread(path)

    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    _, thresh = cv2.threshold(gray, 3, 255, cv2.THRESH_BINARY)

    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    top_pixel = None
    bottom_pixel = None

    for contour in contours:
        x, y, w, h = cv2.boundingRect(contour)
        
        if top_pixel is None or y < top_pixel[1]:
            top_pixel = (x, y)
        if bottom_pixel is None or (y + h) > bottom_pixel[1]:
            bottom_pixel = (x, y + h)

    return bottom_pixel[1] - top_pixel[1]

def size_cm(pixel_plant, pixel_ref, cm_ref, cm_pot):

    cm_plant = (pixel_plant*cm_ref)/pixel_ref - cm_pot
    return round(cm_plant, 3)

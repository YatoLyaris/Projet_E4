import cv2
import numpy as np

img = cv2.imread("./images/plante2.jpg")
hsv_img = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
bound_lower = np.array([25, 20, 20])
bound_upper = np.array([100, 255, 255])

mask_green = cv2.inRange(hsv_img, bound_lower, bound_upper)
kernel = np.ones((7, 7), np.uint8)

mask_green = cv2.morphologyEx(mask_green, cv2.MORPH_CLOSE, kernel)
mask_green = cv2.morphologyEx(mask_green, cv2.MORPH_OPEN, kernel)

seg_img = cv2.bitwise_and(img, img, mask=mask_green)
contours, hier = cv2.findContours(
    mask_green.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE
)

with open('detect_color/points.txt', 'w') as file:
        for contour in contours:
            for i, point in enumerate(contour):
                x, y = point[0]
                file.write(f"{x} {y}\n")
                
output = cv2.drawContours(seg_img, contours, -1, (0, 0, 255), 3)

cv2.imshow("Result", output)
cv2.waitKey(0)
cv2.destroyAllWindows()



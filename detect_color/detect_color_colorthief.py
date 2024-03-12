from colorthief import ColorThief
import matplotlib.pyplot as plt
import colorsys
import numpy as np

bound_lower = np.array([25, 20, 20])
bound_upper = np.array([125, 255, 255])

ct = ColorThief("images/plante2.jpg")

palette = ct.get_palette(color_count=5)

filtered_palette = []
for color in palette:
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

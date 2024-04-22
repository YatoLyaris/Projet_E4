from colorthief import ColorThief
import numpy as np


def color(path):

    bound_lower = np.array([40, 40, 40])
    bound_upper = np.array([170, 170, 170])

    ct = ColorThief(path)

    palette = ct.get_palette(color_count=5, quality=5)

    filtered_palette = []
    for color in palette:
        if (
            bound_lower[0] <= color[0] <= bound_upper[0] and
            bound_lower[1] <= color[1] <= bound_upper[1] and
            bound_lower[2] <= color[2] <= bound_upper[2]
        ):
            filtered_palette.append(color)

    if not filtered_palette:
        return "Aucune couleur détecté", None

    return filtered_palette[0], f"#{filtered_palette[0][0]:02x}{filtered_palette[0][1]:02x}{filtered_palette[0][2]:02x}"

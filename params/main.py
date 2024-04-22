import pandas as pd
import numpy as np
import os
from color import color 
from luminosity import luminosity
from horaire import capture_time
from background import removeBackground
from modele_app import appareil
from size import size_pixel, size_cm

def main():

    directory_plante = "images/plante"
    directory_filtre = "images/filtre"
    l_habitat = []
    l_date = []
    l_modele = []
    l_color_html = []
    l_color_rgb = []
    l_lum = []
    l_cm_size = []
    l_cm_croissance = []
    l_maladie = []

    habitat = input("Rentrez le lieu de l'expérience (plein air, intérieur, isolée de la lumière): ")

    ref_size = None

    while ref_size is None:
        try:
            ref_size = round(float(input("Rentrez la taille de l'objet de référence (en cm) : ")), 3)
        except ValueError:
            print("Veuillez entrer une valeur numérique valide.")

    pot_size = None

    while pot_size is None:
        try:
            pot_size = round(float(input("Rentrez la taille du pot (en cm) : ")), 3)
        except ValueError:
            print("Veuillez entrer une valeur numérique valide.")

    ref_path = "images/reference/reference.jpg"
    ref_back_path = "images/filtre/ref_first_plan.png"

    removeBackground(ref_path, ref_back_path)
    size_pixel_ref = size_pixel(ref_back_path)

    i = 1

    croissance = 0

    while True:

        photo_path = os.path.join(directory_plante, f"photo{i}_1.jpg")
        back_path = os.path.join(directory_filtre, f"photo{i}_first_plan.png")

        print(photo_path, back_path)

        if not os.path.exists(photo_path):
            print(f"fin: {i}")
            break

        try:
            date = capture_time(photo_path)
        except:
            date = np.nan


        try:
            app = appareil(photo_path)
        except:
            app = np.nan

        removeBackground(photo_path, back_path)

        size_pixel_plant = size_pixel(back_path)

        size_cm_plant = size_cm(size_pixel_plant, size_pixel_ref, ref_size, pot_size)

        rgb_color, html_color = color(back_path)

        lum = luminosity(photo_path)

        if i == 1:
            croissance = 0
        else:
            croissance = round(size_cm_plant - l_cm_size[-1], 3)

        l_habitat.append(habitat)
        l_date.append(date)
        l_modele.append(app)
        l_color_html.append(html_color)
        l_color_rgb.append(list(rgb_color))
        l_lum.append(lum)
        l_cm_size.append(size_cm_plant)
        l_cm_croissance.append(croissance)
        l_maladie.append("healthy")

        i += 1

    
    data = {
    'date': l_date,
    'modele': l_modele,
    'habitat': l_habitat,
    'maladie': l_maladie,
    'couleur html': l_color_html,
    'couleur rgb': l_color_rgb,
    'luminosite': l_lum,
    'taille (cm)': l_cm_size,
    'croissance (cm)': l_cm_croissance
    }

    df = pd.DataFrame(data)

    df.to_csv("./data/parametres.csv", index=False)


if __name__ == "__main__":
    main()
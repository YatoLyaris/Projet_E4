import numpy as np
import vtkplotlib as vpl
from stl import mesh, Mesh

def get_points(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()
    # Convertir les chaînes de caractères en entiers
    contour_data = []
    for line in lines:
        if line.strip():  # Vérifier si la ligne n'est pas vide
            values = list(map(int, line.strip().split()))  # Convertir les valeurs en entiers
            values1 = list(map(int, line.strip().split()))
            if len(values) == 2:  # Si seulement deux valeurs sont présentes, ajouter une valeur par défaut pour z
                values.append(0)
                values1.append(20)
            contour_data.append(values)
            contour_data.append(values1)
    return contour_data

def create_faces(points):
    faces = []
    for i in range(len(points)-2):
        faces.append([i, i+1, i+2])
    return np.array(faces)


def creer(vertices, faces, path):
    # Create the mesh
    figure = mesh.Mesh(np.zeros(faces.shape[0], dtype=mesh.Mesh.dtype))
    for i, f in enumerate(faces):
        for j in range(3):
            figure.vectors[i][j] = vertices[f[j]]
    figure.save(path)

def afficher(path):
    v_mesh = Mesh.from_file(path)
    vpl.mesh_plot(v_mesh)
    vpl.show()


# Chemin du fichier texte contenant les données de contour
file_path = 'modelisation/points.txt'

_vertices = get_points(file_path)

_faces = create_faces(_vertices)

_out_path = 'modelisation/plante.stl'

creer(_vertices, _faces, _out_path)
#afficher(_out_path)
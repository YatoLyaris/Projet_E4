import tkinter as tk
from tkinter import ttk
from stl import mesh
from mpl_toolkits import mplot3d
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import numpy as np


def button_click(button_num):
    print(f"Bouton {button_num} cliqué.")


root = tk.Tk()
root.title("Affichage STL")

# Création des boutons
button_frame = ttk.Frame(root)
button_frame.pack(side=tk.RIGHT, fill=tk.Y)
button1 = ttk.Button(button_frame, text="1", command=lambda: button_click(1))
button1.pack(pady=10)
button2 = ttk.Button(button_frame, text="2", command=lambda: button_click(2))
button2.pack(pady=10)

# Chargement du fichier STL
stl_file_path = "./modelisation/plante.stl"
stl_mesh = mesh.Mesh.from_file(stl_file_path)
# Création du canevas pour afficher le maillage STL
fig = plt.figure(figsize=(5, 5))
axes = mplot3d.Axes3D(fig)
axes.add_collection3d(mplot3d.art3d.Poly3DCollection(stl_mesh.vectors))
axes.set_xlabel('X')
axes.set_ylabel('Y')
axes.set_zlabel('Z')

# Redimensionnement ou zoom du maillage STL
axes.auto_scale_xyz(stl_mesh.points.flatten(order='F'),
                     stl_mesh.points.flatten(order='F'),
                     stl_mesh.points.flatten(order='F'))

canvas = FigureCanvasTkAgg(fig, master=root)
canvas_widget = canvas.get_tk_widget()

# Placement du canevas et des boutons dans la fenêtre
canvas_widget.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

root.mainloop()
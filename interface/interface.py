import sys
import pandas as pd
from PyQt5.QtWidgets import QApplication, QMainWindow, QHBoxLayout, QVBoxLayout, QWidget, QSlider, QLabel, QSizePolicy, QDesktopWidget
from PyQt5.QtCore import Qt, QRect
from PyQt5.QtGui import QColor, QPalette
import pyqtgraph.opengl as gl
import numpy as np
from stl import mesh

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.init_ui()

    def init_ui(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        # Ouvrir la fenêtre aux trois quarts de la taille de l'écran
        screen_geometry = QDesktopWidget().availableGeometry()
        width = int(screen_geometry.width() * 0.75)
        height = int(screen_geometry.height() * 0.75)
        self.setGeometry(QRect(0, 0, width, height))

        # Définir un fond beige
        palette = QPalette()
        palette.setColor(QPalette.Background, QColor(245, 245, 220))  # RGB pour un fond beige clair
        central_widget.setPalette(palette)
        central_widget.setAutoFillBackground(True)

        hbox = QHBoxLayout()
        central_widget.setLayout(hbox)

        # Ajout de la partie 3D à gauche
        left_widget = QWidget()
        hbox.addWidget(left_widget)

        vbox_left = QVBoxLayout()
        left_widget.setLayout(vbox_left)

        self.w = gl.GLViewWidget()
        self.w.setMinimumWidth(int(width * 0.65))  # Définir la largeur minimale du widget de la partie 3D à la moitié de la largeur de l'interface
        vbox_left.addWidget(self.w)

        # Chargement du fichier STL et création d'un objet GLMeshItem
        stl_mesh = mesh.Mesh.from_file('modelisation/plante.stl')
        shape = stl_mesh.points.shape
        points = stl_mesh.points.reshape(-1, 3)
        faces = np.arange(points.shape[0]).reshape(-1, 3)

        meshdata = gl.MeshData(vertexes=points, faces=faces)
        self.mesh_item = gl.GLMeshItem(meshdata=meshdata, smooth=True, drawFaces=False, drawEdges=True, edgeColor=(0, 1, 0, 1))
        self.w.addItem(self.mesh_item)

        # Création d'une grille 3D pour la scène
        grid = gl.GLGridItem()
        grid.translate(*points.mean(axis=0))  # Déplacer la grille au centre de la modélisation STL
        self.w.addItem(grid)

        # Ajout de la partie paramètres à droite
        right_widget = QWidget()
        hbox.addWidget(right_widget)

        vbox_right = QVBoxLayout()
        right_widget.setLayout(vbox_right)

        # Ajout du slider prenant la moitié supérieure de l'interface
        self.param_slider = QSlider(Qt.Horizontal)
        self.param_slider.setSingleStep(1)
        self.param_slider.setMaximumWidth(int(width * 0.5))  # Définir la largeur du slider à la moitié de la largeur de l'interface
        vbox_right.addWidget(self.param_slider)

        # Ajout des paramètres sous le slider
        param_widget = QWidget()
        vbox_right.addWidget(param_widget)

        vbox_params = QVBoxLayout()
        param_widget.setLayout(vbox_params)

        # Lire le fichier CSV
        self.data = pd.read_csv('data/parametres.csv')

        # Créer une liste de QLabels pour stocker les labels correspondant à chaque colonne
        self.labels = []
        for i in range(len(self.data.columns)):
            label = QLabel(f"{self.data.columns[i]} : {self.data.iloc[0].iloc[i]}")
            vbox_params.addWidget(label)
            self.labels.append(label)

        # Mettre à jour la plage du slider
        self.param_slider.setRange(0, len(self.data)-1)  # Range étendu pour couvrir les lignes du dataset

        # Mise à jour du label lorsque la valeur du slider change
        self.param_slider.valueChanged.connect(self.update_param_label)

        self.setWindowTitle('Interface Mouvement plantes 3D')
        self.show()

    def update_param_label(self):
        row_index = self.param_slider.value()
        for i, label in enumerate(self.labels):
            label.setText(f"{self.data.columns[i]} : {self.data.iloc[row_index].iloc[i]}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    sys.exit(app.exec_())

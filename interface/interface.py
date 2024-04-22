import sys
import pandas as pd
import matplotlib.pyplot as plt
from PyQt5.QtWidgets import QApplication, QMainWindow, QHBoxLayout, QVBoxLayout, QWidget, QSlider, QLabel, QSizePolicy, QDesktopWidget, QPushButton
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

        # Ajout du widget pour les boutons
        button_widget = QWidget()
        hbox_buttons = QHBoxLayout()
        button_widget.setLayout(hbox_buttons)

        # Ajout des trois boutons
        button1 = QPushButton("Graphique: taille")
        button2 = QPushButton("Graphique: croissance")
        button3 = QPushButton("Graphique: croissance en fonction de la luminosité")

        hbox_buttons.addWidget(button1)
        hbox_buttons.addWidget(button2)
        hbox_buttons.addWidget(button3)

        vbox_main = QVBoxLayout()
        central_widget.setLayout(vbox_main)

        vbox_main.addWidget(button_widget)
        vbox_main.setContentsMargins(0, 0, 0, 0)  # Supprimer les marges autour des boutons
        vbox_main.setSpacing(0)  # Supprimer l'espace entre les boutons et le reste de l'interface

        button_widget.setFixedHeight(int(height * 0.15))  # Définir une hauteur fixe au widget des boutons (15% de la hauteur de l'interface)

        # Connexion des boutons aux fonctions de création de graphiques
        button1.clicked.connect(self.plot_size_graph)
        button2.clicked.connect(self.plot_growth_graph)
        button3.clicked.connect(self.plot_size_vs_light_graph)

        # Ajout de la partie 3D à gauche et des paramètres à droite
        hbox = QHBoxLayout()
        vbox_main.addLayout(hbox)

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

        # Convertir la colonne 'date' en type datetime
        self.data['date'] = pd.to_datetime(self.data['date'])

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

    def plot_size_graph(self):
        plt.plot(self.data['date'], self.data['taille (cm)'])
        plt.xlabel('Date')
        plt.ylabel('Taille (cm)')
        plt.title('Graphique: Taille de la plante au cours du temps')
        plt.show()

    def plot_growth_graph(self):
        plt.plot(self.data['date'], self.data['croissance (cm)'])
        plt.xlabel('Date')
        plt.ylabel('Croissance (cm)')
        plt.title('Graphique: Croissance de la plante au cours du temps')
        plt.show()

    def plot_size_vs_light_graph(self):
        plt.scatter(self.data['croissance (cm)'], self.data['luminosite'])
        plt.xlabel('croissance (cm)')
        plt.ylabel('Luminosité')
        plt.title('Graphique: croissance en fonction de la luminosité')
        plt.show()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    sys.exit(app.exec_())

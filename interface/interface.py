import sys
import os
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from PyQt5.QtWidgets import QApplication, QMainWindow, QHBoxLayout, QVBoxLayout, QWidget, QSlider, QLabel, QSizePolicy, QDesktopWidget, QPushButton, QDialog
from PyQt5.QtCore import Qt, QRect
from PyQt5.QtGui import QColor, QPalette

class GraphDialog(QDialog):
    def __init__(self, fig, title):
        super().__init__()

        self.setWindowTitle(title)
        self.setLayout(QVBoxLayout())
        self.layout().addWidget(FigureCanvas(fig))
        self.resize(800, 600)

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

        # Chargement du graphique enregistré à la place de la modélisation 3D
        depth_map_path = 'images/depth_map/depth_map1.png'
        if os.path.exists(depth_map_path):
            self.depth_map_image = plt.imread(depth_map_path)

            # Création d'un canvas matplotlib pour afficher le graphique
            self.figure = plt.figure()
            self.canvas = FigureCanvas(self.figure)

            # Ajout du widget pour afficher le graphique
            self.graph_widget = QWidget()
            self.graph_widget.setFixedSize(800, 800)  # Définir une taille fixe pour le widget (largeur, hauteur)
            self.graph_layout = QVBoxLayout()
            self.graph_widget.setLayout(self.graph_layout)

            self.graph_layout.addWidget(self.canvas)
            vbox_left.addWidget(self.graph_widget)

            # Mise à jour du graphique lorsque la valeur du slider change
            self.param_slider.valueChanged.connect(self.update_depth_map_plot)

            # Appeler la fonction update_depth_map_plot() pour afficher la carte de profondeur dès le début
            self.update_depth_map_plot()

        else:
            print("Le fichier depth_map1.png n'existe pas dans le répertoire spécifié.")

        self.setWindowTitle('Interface Mouvement plantes 3D')
        self.show()

    def update_param_label(self):
        row_index = self.param_slider.value()
        for i, label in enumerate(self.labels):
            label.setText(f"{self.data.columns[i]} : {self.data.iloc[row_index].iloc[i]}")

    def update_depth_map_plot(self):
        row_index = self.param_slider.value()
        # Construire le chemin du fichier de la carte de profondeur correspondante
        depth_map_path = f'images/depth_map/depth_map{row_index + 1}.png'
        if os.path.exists(depth_map_path):
            # Charger la carte de profondeur correspondante
            depth_map_image = plt.imread(depth_map_path)
            # Mettre à jour le graphique avec la nouvelle carte de profondeur
            self.figure.clear()
            ax = self.figure.add_subplot(111)
            ax.imshow(depth_map_image, cmap='gray')
            ax.axis('off')
            ax.margins(x=0, y=0)  # Réduire les marges autour de la carte de profondeur
            self.figure.subplots_adjust(left=0, right=1, bottom=0, top=1)  # Ajuster l'espace entre le bord du canvas et la carte de profondeur
            self.canvas.draw()
        else:
            print(f"Le fichier depth_map{row_index + 1}.png n'existe pas dans le répertoire spécifié.")


    def plot_size_graph(self):
        fig = plt.figure()
        plt.plot(self.data['date'], self.data['taille (cm)'])
        plt.xlabel('Date')
        plt.ylabel('Taille (cm)')
        plt.title('Graphique: Taille de la plante au cours du temps')
        self.show_graph(fig, 'Taille de la plante')

    def plot_growth_graph(self):
        fig = plt.figure()
        plt.plot(self.data['date'], self.data['croissance (cm)'])
        plt.xlabel('Date')
        plt.ylabel('Croissance (cm)')
        plt.title('Graphique: Croissance de la plante au cours du temps')
        self.show_graph(fig, 'Croissance de la plante')

    def plot_size_vs_light_graph(self):
        fig = plt.figure()
        plt.scatter(self.data['croissance (cm)'], self.data['luminosite'])
        plt.xlabel('croissance (cm)')
        plt.ylabel('Luminosité')
        plt.title('Graphique: Croissance en fonction de la luminosité')
        self.show_graph(fig, 'Croissance en fonction de la luminosité')

    def show_graph(self, fig, title):
        dialog = GraphDialog(fig, title)
        dialog.exec_()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    sys.exit(app.exec_())

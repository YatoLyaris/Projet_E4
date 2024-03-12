import cv2
import numpy as np

file_path = 'detect_color/points.txt'

def get_points(file_path):
    points = []
    with open(file_path, 'r') as f:
        for ligne in f:
            x, y = map(int, ligne.strip().split())
            points.append((x, y))
    return points

print(get_points(file_path))
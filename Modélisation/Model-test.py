import numpy as np
import vtkplotlib as vpl
from stl import mesh, Mesh

"""
vertices = np.array([\
    [-1, -1, -1],
    [+1, -1, -1],
    [+1, +1, -1],
    [-1, +1, -1],
    [-1, -1, +1],
    [+1, -1, +1],
    [+1, +1, +1],
    [-1, +1, +1]])


faces = np.array([\
    [0,3,1],
    [1,3,2],
    [0,4,7],
    [0,7,3],
    [4,5,6],
    [4,6,7],
    [5,1,2],
    [5,2,6],
    [2,3,6],
    [3,7,6],
    [0,1,5],
    [0,5,4]])
"""



#[x,y,z] où z est la hauteur
vertices = np.array([\
    [-1, -1, -1],
    [+1, -1, -1],
    [-1, +1, -1],
    [+1, +1, -1],
    [0, 0, 0.5]])

faces = np.array([\
    [0,1,2],
    [3,1,2],
    [0,1,4],
    [0,2,4],
    [1,3,4],
    [2,3,4]
    ])


# Create the mesh
cube = mesh.Mesh(np.zeros(faces.shape[0], dtype=mesh.Mesh.dtype))
for i, f in enumerate(faces):
    for j in range(3):
        print(vertices[f[j],:])
        cube.vectors[i][j] = vertices[f[j]]

# Write the mesh to file "test.stl"
cube.save('cube.stl')

# Read the STL using numpy-stl
mesh = Mesh.from_file('cube.stl')

# Plot the mesh
vpl.mesh_plot(mesh)

# Show the figure
vpl.show()
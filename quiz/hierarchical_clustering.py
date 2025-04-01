import pandas as pd
import matplotlib.pyplot as plt
from scipy.cluster.hierarchy import dendrogram, linkage
#from TD.dendrogram import Dendrogram
#from TD.graph import Graph, graph_from_matrix_file

def f(filename):
    node_names = []
    dist_matrix = []
    with open(filename, 'r') as f:
        n = int(f.readline())
        for _ in range(n):
            node_names.append(f.readline().strip())
        for _ in range(n):
            dist_matrix.append([float(x) for x in f.readline().strip().split(',')])
    return dist_matrix, node_names


'''
By adding TD/ at the beginning, you explicitly start the path resolution from the TD directory. Without it, the path might not resolve correctly if the current working directory is not set appropriately.
'''
# Code pour le fichier test6.csv
fname = 'TD/../csv/test6.csv' # Got fixed adding TD/ at the beginning of the path. Si on veut fonctionner sans il faut se placer dans le dossier quiz
data = pd.read_csv(fname, header = 0)
tree = linkage(data[['x', 'y']])
D = dendrogram(tree, labels = data['name'].to_numpy(), orientation = 'left')
plt.show()

# Code pour le fichier bluered.csv
fname = 'TD/../csv/bluered.csv' # Got fixed adding TD/ at the beginning of the path. Si on veut fonctionner sans il faut se placer dans le dossier quiz
data = pd.read_csv(fname, header = 0)
tree = linkage(data[['x', 'y']])
D = dendrogram(tree, labels = data['name'].to_numpy(), orientation = 'left')
plt.show()

# Code pour le fichier languages.csv
fname = 'TD/../csv/languages.csv'
matrix, noms = f(fname)
tree = linkage(matrix)
D = dendrogram(tree, labels = noms, orientation = 'left')
plt.show()

# Code pour le fichier iris.csv, voir directement sur le polycopié
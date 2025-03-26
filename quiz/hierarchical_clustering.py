import pandas as pd
import matplotlib.pyplot as plt
from scipy.cluster.hierarchy import dendrogram, linkage

fname = 'TD/../csv/bluered.csv' # Got fixed adding TD/ at the beginning of the path. Si on veut fonctionner sans il faut se placer dans le dossier quiz
data = pd.read_csv(fname, header = 0)

'''
By adding TD/ at the beginning, you explicitly start the path resolution from the TD directory. Without it, the path might not resolve correctly if the current working directory is not set appropriately.
'''

tree = linkage(data[['x', 'y']])
D = dendrogram(tree, labels = data['name'].to_numpy(), orientation = 'left')
plt.show()

import pandas as pd
import matplotlib.pyplot as plt
from scipy.cluster.hierarchy import dendrogram, linkage

fname = '../csv/bluered.csv'
data = pd.read_csv(fname, header = 0)

tree = linkage(data[['x', 'y']])
D = dendrogram(tree, labels = data['name'].to_numpy(), orientation = 'left')
plt.show()

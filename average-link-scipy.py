import re
import sys
import numpy as np
from scipy.cluster.hierarchy import dendrogram, linkage, fcluster
from matplotlib import pyplot

dataset = sys.argv[1]

arq = open(dataset, 'r')
arq.readline()

X = []

for line in arq:
    param = re.split('[ ,\n,\t]', line)
    X.append([float(param[1]), float(param[2])])
    # clusters.append(Cluster([Point(param[0], (float(param[1]), float(param[2])))]))

X = np.array(X)

# X = [[i] for i in [2, 8, 0, 4, 1, 9, 9, 0]]

# Z = linkage(X, 'single')
# fig = pyplot.figure(figsize=(25, 10))
# dn = dendrogram(Z)


Z = linkage(X, 'average')

clusters = fcluster(Z, 5, criterion='maxclust')

for cluster in clusters:
    print(cluster)

from itertools import groupby
print([len(list(group)) for key, group in groupby(sorted(clusters))])

# pyplot.figure(figsize=(10, 8))
# pyplot.scatter(X[:,0], X[:,1], c=clusters, cmap='prism')  # plot all points
# pyplot.show()
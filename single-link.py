import sys
import csv
import math
import collections.abc

def distance(a, b):
    return math.sqrt(sum([(v[0] - v[1])**2 for v in zip(a, b)]))

def flatten(l):
    if isinstance(l, collections.abc.Iterable) and not isinstance(l, (str, bytes)):
        for el in l:
            yield from flatten(el)
    else:
        yield l

dataset = sys.argv[1]
kMin = int(sys.argv[2])
kMax = int(sys.argv[3])

print("Agrupando", dataset, "com kMin =", kMin, "e kMax =", kMax)

clusters = []
values = []

with open(dataset) as file:
    reader = csv.reader(file, delimiter='\t')
    next(reader)

    for row in reader:
        clusters.append(row[0])
        values.append([float(row[1]), float(row[2])])

n = len(clusters)

clusters = { i : clusters[i] for i in range(0, len(clusters) ) }

infinity = math.inf

distances = [[0 for x in range(n)] for y in range(n)]
min_distances = [0 for x in range(n)]

for i in range(n):
    for j in range(n):  
        distances[i][j] = math.inf if i == j else distance(values[i], values[j])
        if distances[i][j] < distances[i][min_distances[i]]:
            min_distances[i] = j
            
print("Distâncias iniciais calculadas")

for i in range(n - kMin):
    clusterA = 0
    for j in range(n):
        if (distances[j][min_distances[j]] < distances[clusterA][min_distances[clusterA]]):
            clusterA = j
    clusterB = min_distances[clusterA]

    clusters[clusterA] = [clusters[clusterA], clusters[clusterB]]

    for j in range(n):
        if distances[clusterB][j] < distances[clusterA][j]:
            distances[clusterA][j] = distances[clusterB][j]
            distances[j][clusterA] = distances[clusterB][j]
        distances[clusterA][clusterA] = math.inf

    for j in range(n):
        distances[j][clusterB] = math.inf
        distances[clusterB][j] = math.inf

    for j in range(n):
        if min_distances[j] == clusterB:
            min_distances[j] = clusterA
        if distances[clusterA][j] < distances[clusterA][min_distances[clusterA]]:
            min_distances[clusterA] = j

    del clusters[clusterB]

    clustersN = n - i - 1

    print("k =", clustersN)

    if clustersN <= kMax:
        result = []
        for i, cluster in zip(range(clustersN), clusters.values()):
            for element in flatten(cluster):
                result.append((element, i))
        with open(dataset + "-singleLink-k" + str(clustersN) + ".clu", "w+") as out:
            for label, cluster in sorted(sorted(result, key=lambda x:x[0]), key=lambda x: (len(x[0]), x[0])):
                out.write(label + '\t' + str(cluster) + '\n')
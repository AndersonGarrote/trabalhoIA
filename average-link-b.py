import sys
import csv
import math
import uuid
import re

class Point:
    label = ''
    coordinates = (0, 0)

    def __init__(self, label, coordinates):
        self.label = label
        self.coordinates = coordinates

    def distance_to(self, point):
        return math.sqrt((self.coordinates[0] - point.coordinates[0])**2 + (self.coordinates[1] - point.coordinates[1])**2)

    def __str__(self):
        return "{}: {}".format(self.label, self.coordinates)

    def __repr__(self):
        return self.__str__()

class Cluster:
    points = []

    def __init__(self, points = []):
        self.uuid = uuid.uuid1()
        self.points = points

    def distance_to(self, cluster):
        lenA = len(self.points)
        lenB = len(cluster.points)

        d = 0.0

        for x in self.points:
            for y in cluster.points:
                d += x.distance_to(y)

        return d/(lenA*lenB)

    def __str__(self):
        return str(self.points)

    def __repr__(self):
        return self.__str__()

    def __add__(self, cluster):
        return Cluster(self.points + cluster.points)

    def __len__(self):
        return len(self.points)

    def __iter__(self):
        return iter(self.points)

dataset = sys.argv[1]
kMin = int(sys.argv[2])
kMax = int(sys.argv[3])

print("Agrupando", dataset, "com kMin =", kMin, "e kMax =", kMax)

clusters = []

arq = open(dataset, 'r')
arq.readline()

for line in arq:
    param = re.split('[ ,\n,\t]', line)
    clusters.append(Cluster([Point(param[0], (float(param[1]), float(param[2])))]))

S = []

while len(clusters) > 1:

    print(len(clusters))

    if len(S) == 0:
        S.append(clusters[0])

    C = S[-1]

    D = None
    D_distance = math.inf

    for cluster in [cluster for cluster in clusters if cluster != C]:
        distance = C.distance_to(cluster)
        if distance < D_distance or distance == D_distance and cluster.uuid < D.uuid:
            D_distance = distance
            D = cluster

    if D in S:
        M = S.pop() + S.pop()
        clusters.remove(C)
        clusters.remove(D)
        clusters.append(M)
    else:
        S.append(D)

    if len(clusters) <= kMax:
        result = []
        for i in range(len(clusters)):
            for point in clusters[i]:
                result.append((point.label, i))

        with open(dataset + "-averageLink-k" + str(len(clusters)) + ".clu", "w+") as out:
            for label, cluster in sorted(sorted(result, key=lambda x:x[0]), key=lambda x: (len(x[0]), x[0])):
                out.write(label + '\t' + str(cluster) + '\n')
import sys
import csv
import math
import re
import json

class Cluster:
    id = -1

    def __init__(self, num_id, ponto):
        self.id= num_id
        self.pontos = []
        self.pontos.append(ponto)

class Ponto:
    nome = ''
    X = 0.0
    Y = 0.0

    def __init__(self, nome, num_X, num_Y):
        self.nome = nome
        self.X = num_X
        self.Y = num_Y

def calcularDistancia_C_C(A, B):
    d = 0.0
    for i in range(len(A.pontos)):
        for j in range(len(B.pontos)):
            d = d + math.sqrt((A.pontos[i].X - B.pontos[j].X)**2 + (A.pontos[i].Y - B.pontos[j].Y)**2)

    return d/len(A.pontos)*len(B.pontos)

def unirClusters(A, B):
    for i in range(len(B.pontos)):
        A.pontos.append(B.pontos[i])


dataset = sys.argv[1]
kMin = int(sys.argv[2])
kMax = int(sys.argv[3])

print("Agrupando", dataset, "com kMin =", kMin, "e kMax =", kMax)

clusters = []

arq = open(dataset, 'r')
arq.readline()

for line in arq:
    param = re.split('[ ,\n,\t]', line)
    clusters.append(Cluster(len(clusters), Ponto(param[0], float(param[1]), float(param[2]))))

nclusters = len(clusters)
infinity = math.inf

# Setando 0 para a distancia entre todos os clusters
distancias = [[0 for x in range(len(clusters))] for y in range(len(clusters))]

# setando que todos os clusters estao mais proximos do cluster 0
cluster_proximo = [0 for x in range(len(clusters))]

for i in range(len(clusters)):
    for j in range(len(clusters)):
        # a distancia de um cluster para ele mesmo e de infinito
        # a distancia de um cluster para outro e de calcularDistancia_C_C
        distancias[i][j] = infinity if i == j else calcularDistancia_C_C(clusters[i], clusters[j])
        # Se foi encontrado um cluster mais proximo de i, atualiza cluster_proximo[i]
        if distancias[i][j] < distancias[i][cluster_proximo[i]]:
            cluster_proximo[i] = j

for i in range(nclusters - kMin):
    clusterA = 0
    clusterB = 0
    for j in range(len(clusters) - kMin):
        # Caso exista clusters mais proximos que o clusterA esta de cluster_proximo[clusterA], atualiza clusterA
        if (distancias[j][cluster_proximo[j]] < distancias[clusterA][cluster_proximo[clusterA]]):
            clusterA = j
    clusterB = cluster_proximo[clusterA]
    # apos achar os clusters mais proximos, unifica eles
    print("UNIFICANDO CLUSTERS ", clusterA, clusterB)
    print("COM ", len(clusters[clusterA].pontos), ", ", len(clusters[clusterB].pontos), " pontos")
    print("DISTANCIA ", distancias[clusterA][clusterB])
    print("Quantidade de clusters ", len(clusters), "\n")
    unirClusters(clusters[clusterA], clusters[clusterB])
    

    for j in range(len(clusters)):
        # Se para algum cluster, o cluster mais proximo era o clusterB, seta para 0
        cluster_proximo[j] = 0 if cluster_proximo[j] >= len(clusters)-1 else cluster_proximo[j]

    del clusters[clusterB]

    # Para todos os pares ordenados
    for j in range(len(clusters)):
        for k in range(len(clusters)):
            # Se a distancia entre os clusters for infinita, continua infinita, senao, atualize a distancia
            distancias[j][k] = infinity if distancias[j][k] == infinity else calcularDistancia_C_C(clusters[j], clusters[k]) 
            
    for j in range(len(clusters)):
        for k in range(len(clusters)):
            # Se a distancia atualizada for menor que a distancia entre o menor que a distancia entre o cluster mais proximo, atualize o cluster mais proximo
            if distancias[j][k] < distancias[j][cluster_proximo[j]]:
                cluster_proximo[j] = k

    clustersN = nclusters - i - 1

    if clustersN <= kMax:
        with open(dataset + "-averageLink-k" + str(clustersN) + ".clu", "w+") as out:
            for j in range(clustersN):
                for k in range(len(clusters[j].pontos)):
                    out.write(clusters[j].pontos[k].nome + '\t' + str(j) + '\n')
                    
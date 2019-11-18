from sklearn.metrics.cluster import adjusted_rand_score
import re

class ponto:
    nome = ''
    cluster = -1

    def __init__(self, nom, clu):   #construtor
        self.nome = nom
        self.cluster = clu
    
    def getNome(self):
        return self.nome

    def getCluster(self):
        return self.cluster

arq_real = open('datasets/monkeyReal1.clu', 'r')
arq_teste = open('datasets/monkey.txt-k-means-k12.clu', 'r')

pontos_real = []
pontos_real_sort = []
pontos = []
pontos_sort = []

for line in arq_real:
    param = re.split('[ ,\n,\t]', line)
    pontos_real_sort.append(ponto(param[0], int(param[1])))

for line in arq_teste:
    param = re.split('[ ,\n,\t]', line)
    pontos_sort.append(ponto(param[0], int(param[1])))

pontos_real_sort = sorted(pontos_real_sort, key = ponto.getNome)
pontos_sort = sorted(pontos_sort, key = ponto.getNome)

for i in range(0, len(pontos_real_sort)):
    pontos_real.append(pontos_real_sort[i].getCluster())

for i in range(0, len(pontos_sort)):
    pontos.append(pontos_sort[i].getCluster())

print(adjusted_rand_score(pontos_real, pontos))
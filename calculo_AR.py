from sklearn.metrics.cluster import adjusted_rand_score
import re

arq_real = open('datasets/c2ds1-2spReal.clu', 'r')
arq = open('c2ds1-2sp.txt-k-means-k5.clu', 'r')

particao_real = []
particao = []

for line in arq_real:
    param = re.split('[ ,\n,\t]', line)
    particao_real.append(int(param[1]))

for line in arq:
    param = re.split('[ ,\n,\t]', line)
    particao.append(int(param[1]))

print(adjusted_rand_score(particao_real, particao))
# Informações importantes:
# eu testei o primeiro arquivo de entrada, com 5 clusters e com 100000 repetições e o teste demorou por volta de 5 min,
# também testei o peimeiro arquivo de entrada com 5 cluster e com 1000000 repetições e ele ficou rodando por meia hora sem resultado...
# Eu acho que se deizar ele rodar por mais ou menos uma hora e maia ele acaba, mas isso está fora de questão.
# É POSSIVEL OTIMIZAR O CÓDIGO
# Deve ter um jeito de perceber se o programa ja estabilizou (os centróides continuam os mesmos depois de uma rodada) isso ainda não foi feito

# Coisas que ainda prescisamos fazer:
# -> Plotar o resultado em um gráfico com alguma api
# -> Fazer a condição de parada da estabilização dos centróides

import re
import math
from random import randint
from random import seed

# Classe responsável pelos pontos da entrada
# Cada ponto tem suas coordenadas, um nome e qual centróide ele pertence
class ponto:
    nome = ''
    d1 = 0.0
    d2 = 0.0
    centroide = -1

    def __init__(self, nom, num1, num2):   #construtor
        self.nome = nom
        self.d1 = num1
        self.d2 = num2
    
    def mudarCentroide(self, cen):
        self.centroide = cen

# Classe responśavel pelos centróides criados
# Cada centróide possui uma lista de quais pontos ele possui
# um nome (o número dele) e suas coordenadas
class centroide:
    nome = 0
    d1 = 0.0
    d2 = 0.0

    def __init__(self, nom, num1, num2):    #construtor
        self.nome = nom
        self.d1 = num1
        self.d2 = num2
        self.pontos = []
    
    def mudarCoordenada(self):      # Função que re-calcula o centroide a partir da sua lista de pontos
        self.d1 = sum(ponto.d1 for ponto in self.pontos)/len(self.pontos)
        self.d2 = sum(ponto.d2 for ponto in self.pontos)/len(self.pontos)

    def inserePonto(self, ponto):
        self.pontos.append(ponto)

def calcularDistancia(ponto, centroide):    # Função que calcula a distância Euclidiana entre um ponto e um centróide
    return math.sqrt( (ponto.d1-centroide.d1)**2 + (ponto.d2-centroide.d2)**2 )

lista_ponto = []
lista_centroide = []
ncluster = 0
nrep = 0
nome_arq = 'monkey'

#Lendo cada linha do arquivo e inserindo os pontos na lista de pontos
arq = open('datasets/' + nome_arq + '.txt', 'r')
arq.readline()

for line in arq:
    param = re.split('[ ,\n,\t]', line)
    lista_ponto.append(ponto(param[0], float(param[1]), float(param[2])))

print("Quantos clusters?")
ncluster = int(input())
print("Quantas iterações?")
nrep = int(input())

# Criando os centróides
# Para criar os centróides, um ponto randomico é escolhido e é atribuido como um centóide
ponto_qualquer = 0
for cluster in range(0, ncluster):
    ponto_qualquer = randint(0, (len(lista_ponto)-1))
    
    lista_centroide.append(centroide(cluster, lista_ponto[ponto_qualquer].d1, lista_ponto[ponto_qualquer].d2))

menor_centroide = -1
dist = 0.0
menor = 1000.0

# Loop principal, repete nrep vezes o algoritmo
for i in range(0, nrep):

    # Loop que percorre todos os pontos na lista de pontos
    j = iter(lista_ponto)
    for j in lista_ponto:
        menor = 1000.0
        menor_centroide = -1
        
        # Loop que percorre a lista de centróides e calcula a distância entre o centrôide e os pontos
        k = iter(lista_centroide)
        for k in lista_centroide:
            dist = calcularDistancia(j, k)
            
            if(menor > dist):
                menor = dist
                menor_centroide = k.nome
        
        lista_centroide[menor_centroide].inserePonto(j)
        j.mudarCentroide(lista_centroide[menor_centroide].nome)

    if i == nrep-1:
        with open(nome_arq + ".txt-k-means-k" + str(ncluster) + ".clu", "w+") as out:
            for i in lista_ponto:
                out.write(i.nome + '\t' + str(i.centroide) + '\n')

    # Loop que re-calcula os centróides
    m = iter(lista_centroide)
    for m in lista_centroide:
        m.mudarCoordenada()
        m.pontos.clear()



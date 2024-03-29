import numpy as np
import matplotlib.pyplot as plt
import re

data_sets = ['c2ds1-2sp', 'c2ds3-2g', 'monkey']

cluster_algorithms = ['k-means', 'singleLink', 'averageLink']

for data_set_name in data_sets:
    
    arq_txt = open('dataset_plot/' + data_set_name + '.txt', 'r')
    
    #Plotando os clusters Encontrados
    for algorithm_name in cluster_algorithms:

        if data_set_name == 'monkey':
            algorithm_range = range(5,13)
        else : 
            algorithm_range = range(2,6)

        for k in algorithm_range:
            filename = data_set_name +'.txt-' + algorithm_name + '-k' + str(k);
            
            arq_txt.seek(0)
            arq_clu = open('dataset_plot/'+ filename + '.clu', 'r')

            ponto_cluster = {}
            x_array = []
            y_array = []
            cluster_array = []

            #Lendo qual cluster pertence cada ponto
            for line in arq_clu:
                param = re.split('[ ,\n,\t]', line)
                ponto_cluster[param[0]] = param[1]

            #Lendo posicoes dos clusters
            arq_txt.readline()
            for line in arq_txt:
                param = re.split('[ ,\n,\t]', line)
                cluster_array.append(ponto_cluster[ param[0] ])
                x_array.append(float(param[1]))
                y_array.append(float(param[2]))

            x = np.array(x_array)
            y = np.array(y_array)
            Cluster = np.array(cluster_array) 

            fig = plt.figure()
            ax = fig.add_subplot(1,1,1)
            scatter = ax.scatter(x,y,c=Cluster,s=50)
            print("Salvando " + filename + '.png...')
            fig.savefig('plot/' + filename + '.png')
            plt.close(fig)

    #Plotando o cluster Real
    arq_txt.seek(0)
    arq_clu = open('dataset_plot/'+ data_set_name + 'Real.clu', 'r')

    ponto_cluster = {}
    x_array = []
    y_array = []
    cluster_array = []

    #Lendo qual cluster pertence cada ponto
    for line in arq_clu:
        param = re.split('[ ,\n,\t]', line)
        ponto_cluster[param[0]] = param[1]

    #Lendo posicoes dos clusters
    arq_txt.readline()
    for line in arq_txt:
        param = re.split('[ ,\n,\t]', line)
        cluster_array.append(ponto_cluster[ param[0] ])
        x_array.append(float(param[1]))
        y_array.append(float(param[2]))

    x = np.array(x_array)
    y = np.array(y_array)
    Cluster = np.array(cluster_array) 

    fig = plt.figure()
    ax = fig.add_subplot(1,1,1)
    scatter = ax.scatter(x,y,c=Cluster,s=50)
    print("Salvando " + data_set_name + 'Real.png...')
    fig.savefig('plot/' + data_set_name + 'Real.png')
    plt.close(fig)

print("Todos as imagens foram plotadas!")

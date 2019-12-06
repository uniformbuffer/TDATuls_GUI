import numpy as np
import time
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider,Button
from matplotlib import gridspec
from mpl_toolkits.mplot3d import Axes3D
import scipy.stats as st
from ripser import ripser
from sklearn.decomposition import PCA
from persim import PersImage, plot_diagrams, persistent_entropy
from sys import argv
# from TDA.slidingWindow import slidingWindow
import TDATuls as tuls
#se la periodicità del segnale che vedo nella rappresentazione dopo le sliding windows si ripete per tutte le serie di punti piu o meno nelle stesse posizioni (correlazione verticale delle sliding window) significa che in quei punti qualcosa sta succedendo (si suppone proteine che vanno in folding)
from sklearn.metrics.pairwise import pairwise_distances
#import Holes as ho
import networkx as nx

if argv[1] != None:
        data = np.genfromtxt(argv[1], delimiter = ";")

#transpose the data before applying sliding window 10001 x 15 -> 15 x 10001
data = data.transpose()

#remove the time column from data
data = data[1:,] # for dim 0 pick from one to end, for dim 1 leave it as it is

#restore data in its original shape
data = data.transpose()

#### CORRELATION MATRICES AND Persistent Entropy ####
X = data.transpose()
W = tuls.matrix_window(X,100,100)
WCorr = []
shapes = (W[0].shape[0],W[0].shape[0])
for w in W:
	#w is 14x100
	wcorr = np.zeros(shapes) #14x14
	for i in range(w.shape[0]):
		for j in range(w.shape[0]):
			coeff,pvalue = st.pearsonr(w[i,:],w[j,:])
			if coeff > 0 and pvalue < 0.05:
				wcorr[i,j] = coeff
	WCorr.append(wcorr)

# for wc in WCorr:
# 	G = nx.Graph()
# 	G = nx.read_edgelist(to_edgelist(wc))
# 	pos = nx.spring_layout(G)
# 	nx.draw_networkx(G, pos)
# 	nx.draw_networkx_edges(G, pos)
# 	nx.draw_networkx_edge_labels(G,pos,edge_labels=nx.get_edge_attributes(G,'weight'))
# 	plt.show()

corrmatdist = np.zeros(shapes) #14x14
for i,wc1 in enumerate(WCorr):
    if i < 14:
        for j,wc2 in enumerate(WCorr):
            if j < 14:
                corrmatdist[i,j]=tuls.abs_distance(wc1,wc2)


D = pairwise_distances(corrmatdist)
hoDgms = tuls.doRipsFiltration(D,maxHomDim=2,distance_matrix=True)
Pers = tuls.persentropy(hoDgms)
plot_diagrams(hoDgms)

plt.show()

#distance1 sembra dare un risultato concreto
#l'entropia in H1 è 0 e c'è un solo barcode

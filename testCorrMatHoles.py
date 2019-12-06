import numpy as np
import pickle
import time
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider,Button
from matplotlib import gridspec
from mpl_toolkits.mplot3d import Axes3D
import scipy.stats as st
from ripser import ripser
from persim import PersImage, plot_diagrams, persistent_entropy
from sys import argv
# from TDA.slidingWindow import slidingWindow
import TDATuls as tuls
#se la periodicità del segnale che vedo nella rappresentazione dopo le sliding windows si ripete per tutte le serie di punti piu o meno nelle stesse posizioni (correlazione verticale delle sliding window) significa che in quei punti qualcosa sta succedendo (si suppone proteine che vanno in folding)
from sklearn.metrics.pairwise import pairwise_distances
import Holes as ho
import networkx as nx

if argv[1] != None:
        data = np.genfromtxt(argv[1], delimiter = ";")

#transpose the data before applying sliding window 10001 x 15 -> 15 x 10001
data = data.transpose()

#remove the time column from data
data = data[1:,] # for dim 0 pick from one to end, for dim 1 leave it as it is

#restore data in its original shape
data = data.transpose()

#### CORRELATION MATRICES AND HOLES #####
X = data.transpose()
n_signal = X.shape[0]
W = tuls.matrix_window(X,100,100)
WCORR = []
Fil = []
for w in W:
	Wcorr = np.full((n_signal,n_signal),24.0)
	for i in range(n_signal): # 14x14 correlation of signals
		for j in range(n_signal):
			coeff,pvalue = st.pearsonr(X[i,:],X[j,:])
			if coeff > 0 and pvalue < 0.05:
				Wcorr[i,j] = coeff
			else:
				Wcorr[i,j] = 0
	WCORR.append(Wcorr)
for i,wc in enumerate(WCORR):
	if i < len(WCORR):
		G = nx.Graph(wc)
		
		#TODO creare a mano il grafo a partire dalla matrice 
		# for i in range(len(wc)):
		# 	for j in range(len(wc[i])):
		# 		G.add_edge(i,j,weight=wc[i][j])
		cliqueDict = ho.standard_weight_clique_rank_filtration(G)
		with open('clique-%d.pkl'%(i), 'wb') as f:
			pickle.dump(cliqueDict, f, protocol=2)
		ho.persistent_homology_calculation("clique-%d.pkl"%(i), 1, "matrices", ".")
		Fil.append(cliqueDict)
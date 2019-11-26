import numpy as np
import math
import time
import matplotlib.pyplot as plt
from ripser import ripser
import scipy.spatial.distance as dist
from scipy import sparse
from sklearn.metrics.pairwise import pairwise_distances

def abs_distance(A,B):
    assert A.shape[0] == A.shape[1] , "Matrix is not square"
    assert B.shape[0] == B.shape[1] , "Matrix is not square"
    assert A.shape == B.shape , "Matrices have not the same shape"
    
    suum = 0
    for i in range(A.shape[0]):
        for j in range(B.shape[0]):
            suum = suum + np.abs(A[i][j]-B[i][j])
    return suum

def euclidean_distance(A,B):
    assert A.shape[0] == A.shape[1] , "Matrix is not square"
    assert B.shape[0] == B.shape[1] , "Matrix is not square"
    assert A.shape == B.shape , "Matrices have not the same shape"
    
    suum = 0
    for i in range(A.shape[0]):
        for j in range(B.shape[0]):
            suum = suum + (A[i][j]-B[i][j])**2
    return np.sqrt(suum)

def fnorm_distance(A,B):
    assert A.shape[0] == A.shape[1] , "Matrix is not square"
    assert B.shape[0] == B.shape[1] , "Matrix is not square"
    assert A.shape == B.shape , "Matrices have not the same shape"
    
    fnormA = 0
    fnormB = 0
    suumA = 0
    suumB = 0
    for i in range(A.shape[0]):
        for j in range(A.shape[0]):
            suumA = suumA + A[i][j]**2
    for i in range(B.shape[0]):
        for j in range(B.shape[0]):
            suumB = suumB + B[i][j]**2
    fnormA = np.sqrt(suumA)
    fnormB = np.sqrt(suumB)
    return np.abs(fnormA-fnormB)

def frobenius_distance(A,B):
    assert A.shape[0] == A.shape[1] , "Matrix is not square"
    assert B.shape[0] == B.shape[1] , "Matrix is not square"
    assert A.shape == B.shape , "Matrices have not the same shape"

    inner = (A - B) * ((A - B).conj().T)
    trace = np.trace(inner)
    return np.sqrt(trace)

def infinite_distance(A,B):
    assert A.shape[0] == A.shape[1] , "Matrix is not square"
    assert B.shape[0] == B.shape[1] , "Matrix is not square"
    assert A.shape == B.shape , "Matrices have not the same shape"

    MaxList = []
    #fai la somma all'interno della riga e prendi il massimo
    for i in range(A.shape[0]):
        maxlistij = []
        #fai la stessa cosa con i vari elementi della colonna e prendi il massimo
        for j in range(B.shape[0]):
            m = np.abs(A[i][j] - B[i][j])
            maxlistij.append(m)

        MaxList.append(np.max(maxlistij))
    return np.max(MaxList)

def to_edgelist(m):
    N = m.shape[0]
    M = m.shape[1]
    Edge_list = []
    for i in range(N):
        for j in range(M):
            edge = "%d %d {'weight':%f}"%(i,j,m[i][j])
            Edge_list.append(edge)
    return Edge_list

def lsf_setup_dgm(lsf_dgm0):
    """
    Prepare diagram to be computed by persentropy function 
    """
    L = []
    L.append(lsf_dgm0)
    dmg = np.array(L)
    return dmg

def plot_barcodes(dgms, batch_size=1000):
    #l = len(np.array(dgms))
    i = 3
    step = 3
    for dgm in dgms:
        dgm_np = np.array(dgm)
        print(dgm_np.shape)
        #remove the infinity point
        #dgm_np = dgm_np[dgm_np < np.inf]
        print(dgm_np.shape)
        dgm_np = dgm_np.transpose()
        print(dgm_np.shape)
        barcodes_X = dgm_np[0,:]
        print(barcodes_X)
        barcodes_Y = dgm_np[1,:]
        plt.subplot(2,3,i)
        plt.title("Barcode for $H_"+str(i-step)+"$")
        for z in range(barcodes_X.shape[0]):
            plt.hlines(z,barcodes_X[z],barcodes_Y[z])
        i=i+1
        #plt.show()

def doRipsFiltration(X, maxHomDim, distance_matrix=False, metric='euclidean'):
    '''
    :param X: The data onto which performs ripser
    :param maxHomDim: The maximum homology group to compute
    :param distance_matrix: Says if the data passed as X is a distance matrix
    :param metric: The metric used to compute the distance matrix
    '''
    dgms = None
    if(metric == 'euclidean' and distance_matrix):
        #D = pairwise_distances(X,metric="euclidean")
        dgms = ripser(X,maxdim = maxHomDim, distance_matrix=True, metric='euclidean')["dgms"]
    elif(metric == 'euclidean' and not distance_matrix):
        D = pairwise_distances(X,metric='euclidean')
        dgms = ripser(X,maxdim= maxHomDim, distance_matrix=True)
    elif(metric == 'minkowski'):
        D = pairwise_distances(X,metric="minkowski")
        dgms = ripser(D,maxdim = maxHomDim, distance_matrix=True)["dgms"]
    elif(metric == 'chebyshev'):
        D = pairwise_distances(X,metric="chebyshev")
        dgms = ripser(D,maxdim = maxHomDim, distance_matrix=True)["dgms"]
    else: # No distance matrix needs to be computed
        dgms = ripser(X,maxdim = maxHomDim,distance_matrix=False)["dgms"]
    return dgms

def doWindowedRipsFiltration(data,windowSize,overlap, maxHomDim, distance_matrix=False, metric='euclidean'):
	windows = matrix_window(data,windowSize,overlap)
	diagrams = []
	for window in windows:
		dgms = doRipsFiltration(window,maxHomDim, distance_matrix, metric)
		diagrams.push(diagrams)
		print(diagrams)
	return diagrams

def doLowerStarFiltration(x):
    N = x.shape[0]
    I = np.arange(N-1)
    J = np.arange(1, N)
    V = np.maximum(x[0:-1], x[1::])
    # Add vertex birth times along the diagonal of the distance matrix
    I = np.concatenate((I, np.arange(N)))
    J = np.concatenate((J, np.arange(N)))
    V = np.concatenate((V, x))
    #Create the sparse distance matrix
    D = sparse.coo_matrix((V, (I, J)), shape=(N, N)).tocsr()
    dgm0 = ripser(D, maxdim=0, distance_matrix=True)['dgms'][0]
    dgm0 = dgm0[dgm0[:, 1]-dgm0[:, 0] > 1e-3, :]
    return dgm0

def matrix_window(I, dim, dT):
    '''
    Performs the sliding window on an Nxm matrix of signals.
    '''
    N = I.shape[0]
    P = I.shape[1]
    X = []
    NWindows = int(np.floor((P-dim)/dT))
    X = []
    for i in range(NWindows): # per ogni finestra
        idxx = dT*i + np.arange(dim) #0-279, 15-294....
        Z = np.zeros((N,dim))
        #starting and ending point of this particular window
        #on all the signals
        start = int(np.floor(idxx[0]))
        end = int(np.ceil(idxx[-1]))
        for j in range(N): # per ogni vettore i
            #end overflows, give me Z up to j
            if end >= P:
                Z = Z[0:j]
                break
            
            #Z[start:end] = I[j,start:end+1]
            #Z = interp.spline(idx[start:end+1], I[j,start:end+1], idxx)
            Z[j,:] = I[j,start:end+1]
        X.append(Z)
    return np.array(X) # shape will be NWindows x Z where Z is N x dim

def signal_window(I, dim, dT):
    '''
    Performs the sliding window on a one dimensional signal.
    '''
    P = I.shape[0] #all points in the signal
    X = [] # list of arrays representing the windows
    NWindows = int(np.floor((P-dim)/dT))
    for i in range(NWindows): # for each window
        idxx = dT*i + np.arange(dim) #0-279, 15-294....
        Z = np.zeros(dim)
        start = int(np.floor(idxx[0]))
        end = int(np.ceil(idxx[-1]))    
        if end >= P:
            end = P-1
        
        Z = I[start:end+1]
        
        X.append(Z)
    return np.array(X) # shape will be (NWindows x dim, )

def slidingWindow(x, dim, Tau, dT):
    '''
    Performes the sliding window on a single one dimensional signal.
    Author: Christopher J. Tralie
    '''
    N = len(x)
    NWindows = int(np.floor((N-dim*Tau)/dT)) # The number of windows
    if NWindows <= 0:
        print("Error: Tau too large for signal extent")
        return np.zeros((3, dim))
    X = np.zeros((NWindows, dim)) # Create a 2D array which will store all windows
    idx = np.arange(N)
    for i in range(NWindows):
        # Figure out the indices of the samples in this window
        idxx = dT*i + Tau*np.arange(dim) 
        start = int(np.floor(idxx[0]))
        end = int(np.ceil(idxx[-1]))
        if end >= len(x):
            X = X[0:i, :]
            break
        # Do spline interpolation to fill in this window, and place
        # it in the resulting array
        X[i, :] = x[start:end+1]
        #X[i, :] = interp.spline(idx[start:end+1], x[start:end+1], idxx)
    return X

def persentropy(dgms, normalize=False):
    """
    Calculates the persistent entropies of a set of persistent diagrams.
    """
    result = []

    #calculate PE for all diagrams
    for dgm in dgms:
        #array copy of the array to not modify the original diagram
        dgm_np = np.asarray(dgm)
        #substitute the point at infinity with max + 1
        values =[]
        ltot = 0
        _max = None
        infs = []
    
        for row in dgm_np:
            if row[1] == math.inf:
                infs.append(row)
                continue
            li = row[1] - row[0] #lunghezza del barcode
            values.append(li)
            ltot = ltot + li #lunghezza totale dei barcode
            if _max == None or _max < row[1]: #mi salvo il massimo valore della filtrazione + 1 per poterlo sostituire al punto inf
                _max = row[1] 

        _max = _max + 1
        for row in infs:
            li = _max - row[0] #persistent entropy: i punti all'infinito danno contributi ad li e ltot?
            values.append(li)
            ltot = ltot + li
        
        size = len(values)
        ret = 0
        for e in values: #ogni valore e e' un li e faccio la sommatoria come richiede la formula
            ret = ret + e/ltot * math.log(e/ltot)
        if size == 1 and normalize:
            result.append(-ret)
        elif normalize: # normalize [0,1]
            result.append((-1/np.log(size))*ret)
        else:
            result.append(-ret)
    return np.array(result)

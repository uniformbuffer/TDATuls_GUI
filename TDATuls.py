import numpy as np
import math
import time
import matplotlib.pyplot as plt
from ripser import ripser
import scipy.spatial.distance as dist
from scipy import sparse
from sklearn import cluster, datasets, mixture
from sklearn.neighbors import kneighbors_graph
from sklearn.preprocessing import StandardScaler,MinMaxScaler,Normalizer
from sklearn.decomposition import PCA
from sklearn.metrics.pairwise import pairwise_distances

def abs_distance(A,B):
    assert A.shape[0] == A.shape[1] , "Matrix is not square"
    assert B.shape[0] == B.shape[1] , "Matrix is not square"
    assert A.shape == B.shape , "Matrices have not the same shape"
    
    suum = 0
    for i in range(A.shape[0]):
        for j in range(B.shape[0]):
            #print('A',A[i][j])
            #print('B',B[i][j])
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
        dgms = ripser(X,maxdim = maxHomDim, distance_matrix=True, metric='euclidean')["dgms"]
    elif(metric == 'euclidean' and not distance_matrix):
        D = pairwise_distances(X,metric='euclidean')
        dgms = ripser(D,maxdim=maxHomDim, distance_matrix=True)["dgms"]
    elif(metric == 'minkowski'):
        D = pairwise_distances(X,metric="minkowski")
        dgms = ripser(D,maxdim = maxHomDim, distance_matrix=True)["dgms"]
    elif(metric == 'chebyshev'):
        D = pairwise_distances(X,metric="chebyshev")
        dgms = ripser(D,maxdim = maxHomDim, distance_matrix=True)["dgms"]
    else: # No distance matrix needs to be computed
        dgms = ripser(X,maxdim = maxHomDim,distance_matrix=False)["dgms"]
    return dgms

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
	Calculates the persistent entropies of a set of persistence diagrams.
	"""
	result = []
	if not (isinstance(dgms, list) or isinstance(dgms, np.ndarray)):
		dgms = [dgms]
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
			else:
				li = row[1] - row[0] #lunghezza del barcode
				values.append(li)
				ltot = ltot + li #lunghezza totale dei barcode
				if _max == None or _max < row[1]: #mi salvo il massimo valore della filtrazione + 1 per poterlo sostituire al punto inf
					_max = row[1]

		if _max != None:
			_max = _max + 1

			for row in infs:
				li = _max - row[0] #persistent entropy: i punti all'infinito danno contributi ad li e ltot
				values.append(li)
				ltot = ltot + li
        
		size = len(values)
		ret = 0
		for e in values: #ogni valore e è un li e faccio la sommatoria come richiede la formula
			ret = ret + e/ltot * math.log(e/ltot)
		if size == 1 and normalize:
			result.append(-ret)
		elif normalize: # normalize [0,1]
			result.append((-1/np.log(size))*ret)
		else:
			result.append(-ret)
	return np.array(result)

def calculate_windows(size,overlap,limit):
	advancement = size - overlap
	i = 0
	res = []
	while i <= (limit-size):
		res.append(range(i,(i+size)))
		i += advancement

	if i < limit:
		res.append(range(i,limit))
	return res


from multiprocessing.pool import ThreadPool as Pool
pool = Pool(4)

'''
Spikes
'''
def prepare_spike_detection_parameters(data,windows,threshold):
    parameters = []
    t = (data.max() - data.min())/100*threshold
    for w in windows:
        parameters += [(data[w],w.start,t)]
    return parameters


def spike_detection(data,offset,threshold):
    min = data.min()
    argmin = data.argmin()
    max = data.max()
    argmax = data.argmax()
    if max - min >= threshold:
        if argmax >= argmin:
            return (1,offset+argmax)
        else:
            return (-1,offset+argmin)
    else:
        return (0,0)

def filter_spikes(spikes,data_len):
    res = np.full((data_len),0)
    for s in spikes:
        res[s[1]] = s[0]
    return res

def spikes(data,window=None,show=False,threshold=30):
    cols = data.shape[0]
    if data.shape == (cols,):
        data = np.array([data]).transpose()


    print('Calculating spikes...')
    spikes = np.empty((cols,0))
    for i in range(0,data.shape[1]):
        row = np.array([data[:,i]]).transpose()

        if(window != None):
            size,overlap = window
            windows = calculate_windows(size,overlap,len(row))
        else:
            windows = calculate_windows(len(row),0,len(row))

        parameters = prepare_spike_detection_parameters(row,windows,threshold)
        raw_spikes = pool.starmap(spike_detection,parameters)
        filtred_spikes = np.array([filter_spikes(raw_spikes,len(row))]).transpose()
        spikes = np.hstack((spikes,filtred_spikes))

    spikes = np.array(spikes)
    print('Spikes calculated')

    if(show):
        print('Plotting results...')
        cols = np.ceil(np.sqrt(spikes.shape[1]))
        rows = np.ceil(spikes.shape[1]/cols)
        for i in range(0,spikes.shape[1]):
            fig = plt.subplot(rows,cols, i+1)
            plt.ylim(-1,1)
            plt.xlabel('Time')
            plt.ylabel('Direction')
            plt.suptitle('Spikes on '+str(data.shape[1])+' signals with a threshold of '+str(threshold)+'%')
            plt.plot(spikes[:,i])
        print('Results plotted')

        plt.tight_layout()
        plt.show()#block=False
    return spikes



'''
Clusters
'''
def all_clusters(data,parameters={}):
	# ============
	# Set up cluster parameters
	# ============
	print('Calculating all clusters...')
	#plt.figure(figsize=(9 * 2 + 3, 12.5))
	#plt.subplots_adjust(left=.02, right=.98, bottom=.001, top=.96, wspace=.05,
	#                    hspace=.01)

	#plot_num = 1

	params = {'quantile': .3,
					'eps': .3,
					'damping': .9,
					'preference': -200,
					'n_neighbors': 10,
					'n_clusters': 2,
					'min_samples': 20,
					'xi': 0.05,
					'min_cluster_size': 0.1}

	X = data
	params.update(parameters)

	# normalize dataset for easier parameter selection
	X = StandardScaler().fit_transform(X)

	# estimate bandwidth for mean shift
	bandwidth = cluster.estimate_bandwidth(X, quantile=params['quantile'])

	# connectivity matrix for structured Ward
	connectivity = kneighbors_graph(X, n_neighbors=params['n_neighbors'], include_self=False)
	# make connectivity symmetric
	connectivity = 0.5 * (connectivity + connectivity.T)

	# ============
	# Create cluster objects
	# ============
	ms = cluster.MeanShift(bandwidth=bandwidth, bin_seeding=True)
	two_means = cluster.MiniBatchKMeans(n_clusters=params['n_clusters'])
	ward = cluster.AgglomerativeClustering(
		n_clusters=params['n_clusters'], linkage='ward',
		connectivity=connectivity)
	spectral = cluster.SpectralClustering(
		n_clusters=params['n_clusters'], eigen_solver='arpack',
		affinity="nearest_neighbors")
	dbscan = cluster.DBSCAN(eps=params['eps'])
	optics = cluster.OPTICS(min_samples=params['min_samples'],
							xi=params['xi'],
							min_cluster_size=params['min_cluster_size'])
	affinity_propagation = cluster.AffinityPropagation(
		damping=params['damping'], preference=params['preference'])
	average_linkage = cluster.AgglomerativeClustering(
		linkage="average", affinity="cityblock",
		n_clusters=params['n_clusters'], connectivity=connectivity)
	birch = cluster.Birch(n_clusters=params['n_clusters'])
	gmm = mixture.GaussianMixture(
		n_components=params['n_clusters'], covariance_type='full')

	clustering_algorithms = (
		('MiniBatchKMeans', two_means),
		('AffinityPropagation', affinity_propagation),
		('MeanShift', ms),
		('SpectralClustering', spectral),
		('Ward', ward),
		('AgglomerativeClustering', average_linkage),
		('DBSCAN', dbscan),
		('OPTICS', optics),
		('Birch', birch),
		('GaussianMixture', gmm)
	)

	results = {}

	for name, algorithm in clustering_algorithms:
		t0 = time.time()

		# catch warnings related to kneighbors_graph
		with warnings.catch_warnings():
			warnings.filterwarnings(
				"ignore",
				message="the number of connected components of the " +
				"connectivity matrix is [0-9]{1,2}" +
				" > 1. Completing it to avoid stopping the tree early.",
				category=UserWarning)
			warnings.filterwarnings(
				"ignore",
				message="Graph is not fully connected, spectral embedding" +
				" may not work as expected.",
				category=UserWarning)
			algorithm.fit(X)

		results[name] = X[:, 0:1]

	print('Calculation compleded')

	print('Plotting results...')
	#plt.show()#block=False
	print('Results plotted')
	return result


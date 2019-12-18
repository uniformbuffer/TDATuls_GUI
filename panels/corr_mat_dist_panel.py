from export import *
from panels.base_panel import *
from noname import PanelCorrMatDist

class AppPanelCorrMatDist(PanelCorrMatDist,BasePanel):
	def __init__(self, parent,data):
		PanelCorrMatDist.__init__(self, parent=parent.notebook)
		BasePanel.__init__(self, name='CorrMatDist', parent=parent, data=data)

		# Set Label
		self.label_shape.SetLabel(str(self.data.shape))

		# Execute button
		self.btn_execute.Bind(wx.EVT_BUTTON,self.onExecuteButtonClick)
		# Close button
		self.btn_close.Bind(wx.EVT_BUTTON,self.onCloseButtonClick)

		# Slider window size
		self.window_size_slider.Bind(wx.EVT_SCROLL,self.onWindowSizeSliderChange)
		self.window_size_slider.SetMax(self.data.shape[0])

	def onExecuteButtonClick(self, event):
		overlap = self.overlap_slider.GetValue()
		window_size = self.window_size_slider.GetValue()

		#transpose the data before applying sliding window 10001 x 15 -> 15 x 10001
		#data = data.transpose()

		#remove the timecorrelationMatrix column from data
		#data = data[1:,] # for dim 0 pick from one to end, for dim 1 leave it as it is

		#restore data in its original shape
		#data = data.transpose()


		#### CORRELATION MATRICES AND Persistent Entropy ####
		#X = data.transpose()

		windows = calculate_windows(window_size,overlap,self.data.shape[0])
		diagrams = {}
		WCorr = []
		shapes = (self.data.shape[1],self.data.shape[1])
		for window in windows:
			#w is 14x100
			#print(window)
			wcorr = np.zeros((self.data.shape[1],self.data.shape[1])) #14x14
			#print(wcorr.shape)
			for i in range(self.data.shape[1]):
				for j in range(self.data.shape[1]):
					#print(self.data[window].shape,self.data[window][:,i].shape)
					coeff,pvalue = st.pearsonr(self.data[window][:,i],self.data[window][:,j])
					if coeff > 0 and pvalue < 0.05:
						#print('Written ('+str(i)+','+str(j)+') = '+str(coeff))
						wcorr[i,j] = coeff
			#print('wcorr',wcorr)
			WCorr.append(wcorr)
		#print('WCorr',len(WCorr))
		corrmatdist = np.zeros(shapes) #14x14
		self.add_export('','Correlation Matrix Distances',corrmatdist)
		#print(corrmatdist.shape)
		#for i,wc1 in enumerate(WCorr):
		#	if i < 14:
		#		for j,wc2 in enumerate(WCorr):
		#			if j < 14:
		#			    corrmatdist[i,j] = abs_distance(wc1,wc2)

		for i in range(0,len(WCorr)):
			for j in range(0,len(WCorr)):
				corrmatdist[i,j] = abs_distance(WCorr[i],WCorr[j])
				#print(corrmatdist[i,j])

		#print(corrmatdist)
		'''
		#### CORRELATION MATRICES AND Persistent Entropy ####
		print(self.data)
		W = matrix_window(self.data,window_size,window_size-overlap)
		WCorr = []
		print(W)
		shapes = (W.shape[0],W.shape[0])
		print(shapes)
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
				        corrmatdist[i,j]=abs_distance(wc1,wc2)
		'''

		#print('corrmatdist',corrmatdist)
		figure = plt.figure()
		plt.figure(figure.number)
		D = pairwise_distances(corrmatdist)
		self.add_export('','Pairwise Distances',D)
		#print('D',D)
		hoDgms = doRipsFiltration(D,maxHomDim=2,distance_matrix=True)
		#print('Ripser',hoDgms)
		Pers = persentropy(hoDgms)
		self.add_export('','Persistent Entropy',Pers)
		#print('Persentropy',Pers)
		plot_diagrams(hoDgms)
		diagrams['correlation_matrix'] = figure

		#distance1 sembra dare un risultato concreto
		#l'entropia in H1 è 0 e c'è un solo barcode
		wx.adv.NotificationMessage('Done', message="Done")
		self.diagrams = diagrams
		self.updateFigure(0)

	def onWindowSizeSliderChange(self, event):
		self.overlap_slider.SetMax(self.window_size_slider.GetValue())

	def onFigureChange(self, event):
		self.updateFigure(self.figure_list.GetCurrentSelection())



from export import *
from panels.base_panel import *
from noname import PanelCorrMatHoles

class AppPanelCorrMatHoles(PanelCorrMatHoles,BasePanel):
	def __init__(self, parent,data):
		PanelCorrMatHoles.__init__(self, parent=parent.notebook)
		BasePanel.__init__(self, name='CorrMatHoles', parent=parent, data=data)

		# Set Label
		self.label_shape.SetLabel(str(self.data.shape))

		self.btn_open_folder.Bind(wx.EVT_BUTTON,self.onSelectFolder)

		# Execute button
		self.btn_execute.Bind(wx.EVT_BUTTON,self.onExecuteButtonClick)
		# Close button
		self.btn_close.Bind(wx.EVT_BUTTON,self.onCloseButtonClick)


		# Slider window size
		self.window_size_slider.Bind(wx.EVT_SCROLL,self.onWindowSizeSliderChange)
		self.window_size_slider.SetMax(self.data.shape[1])

		self.updateFigure(0)

	def onExportPikle(self,event):
		dialog = wx.DirDialog (None, "Choose output directory", "", wx.DD_DEFAULT_STYLE | wx.DD_DIR_MUST_EXIST)
		if dialog.ShowModal() == wx.ID_CANCEL:
			return
		self.txt_open_folder.SetValue(dialog.GetPath())

	def onSelectFolder(self,event):
		dialog = wx.DirDialog (None, "Choose output directory", "", wx.DD_DEFAULT_STYLE | wx.DD_DIR_MUST_EXIST)
		if dialog.ShowModal() == wx.ID_CANCEL:
			return
		self.txt_open_folder.SetValue(dialog.GetPath())

	def onExecuteButtonClick(self, event):
		overlap = self.overlap_slider.GetValue()
		window_size = self.window_size_slider.GetValue()
		windows = calculate_windows(window_size,overlap,self.data.shape[1])
		output_path = self.txt_open_folder.GetValue()
		if not os.path.isdir(output_path):
			wx.adv.NotificationMessage('Error', message="Output directory does not exist")
			print('Output directory does not exist')
			return
		diagrams = {}

		#### CORRELATION MATRICES AND HOLES #####
		X = self.data.transpose()
		n_signal = X.shape[0]
		W = matrix_window(X,window_size,window_size-overlap)
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
				#figure = plt.figure()
				#plt.figure(figure.number)

				G = nx.Graph(wc)

				#TODO creare a mano il grafo a partire dalla matrice
				# for i in range(len(wc)):
				# 	for j in range(len(wc[i])):
				# 		G.add_edge(i,j,weight=wc[i][j])
				cliqueDict = ho.standard_weight_clique_rank_filtration(G)
				with open('clique-%d.pkl'%(i), 'wb') as f:
					pickle.dump(cliqueDict, f, protocol=2)
				ho.persistent_homology_calculation(os.path.join(output_path,"clique-%d.pkl"%(i)), 1, "matrices", ".")
				Fil.append(cliqueDict)
				#diagrams['window'+str(i)] = figure


		wx.adv.NotificationMessage('Done', message="Done")
		self.diagrams = diagrams
		self.updateFigure(0)

	def onEntropyCheck(self, event):
		mainSizer = self.GetSizer()
		# First child is canvasSizer, the second is settingsSizer
		canvasSizer = mainSizer.GetChildren()[0].GetSizer()
		optionalCanvasSizer = canvasSizer.GetChildren()[1].GetSizer()
		if self.chx_entropy.IsChecked(): # Box is checked and I need to add the pe plot
			self.pe_Figure = Figure()
			self.pe_axes = self.pe_Figure.add_subplot(111)
			self.pe_canvas = FigureCanvas(self, -1, self.pe_Figure)
			self.pe_toolbar = NavigationToolbar(self.pe_canvas)
			self.pe_toolbar.Realize()

			optionalCanvasSizer.Add(self.pe_canvas, 1, wx.ALL)
			optionalCanvasSizer.Add(self.pe_toolbar, 0, wx.LEFT | wx.EXPAND)
			self.SetSizer(mainSizer)
			self.Layout() # automatically reshape the page to fit the pe plot
		else: # Check is unchecked and I need to remove the pe plot
			# i remove them by simply destroying children of the sizer
			optionalCanvasSizer.Clear(True)
			optionalCanvasSizer.Layout()

	def onWindowSizeSliderChange(self, event):
		self.overlap_slider.SetMax(self.window_size_slider.GetValue())

	def onFigureChange(self, event):
		self.updateFigure(self.figure_list.GetCurrentSelection())


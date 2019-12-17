from export import *
from panels.base_panel import *
from noname import PanelLowerStar


	# Now we override the behaviour of the lowerStar menu selection
	# The change here requires to select on which data to perform the filtration
# Now we override the behaviour of the Panel page for lower star filtration
class AppPanelLowerStar(PanelLowerStar,BasePanel):
	def __init__(self, parent,data):
		PanelLowerStar.__init__(self, parent=parent.notebook)
		BasePanel.__init__(self, name='LowerStar', parent=parent, data=data)

		# Set Label
		self.label_shape.SetLabel(str(self.data.shape))

		# Entropy check
		self.persistent_entropy = False
		self.chx_entropy.Bind(wx.EVT_CHECKBOX,self.onEntropyCheck)

		# Execute button
		self.btn_execute.Bind(wx.EVT_BUTTON,self.onExecuteButtonClick)

		# Close button
		self.btn_close.Bind(wx.EVT_BUTTON,self.onCloseButtonClick)

		# Overlap slider
		# SpinCtrl window size
		self.window_size_slider.Bind(wx.EVT_SCROLL,self.onWindowSizeSliderChange)
		self.window_size_slider.SetMax(self.data.shape[0])
		self.window_size = self.window_size_slider.GetValue()

		# Choice for selecting the signal
		if self.data.dtype.names == None:
			list = []
			for i in range(0,self.data.shape[1]):
				list.append(str(i))
			self.ch_signal.SetItems(list)
		else:
			self.ch_signal.SetItems(self.data.dtype.names)
		self.ch_signal.SetSelection(0)

	def onExecuteButtonClick(self, event):
		window_size = self.window_size_slider.GetValue()
		overlap = self.overlap_slider.GetValue()
		signal_index = self.ch_signal.GetCurrentSelection()
		windows = calculate_windows(window_size,overlap,self.data.shape[0])
		diagrams = {}

		norm_pers = []
		i = 0
		for window in windows:
			#Lower Star Filtration
			figure = plt.figure()
			plt.figure(figure.number)
			lsf_dgm0 = doLowerStarFiltration(self.data[window,signal_index])
			plt.plot(lsf_dgm0)
			diagrams['window'+str(i)+': lower star filtration'] = figure

			if self.chx_entropy.IsChecked():
				# Persistent Entropy
				L = []
				L.append(lsf_dgm0)
				dmg = np.array(L)
				ent = persentropy(dmg)[0]

				# Normalized Persistent Entropy
				pent = persentropy(dmg,normalize=True)[0]
				norm_pers.append(pent)
			i += 1

		if self.chx_entropy.IsChecked():
			figure = plt.figure()
			plt.figure(figure.number)
			plt.plot(np.arange(len(windows)),norm_pers)
			diagrams['normalized persistent entropy'] = figure

		wx.adv.NotificationMessage('Done', message="Done")
		self.diagrams = diagrams
		self.updateFigure(0)

	def onEntropyCheck(self, event):
		self.persistent_entropy = self.chx_entropy.IsChecked()

	def onWindowSizeSliderChange(self, event):
		self.overlap_slider.SetMax(self.window_size_slider.GetValue())

	def onFigureChange(self, event):
		self.updateFigure(self.figure_list.GetCurrentSelection())


from export import *
from panels.base_panel import *
from noname import PanelAgglomerativeClustering

class AppPanelAgglomerativeClustering(PanelAgglomerativeClustering,BasePanel):
	def __init__(self, parent,data):
		PanelAgglomerativeClustering.__init__(self, parent=parent.notebook)
		BasePanel.__init__(self, name='AgglomerativeClustering', parent=parent, data=data)

		# Set Label
		self.label_shape.SetLabel(str(self.data.shape))

		# Execute button
		self.btn_execute.Bind(wx.EVT_BUTTON,self.onExecuteButtonClick)
		# Close button
		self.btn_close.Bind(wx.EVT_BUTTON,self.onCloseButtonClick)

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
		nclusters = int(self.ncluster_textctrl.GetValue())
		if nclusters < 2:
			print("Error: Number of clusters must be greater then 2")
			return
		neighbors = int(self.neighbors_textctrl.GetValue())
		signal_index = self.ch_signal.GetCurrentSelection()
		diagrams = {}
		name = 'AgglomerativeClustering'
		data = self.data[:,signal_index]
		time_line = np.arange(len(data))
		timed_data = np.vstack((time_line,data)).transpose()

		connectivity = kneighbors_graph(timed_data, n_neighbors=neighbors, include_self=False)
		algorithm = cluster.AgglomerativeClustering(linkage="average", affinity="cityblock",n_clusters=nclusters, connectivity=connectivity)
		figure = plt.figure()
		plt.figure(figure.number)

		plot_cluster(name,algorithm,timed_data)

		diagrams[name] = figure

		wx.adv.NotificationMessage('Done', message="Done")
		self.diagrams = diagrams
		self.updateFigure(0)

	def onWindowSizeSliderChange(self, event):
		self.overlap_slider.SetMax(self.window_size_slider.GetValue())

	def onFigureChange(self, event):
		self.updateFigure(self.figure_list.GetCurrentSelection())


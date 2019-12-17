from export import *
from panels.base_panel import *
from noname import PanelMiniBatchKMeans

class AppPanelMiniBatchKMeans(PanelMiniBatchKMeans,BasePanel):
	def __init__(self, parent,data):
		PanelMiniBatchKMeans.__init__(self, parent=parent.notebook)
		BasePanel.__init__(self, name='MiniBatchKMeans', parent=parent, data=data)

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
		signal_index = self.ch_signal.GetCurrentSelection()

		diagrams = {}
		name = 'MiniBatchKMeans'
		data = self.data[:,signal_index]
		time_line = np.arange(len(data))
		timed_data = np.vstack((time_line,data)).transpose()

		algorithm = cluster.MiniBatchKMeans(n_clusters=nclusters)
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


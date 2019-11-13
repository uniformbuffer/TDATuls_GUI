import wx
from numpy import arange, sin, pi
import matplotlib
matplotlib.use('WXAgg')

from matplotlib.backends.backend_wxagg import FigureCanvasWxAgg as FigureCanvas
from matplotlib.backends.backend_wx import NavigationToolbar2Wx
from matplotlib.figure import Figure

class MyFrame(wx.Frame):
    def __init__(self,parent,title):
        super(MyFrame,self).__init__(parent,title=title)
        
        self.menuBar = wx.MenuBar()

        # File menu
        file_menu = wx.Menu()
        #wx.App.SetMacExitMenuItemId(wx.ID_EXIT)
        exit_item = file_menu.Append(wx.ID_EXIT, "E&xit\tCtrl-Q", "Exit NodeMCU PyFlasher")
        self.Bind(wx.EVT_MENU, self._on_exit_app, exit_item)
        self.menuBar.Append(file_menu, "&File")

        # Filtrations menu
        filtration_menu = wx.Menu()
        sliding_window_menu = wx.Menu()
        corr_mat_menu = wx.Menu()
        lower_star_item = sliding_window_menu.Append(wx.ID_ANY, 'L&ower star', 'Create a new lower star')
        matrix_window_item = sliding_window_menu.Append(wx.ID_ANY,'R&ipser window','Create a new ripser')
        corr_mat_dist_item = corr_mat_menu.Append(wx.ID_ANY,'Correlation matrix distance','create a new correlation matrix distance')
        corr_mat_holes_item = corr_mat_menu.Append(wx.ID_ANY,'Correlation matrix and holes','create a new correlation matrix holes')
        cluster_item = filtration_menu.Append(wx.ID_ANY,'C&luster','Start a new clustering filtration')
        filtration_menu.AppendSubMenu(sliding_window_menu,'Sliding window')
        filtration_menu.AppendSubMenu(corr_mat_menu,'Correlation matrix')
        self.Bind(wx.EVT_MENU,self._on_new_sliding_window, lower_star_item)
        self.Bind(wx.EVT_MENU,self._on_new_cluster,cluster_item)
        self.menuBar.Append(filtration_menu,'New Operation')

        # Help menu
        help_menu = wx.Menu()
        help_item = help_menu.Append(wx.ID_ABOUT, '&About NodeMCU PyFlasher', 'About')
        self.Bind(wx.EVT_MENU, self._on_help_about, help_item)
        self.menuBar.Append(help_menu, '&Help')

        self.SetMenuBar(self.menuBar)

        self.panel = wx.Panel(self)
        self.nb = wx.Notebook(self.panel)

        sizer = wx.BoxSizer()
        sizer.Add(self.nb,1,wx.EXPAND)
        self.panel.SetSizer(sizer)

    def _on_exit_app(self,event):
        print("Exiting...")

    def _on_help_about(self,event):
        print("Now you are looking at help file")

    def _on_new_sliding_window(self,event):
        page = CanvasPanelLowerStar(self.nb)
        label = wx.StaticText(page,label="This is a new sliding window")
        self.nb.AddPage(page,"Sliding Window")
        print("New page added")
    def _on_new_cluster(self,event):
        page = wx.CanvasPanel(self.nb)
        label = wx.StaticText(page,label="This is a new cluster")
        self.nb.AddPage(page,"Cluster")
        print("New page added")

class CanvasPanel(wx.Panel):
    def __init__(self,parent):
        wx.Panel.__init__(self, parent)
        self.figure = Figure()
        self.axes = self.figure.add_subplot(111)
        self.canvas = FigureCanvas(self, -1, self.figure)
        #---------------------SIZER-------------------------
        self.btn = wx.Button(self,label="click,me")


        self.sizer = wx.BoxSizer(wx.VERTICAL)
        self.sizer.Add(self.canvas, 1, wx.LEFT | wx.TOP | wx.GROW)
        self.sizer.Add(self.btn,2,wx.TOP)
        self.SetSizer(self.sizer)
        self.Fit()

class CanvasPanelLowerStar(wx.Panel):
    def __init__(self,parent):
        wx.Panel.__init__(self,parent)
        self.figure = Figure()
        self.axes1 = self.figure.add_subplot(111)
        self.axes2 = self.figure.add_subplot(121)
        self.canvas = FigureCanvas(self,-1,self.figure)

        self.sizer = wx.BoxSizer(wx.VERTICAL)
        self.sizer.Add(self.canvas, 1, wx.LEFT | wx.TOP | wx.GROW)
        self.SetSizer(self.sizer)
        self.Fit()

class MyApp(wx.App):
    def OnInit(self):
        self.frame = MyFrame(parent=None,title="Main Window")
        self.frame.Show()

        return True

if __name__ == "__main__":
    app = MyApp()
    app.MainLoop()
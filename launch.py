import wx
from noname import MainFrame

class TDATulsApp (wx.App):
    def OnInit(self):
        self.frame = MainFrame(parent=None)
        self.frame.Show()

        return True

if __name__ == "__main__":
    app = TDATulsApp()
    app.MainLoop()

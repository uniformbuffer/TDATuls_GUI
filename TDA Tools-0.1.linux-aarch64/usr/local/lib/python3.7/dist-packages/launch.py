import wx
from app import AppFrame

class TDATulsApp (wx.App):
    def OnInit(self):
        self.frame = AppFrame(parent=None)
        self.frame.Show()

        return True

if __name__ == "__main__":
    app = TDATulsApp()
    app.MainLoop()

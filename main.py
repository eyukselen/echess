import wx
import sys
from wx.svg import SVGimage


# region high dpi settings for windows
if sys.platform == 'win32':
    # import ctypes
    from ctypes import OleDLL
    try:
        # ctypes.windll.shcore.SetProcessDpiAwareness(True)
        # ctypes.OleDLL('shcore').SetProcessDpiAwareness(1)
        OleDLL('shcore').SetProcessDpiAwareness(1)
        pass
    except (AttributeError, OSError):
        pass
# endregion


class Pieces(wx.Panel):
    def __init__(self) -> None:
        lst = {'kl': 'Chess_klt45.svg',
               'ql': 'Chess_qlt45.svg',
               'rl': 'Chess_rlt45.svg',
               'nl': 'Chess_nlt45.svg',
               'bl': 'Chess_blt45.svg',
               'pl': 'Chess_plt45.svg',
               'kd': 'Chess_kdt45.svg',
               'qd': 'Chess_qdt45.svg',
               'rd': 'Chess_rdt45.svg',
               'nd': 'Chess_ndt45.svg',
               'bd': 'Chess_bdt45.svg',
               'pd': 'Chess_pdt45.svg',
               }
        pieces = {}
        for k, v in lst.items():
            img = SVGimage.CreateFromFile(v)
            bmp = img.ConvertToScaledBitmap(wx.Size(96, 96), self)
            pieces[k] = bmp
        self.pieces = pieces


class Board(wx.Panel):
    def __init__(self, parent, id):
        wx.Panel.__init__(self, parent, id)
        self.square_size = 128
        self.sq_margin = self.square_size * 0.15
        self.dark_sq = wx.Colour(148, 120, 86)
        self.light_sq = wx.Colour(214, 198, 140)
        self.SetBackgroundColour("grey")
        self.Bind(wx.EVT_PAINT, self.OnPaint)
        self.pieces = Pieces()
        self.kl = self.pieces.pieces['kl']
        self.ql = self.pieces.pieces['ql']
        self.nl = self.pieces.pieces['nl']
        self.bl = self.pieces.pieces['bl']
        self.rl = self.pieces.pieces['rl']
        self.pl = self.pieces.pieces['pl']
        self.kd = self.pieces.pieces['kd']
        self.qd = self.pieces.pieces['qd']
        self.nd = self.pieces.pieces['nd']
        self.bd = self.pieces.pieces['bd']
        self.rd = self.pieces.pieces['rd']
        self.pd = self.pieces.pieces['pd']

    def OnPaint(self, evt):
        self.dc = wx.PaintDC(self)
        for x in range(8):
            for y in range(8):
                if (x + y) % 2 == 0:
                    self.dc.SetBrush(wx.Brush(self.light_sq))
                else:
                    self.dc.SetBrush(wx.Brush(self.dark_sq))
                self.dc.DrawRectangle(x * self.square_size, y * self.square_size, self.square_size, self.square_size)    

        # # Draw the pieces
        # i = 0
        # for k, v in self.pieces.pieces.items():
        #     i += 1
        #     self.dc.DrawBitmap(v, 100 * i + 16, 100 * i + 16, True)
        for i in range(8):
            self.dc.DrawBitmap(self.pd, i * self.square_size + self.sq_margin, 1 * self.square_size + self.sq_margin, True)
            self.dc.DrawBitmap(self.pl, i * self.square_size + self.sq_margin, 6 * self.square_size + self.sq_margin, True)
        
        self.dc.DrawBitmap(self.rl, 0 * self.square_size + self.sq_margin, 7 * self.square_size + self.sq_margin, True)
        self.dc.DrawBitmap(self.nl, 1 * self.square_size + self.sq_margin, 7 * self.square_size + self.sq_margin, True)
        self.dc.DrawBitmap(self.bl, 2 * self.square_size + self.sq_margin, 7 * self.square_size + self.sq_margin, True)
        self.dc.DrawBitmap(self.ql, 3 * self.square_size + self.sq_margin, 7 * self.square_size + self.sq_margin, True)
        self.dc.DrawBitmap(self.kl, 4 * self.square_size + self.sq_margin, 7 * self.square_size + self.sq_margin, True)
        self.dc.DrawBitmap(self.bl, 5 * self.square_size + self.sq_margin, 7 * self.square_size + self.sq_margin, True)
        self.dc.DrawBitmap(self.nl, 6 * self.square_size + self.sq_margin, 7 * self.square_size + self.sq_margin, True)
        self.dc.DrawBitmap(self.rl, 7 * self.square_size + self.sq_margin, 7 * self.square_size + self.sq_margin, True)

        self.dc.DrawBitmap(self.rd, 0 * self.square_size + self.sq_margin, self.sq_margin, True)
        self.dc.DrawBitmap(self.nd, 1 * self.square_size + self.sq_margin, self.sq_margin, True)
        self.dc.DrawBitmap(self.bd, 2 * self.square_size + self.sq_margin, self.sq_margin, True)
        self.dc.DrawBitmap(self.qd, 3 * self.square_size + self.sq_margin, self.sq_margin, True)
        self.dc.DrawBitmap(self.kd, 4 * self.square_size + self.sq_margin, self.sq_margin, True)
        self.dc.DrawBitmap(self.bd, 5 * self.square_size + self.sq_margin, self.sq_margin, True)
        self.dc.DrawBitmap(self.nd, 6 * self.square_size + self.sq_margin, self.sq_margin, True)
        self.dc.DrawBitmap(self.rd, 7 * self.square_size + self.sq_margin, self.sq_margin, True)

        del self.dc

    def positionPieces():
        pass


class MainWindow(wx.Frame):
    def __init__(self, parent):
        wx.Frame.__init__(self, parent, title='chess game')
        self.SetSize((1600, 1200))
        self.main_panel = wx.Panel(parent=self)
        self.main_panel.SetBackgroundColour('yellow')
        self.main_sizer = wx.BoxSizer(wx.VERTICAL)
        self.main_panel.SetSizer(self.main_sizer)
        self.board = Board(self.main_panel, -1)
        self.main_sizer.Add(self.board, 1, wx.EXPAND)
        self.Show()


app = wx.App()
MainWindow(None)
app.MainLoop()

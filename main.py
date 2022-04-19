import wx.lib.inspection  # for debugging
import wx
import wx.grid as gridlib
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


class Piece:
    def __init__(self, svg, name, def_pos):
        img = SVGimage.CreateFromFile(svg)
        self.bmp = img.ConvertToScaledBitmap(wx.Size(96, 96), window=None)
        self.name = name
        self.pos = def_pos
        bg = BoardGeometry()
        self.coord = bg.board_pos[self.pos]
        self.fullscreen = False
        self.shown = True

    def HitTest(self, pt):
        rect = self.GetRect()
        return rect.Contains(pt)

    def GetRect(self):
        return wx.Rect(self.coord[0], self.coord[1],
                       self.bmp.GetWidth(), self.bmp.GetHeight())

    def Draw(self, dc, op=wx.COPY):
        memDC = wx.MemoryDC()
        memDC.SelectObject(self.bmp)
        dc.Blit(self.coord[0], self.coord[1],
                self.bmp.GetWidth(), self.bmp.GetHeight(),
                memDC, 0, 0, op, True)
    
    def move(self):
        pass


class BoardGeometry:
    def __init__(self):
        self.piece_size = (96, 96)
        self.square_size = 100
        self.piece_margin = self.square_size - self.piece_size[0]

        self.files = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']
        self.ranks = ['1', '2', '3', '4', '5', '6', '7', '8']
        self.ranks.reverse()
        self.coords = [f + r for f in self.files for r in self.ranks]
        self.board_pos = {}

        for f in self.files:
            for r in self.ranks:
                self.board_pos[f + r] = (self.files.index(f) * self.square_size + self.piece_margin,
                                         self.ranks.index(r) * self.square_size + self.piece_margin)
        self.ranks.reverse()


class Pieces:
    def __init__(self) -> None:
        self.wr1 = Piece('Chess_rlt45.svg', 'White Rook', 'a1')
        self.wn1 = Piece('Chess_nlt45.svg', 'White Knight', 'b1')
        self.wb1 = Piece('Chess_blt45.svg', 'White Bishop', 'c1')
        self.wq = Piece('Chess_qlt45.svg', 'White Queen', 'd1')
        self.wk = Piece('Chess_klt45.svg', 'White King', 'e1')
        self.wb2 = Piece('Chess_blt45.svg', 'White Bishop', 'f1')
        self.wn2 = Piece('Chess_nlt45.svg', 'White Knight', 'g1')
        self.wr2 = Piece('Chess_rlt45.svg', 'White Rook', 'h1')
        self.wp1 = Piece('Chess_plt45.svg', 'White Pawn', 'a2')
        self.wp2 = Piece('Chess_plt45.svg', 'White Pawn', 'b2')
        self.wp3 = Piece('Chess_plt45.svg', 'White Pawn', 'c2')
        self.wp4 = Piece('Chess_plt45.svg', 'White Pawn', 'd2')
        self.wp5 = Piece('Chess_plt45.svg', 'White Pawn', 'e2')
        self.wp6 = Piece('Chess_plt45.svg', 'White Pawn', 'f2')
        self.wp7 = Piece('Chess_plt45.svg', 'White Pawn', 'g2')
        self.wp8 = Piece('Chess_plt45.svg', 'White Pawn', 'h2')

        self.br1 = Piece('Chess_rdt45.svg', 'Black Rook', 'a8')
        self.bn1 = Piece('Chess_ndt45.svg', 'Black Knight', 'b8')
        self.bb1 = Piece('Chess_bdt45.svg', 'Black Bishop', 'c8')
        self.bq = Piece('Chess_qdt45.svg', 'Black Queen', 'd8')
        self.bk = Piece('Chess_kdt45.svg', 'Black King', 'e8')
        self.bb2 = Piece('Chess_bdt45.svg', 'Black Bishop', 'f8')
        self.bn2 = Piece('Chess_ndt45.svg', 'Black Knight', 'g8')
        self.br2 = Piece('Chess_rdt45.svg', 'Black Rook', 'h8')

        self.bp1 = Piece('Chess_pdt45.svg', 'Black Pawn', 'a7')
        self.bp2 = Piece('Chess_pdt45.svg', 'Black Pawn', 'b7')
        self.bp3 = Piece('Chess_pdt45.svg', 'Black Pawn', 'c7')
        self.bp4 = Piece('Chess_pdt45.svg', 'Black Pawn', 'd7')
        self.bp5 = Piece('Chess_pdt45.svg', 'Black Pawn', 'e7')
        self.bp6 = Piece('Chess_pdt45.svg', 'Black Pawn', 'f7')
        self.bp7 = Piece('Chess_pdt45.svg', 'Black Pawn', 'g7')
        self.bp8 = Piece('Chess_pdt45.svg', 'Black Pawn', 'h7')
        self.all_pieces = [self.wr1, self.wn1, self.wb1, self.wq, self.wk,self.wb2, self.wn2, self.wr2,
                           self.wp1, self.wp2, self.wp3, self.wp4, self.wp5, self.wp6, self.wp7, self.wp8,
                           self.br1, self.bn1, self.bb1, self.bq, self.bk, self.bb2, self.bn2, self.br2,
                           self.bp1, self.bp2, self.bp3, self.bp4, self.bp5, self.bp6, self.bp7, self.bp8,
                           ]


class MoveEditor(gridlib.Grid):
    def __init__(self, parent, id) -> None:
        gridlib.Grid.__init__(self, parent, -1)
        self.CreateGrid(0, 2)
        self.SetSize(wx.Size(200, 200))
        self.SetWindowStyleFlag(wx.VSCROLL)
        self.SetRowLabelSize(64)
        self.SetColLabelValue(0, 'White')
        self.SetColLabelValue(1, 'Black')
        self.SetCornerLabelValue('Moves')
        self.ShowScrollbars(horz=False, vert=True)
        self.history = []

    def add_move(self, move):
        self.history.append(move)
        self.AppendRows(1)
        self.SetSize(self.GetSize()[0], self.GetSize()[1] + self.GetRowSize(0))
        self.InvalidateBestSize()
        self.GetParent().Layout()
        
        row = self.GetNumberRows() - 1
        col = 0
        if move.split('-')[0] == 'b':
            col = 1
        self.SetCellValue(row, col, move)

    def clear_history(self):
        self.history = []


class Board(wx.Panel):
    def __init__(self, parent, id):
        wx.Panel.__init__(self, parent, id)
        # geometry
        self.dark_sq = wx.Colour(148, 120, 86)
        self.light_sq = wx.Colour(214, 198, 140)
        self.SetBackgroundColour("tan")
        # logical geometry
        self.bg = BoardGeometry()
        # pieces
        self.pieces = Pieces()
        self.selected = None
        self.drag_piece = None
        self.drag_image = None
        self.hilite_piece = None

        self.Bind(wx.EVT_PAINT, self.OnPaint)
        self.Bind(wx.EVT_LEFT_DOWN, self.on_left_down)
        self.Bind(wx.EVT_LEFT_UP, self.on_left_up)
        self.Bind(wx.EVT_MOTION, self.on_mouse_move)

    def on_left_up(self, event):

        if not self.drag_image or not self.drag_piece:
            self.drag_image = None
            self.drag_image = None
            return

        sq_old = self.drag_piece.pos
        sq_new = self.find_square(event.GetPosition())
        print(sq_old, sq_new)
        turn = 'b'
        if self.drag_piece.name.startswith('White'):
            turn = 'w'

        move = str(turn) + '-' + str(sq_old) + '-' + str(sq_new)
        self.GetParent().GetParent().move_editor.add_move(move)

        self.drag_image.Hide()
        self.drag_image.EndDrag()
        self.drag_image = None

        self.drag_piece.pos = sq_new
        self.drag_piece.coord = self.bg.board_pos[sq_new]

        self.drag_piece.shown = True
        self.RefreshRect(self.drag_piece.GetRect())
        self.drag_piece = None

        self.Refresh()

    def on_left_down(self, event):
        self.find_square(event.GetPosition())
        piece = self.find_piece(event.GetPosition())

        if piece:
            print(piece.name)
            self.drag_piece = piece
            self.drag_start_coord = event.GetPosition()
        # print(self.find_square(event.GetPosition()))

    def on_mouse_move(self, event):
        if (
                not self.drag_piece or
                not event.Dragging() or
                not event.LeftIsDown()
        ):
            return

        # if we have a shape, but haven't started dragging yet
        if self.drag_piece and not self.drag_image:
            # only start the drag after having moved a couple pixels
            tolerance = 2
            pt = event.GetPosition()
            dx = abs(pt.x - self.drag_start_coord.x)
            dy = abs(pt.y - self.drag_start_coord.y)
            if dx <= tolerance and dy <= tolerance:
                return

            # refresh the area of the window where the shape was so it
            # will get erased.
            self.drag_piece.shown = False
            self.RefreshRect(self.drag_piece.GetRect(), True)
            # refresh whole board
            self.Update()

            item = self.drag_piece.bmp
            self.drag_image = wx.DragImage(item, wx.Cursor(wx.CURSOR_HAND))

            hotspot = self.drag_start_coord - self.drag_piece.coord
            self.drag_image.BeginDrag(hotspot, self, False)

            self.drag_image.Move(pt)
            self.drag_image.Show()

        # if we have shape and image then move it, posibly highlighting another shape.
        elif self.drag_piece and self.drag_image:
            onShape = self.find_piece(event.GetPosition())
            unhiliteOld = False
            hiliteNew = False

            # figure out what to hilite and what to unhilite
            if self.hilite_piece:
                if onShape is None or self.hilite_piece is not onShape:
                    unhiliteOld = True

            if onShape and onShape is not self.hilite_piece and onShape.shown:
                hiliteNew = True

            # if needed, hide the drag image so we can update the window
            if unhiliteOld or hiliteNew:
                self.drag_image.Hide()

            if unhiliteOld:
                dc = wx.ClientDC(self)
                self.hilite_piece.Draw(dc)
                self.hilite_piece = None

            if hiliteNew:
                dc = wx.ClientDC(self)
                self.hilite_piece = onShape
                self.hilite_piece.Draw(dc, wx.INVERT)

            # now move it and show it again if needed
            self.drag_image.Move(event.GetPosition())
            if unhiliteOld or hiliteNew:
                self.drag_image.Show()

    def find_piece(self, pt):
        for piece in self.pieces.all_pieces:
            if piece.HitTest(pt):
                return piece
        return None

    def find_square(self, pt):
        x, y = pt
        if x <= self.bg.square_size * 8 and y <= self.bg.square_size * 8:
            coord_rank = 7 - int(y / self.bg.square_size)
            coord_file = int(x / self.bg.square_size)
            return self.bg.files[coord_file] + self.bg.ranks[coord_rank]

    def draw_pieces(self, dc):
        for piece in self.pieces.all_pieces:
            piece.Draw(dc)

    def draw_board(self, dc):
        # self.dc = wx.PaintDC(self)
        # self.dc = wx.PaintDC(self)
        for x in range(8):
            for y in range(8):
                if (x + y) % 2 == 0:
                    dc.SetBrush(wx.Brush(self.light_sq))
                else:
                    dc.SetBrush(wx.Brush(self.dark_sq))
                dc.DrawRectangle(x * self.bg.square_size,
                                 y * self.bg.square_size,
                                 self.bg.square_size,
                                 self.bg.square_size)

    def OnPaint(self, event):
        self.dc = wx.PaintDC(self)
        self.draw_board(self.dc)
        self.draw_pieces(self.dc)


class MainWindow(wx.Frame):
    def __init__(self, parent):
        wx.Frame.__init__(self, parent, title='chess game')
        self.SetBackgroundColour('white')
        self.SetSize((1200, 900))
        self.mother_sizer = wx.BoxSizer(wx.VERTICAL)
        self.SetSizer(self.mother_sizer)

        self.main_panel = wx.Panel(parent=self)
        self.main_panel.SetBackgroundColour('wheet')
        self.main_sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.main_panel.SetSizer(self.main_sizer)

        self.board = Board(self.main_panel, -1)
        self.move_editor = MoveEditor(self.main_panel, -1)
        self.move_editor.FitInside()

        self.main_sizer.Add(self.board, 1, wx.EXPAND)
        self.main_sizer.Add(self.move_editor, 0, wx.RIGHT)
        self.mother_sizer.Add(self.main_panel, 1, wx.EXPAND)
        self.Show()


app = wx.App()
MainWindow(None)
wx.lib.inspection.InspectionTool().Show()  # for inspecting ui stuff
app.MainLoop()

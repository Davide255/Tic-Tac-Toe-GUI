from kivymd.uix.boxlayout import MDBoxLayout
from kivy.uix.gridlayout import GridLayout
from kivymd.uix.label import MDLabel
from kivy.uix.behaviors import ButtonBehavior

from kivy.graphics import Line, Color

class SymbolBox(ButtonBehavior, MDLabel):
    def __init__(self, number, **kwargs):
        super().__init__(**kwargs)
        self.number = number
        self.font_style = 'H1'
        self.halign = 'center'
        self.valign = 'center'
        self.bind(on_press = lambda *args: args[0].parent.parent.callbacks[self.number](self))

class Board(MDBoxLayout):

    callbacks = {}
    cells = {}
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.padding = (40,10,40,40)
        self.orientation = 'vertical'
        self.spacing = 10

        title = MDLabel(text = '[b]Tic-Tac-Toe Game[/b]', markup=True, halign = 'center')
        title.font_size = 40
        title.color = (0,0,0,1)
        title.size_hint_y = None
        title.height = 50
        self.add_widget(title)

        self.hint_text = MDLabel(text='Game Start!', halign = 'center')
        self.hint_text.bold = False
        self.hint_text.font_size = 20
        self.hint_text.size_hint_y = None
        self.hint_text.height = 20
        self.add_widget(self.hint_text)

        self.table = GridLayout(cols=3, rows=3)

        for i in range(9):
            cell = SymbolBox(i)
            self.cells[i] = cell
            self.table.add_widget(cell)
            self.callbacks[i] = lambda *args: None

        self.add_widget(self.table)

    def _draw_lines(self, *args):
        
        for i in self.canvas.children:
            if isinstance(i, Line): self.canvas.remove(i)

        first_colon_line = [
            round(self.cells[0].pos[0] + self.cells[0].size[0]),
            round(self.cells[0].pos[1] + self.cells[0].size[1]),

            round(self.cells[6].pos[0] + self.cells[6].size[0]),
            round(self.cells[6].pos[1])
        ]

        with self.canvas:
            Color(0,0,0,1)
            Line(points=first_colon_line, width=3)

        second_colon_line = [
            round(self.cells[2].pos[0]),
            round(self.cells[2].pos[1] + self.cells[2].size[1]),

            round(self.cells[8].pos[0]),
            round(self.cells[8].pos[1])
        ]

        with self.canvas:
            Color(0,0,0,1)
            Line(points=second_colon_line, width=3)

        first_raw_line = [
            *self.cells[0].pos,
            self.cells[2].pos[0] + self.cells[2].size[0],
            self.cells[2].pos[1]
        ]

        with self.canvas:
            Color(0,0,0,1)
            Line(points=first_raw_line, width=3)

        second_raw_line = [
            self.cells[6].pos[0],
            self.cells[6].pos[1] + self.cells[6].size[1],
            self.cells[8].pos[0] + self.cells[8].size[0],
            self.cells[8].pos[1] + self.cells[8].size[1]
        ]

        with self.canvas:
            Color(0,0,0,1)
            Line(points=second_raw_line, width=3)

        return self

    def set_callback(self, cell, callback):
        if callable(callback): self.callbacks[cell] = callback
    
    def set_cell_sign(self, cell, sign):
        if not self.cells[cell].text == '': raise AttributeError(
                'Cell number {} has already a symbol!'.format(cell)
        )
        self.cells[cell].text = str(sign)
    
    def clear(self):
        for i in self.cells:
            self.cells[i].text = ''
            self.callbacks[i] = lambda: None

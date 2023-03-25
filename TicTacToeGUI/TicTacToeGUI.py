from kivymd.app import MDApp
from kivymd.uix.button import MDFlatButton
from kivymd.uix.dialog import MDDialog
from .board import Board
from kivy.clock import Clock, mainthread
from kivy.core.window import Window
from threading import Thread, Timer

from random import choice

class TicTacToeGUI(MDApp):

    free_places = []
    busy_places = {
        'O':[],
        'X':[]
    }
    dialog: MDDialog = None

    last_move = None

    def build(self):
        self.title = 'Tic-Tac-Toe GUI'
        self.root = Board()
        self.free_places = [n for n in range(9)]
        self.hint_text = self.root.hint_text
        Window.bind(on_resize = self.root._draw_lines)
        Clock.schedule_once(self.root._draw_lines)
        Thread(target=self.start, daemon=True).start()
        return self.root

    def start(self, *args):
        turn = 'O'
        while self.check_status() == None:
            if turn == 'O':
                self.set_hint_text('Tocca a te')
                cell = self.wait_user()
                self.set_cell_sign(cell, 'O')
                turn = 'X'
            else:
                self.set_hint_text('Faccio la mia mossa.')
                self.wait(.5)
                move = self.computer_move()
                self.set_cell_sign(move, 'X')
                turn = 'O'
        
        self.set_hint_text('Congradulazioni {}, hai vinto!'.format(self.check_status()))
        self.wait(1)
        if not self.ask_to_play_again():
            self.close()
        else: 
            self.clear()
            self.start()

    def computer_move(self):
        return choice(self.free_places)

    @classmethod
    def wait(cls, seconds):
        class Time: stop = False

        t = Timer(seconds, setattr, (Time, 'stop', True))
        t.setDaemon(True)
        t.start()

        while not Time.stop: pass
        return
    
    @classmethod
    def set_callback(cls, cell, callback):
        cls.get_running_app().root.set_callback(cell, callback)

    @classmethod
    def set_hint_text(cls, text):
        cls.get_running_app().root.hint_text.text = str(text)

    @classmethod
    def set_cell_sign(cls, cell, sign):
        self = cls.get_running_app()
        self.root.set_cell_sign(cell, sign)
        self.busy_places[sign].append(cell)
        self.free_places.remove(cell)
        self.last_move = [cell, sign]
    
    @classmethod
    def clear(cls):
        self = cls.get_running_app()
        self.root.clear()
        self.free_places = [n for n in range(9)]
        self.busy_places = {
            'O':[],
            'X':[]
        }

    @classmethod
    def get_cell_sign(cls, cell):
        return cls.get_running_app().root.cells[cell].text

    @classmethod
    def wait_user(cls):
        self = cls.get_running_app()
        old = self.root.callbacks

        class Clicked(object): 
            clicked = False
            cell_number = 0

        self.root.callbacks = {
            i : lambda *args: [setattr(Clicked, 'clicked', True), setattr(Clicked, 'cell_number', args[0].number)] \
                for i in range(9)}
        while not Clicked.clicked: pass
        self.root.callbacks = old
        self.root.callbacks[Clicked.cell_number]()
        return Clicked.cell_number

    @classmethod
    def check_status(cls):
        self = cls.get_running_app()

        possibilities = [
            [0,1,2],
            [3,4,5],
            [6,7,8],

            [0,3,6],
            [1,4,7],
            [2,5,8],

            [0,4,8],
            [2,4,6]
        ]

        for i in self.busy_places.keys():
            for p in possibilities:
                if set(p).issubset(self.busy_places[i]):
                    return i

        if len(self.free_places) == 0: return 'Nobody'
        return None

    @classmethod
    def ask_to_play_again(cls):
        self = cls.get_running_app()
        self.choice = None

        @mainthread
        def add_dialog(self):
            no_button = MDFlatButton(
                        text="NO",
                        theme_text_color="Custom",
                        text_color=self.theme_cls.primary_color,
                    )
            no_button.bind(on_release = lambda wdg: [
                setattr(self, 'choice', False),
                wdg.parent.parent.parent.parent.dismiss()
                ])
            yes_button = MDFlatButton(
                        text="SI",
                        theme_text_color="Custom",
                        text_color=self.theme_cls.primary_color,
                    )
            yes_button.bind(on_release = lambda wdg: [
                setattr(self, 'choice', True),
                wdg.parent.parent.parent.parent.dismiss()
                ])
            
            dialog = MDDialog(
                title='Vuoi giocare di nuovo?',
                buttons=[
                    no_button,
                    yes_button
                ],
            )
            dialog.bind(on_dismiss = lambda *args: setattr(self, 'choice', True) if self.choice == None else None)
            self.dialog = dialog
            self.dialog.open()
        
        if not self.dialog:
            add_dialog(self)
        else:
            Clock.schedule_once(lambda *args: self.dialog.open())
        
        while self.choice == None: pass

        res = self.choice
        del self.choice
        return res
    
    @classmethod
    @mainthread
    def close(cls):
        cls.get_running_app().stop()

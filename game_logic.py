from TicTacToeGUI import TicTacToeGUI
from random import choice

gui = TicTacToeGUI()

def computer(*args):
    # if the center is free set the computer move on the center
    # else randomically choose a place
    if gui.get_cell_sign(4) == '':
        return 4
    else: choice(gui.free_places)

gui.computer_move = computer

gui.run()

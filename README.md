# Tic-Tac-Toe GUI

Simple GUI for Tic-Tac-Toe game.

## Simple:
To start, import the main GUI frame
``` python
from TicTacToeGUI import TicTacToeGUI
```
After that, we must initiate the GUI by the assignement of a variable
``` python
gui = TicTacToeGUI()
```
Now we are ready to start our program by calling the <code>run()</code> function
``` python
gui.run()
```
[_Here the full code_](https://github.com/Davide255/Tic-Tac-Toe-GUI/blob/main/simple.py)

## Create your own game logic:
To substitute our game logic to the default we must create our logic function:
``` python
def computer(*args):
    # if the center is free set the computer move on the center
    # else randomically choose a place
    if gui.get_cell_sign(4) == '':
        return 4
    else: choice(gui.free_places)
```
Now we have to replace the default function with our function:
``` python
gui.computer_move = computer
```
We're ready to call the <code>gui.run()</code> method and to play with our own game logic!

[_Here the full code_](https://github.com/Davide255/Tic-Tac-Toe-GUI/blob/main/game_logic.py)

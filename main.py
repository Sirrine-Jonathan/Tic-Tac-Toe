# Tic Tac Toe Game Board   ===========================================
import tkinter as tk
from tkinter import font as tkFont
from math import floor
from time import sleep

config = {
    "rows": 3,
    "cols": 3,
    "blank": ' ',
    "x_turn": True,
    "btns": {}
}

def check_win():
    '''Examines the board and checks for a win'''
    last_row = config.get("rows") - 1
    last_col = config.get("cols") - 1
    cols = False
    diagonals = False
    for row in range(0, config.get("rows")):
        if cols == False: cols = []
        if diagonals == False: diagonals = [[], []]
        row_winner = True
        row_val = False
        for col in range(0, config.get("cols")):
            val = config['btns'][row][col]['text']
            if col == row: diagonals[0].append(val)
            if col == (config.get("cols") - row - 1): diagonals[1].insert(0, val)
            if row == 0: cols.append([])
            cols[col].append(val)
            if row_val == False: row_val = val
            if row_val != val: row_winner = False
            # Checking the last column in a row
            if col >= last_col:
                if row_winner and val != config.get('blank'): 
                    player_wins(row, 0, type="Row")
                else:
                    row_val = False
            # Checking the last row
            if row >= last_row:
                if len(set(cols[col])) == 1 and cols[col][0] != config.get('blank'):
                    player_wins(0, col, type="Column")
            # Checking the last cell
            if row >= last_row and col >= last_col:
                if (len(set(diagonals[0])) == 1 and diagonals[0][0] != config.get('blank')):
                    player_wins(floor(config.get('rows') / 2), floor(config.get('cols') / 2), type="Diagonal Backward")
                elif (len(set(diagonals[1])) == 1 and diagonals[1][0] != config.get('blank')):
                    player_wins(floor(config.get('rows') / 2), floor(config.get('cols') / 2), type="Diagonal Forward")
            row_val = val

def highlightWin(row, col, type):
    win_color = "#66FF66"
    if type == "Row":
        for col in range(0, config.get("cols")):
            config['btns'][row][col]['bg'] = win_color
            config['btns'][row][col].config(font=fontWin)
    elif type == "Column":
        for row in range(0, config.get("rows")):
            config['btns'][row][col]['bg'] = win_color
            config['btns'][row][col].config(font=fontWin)
    elif type == "Diagonal Forward":
        for row in range(0, config.get("rows")):
            config['btns'][row][config.get("cols") - row - 1]['bg'] = win_color
            config['btns'][row][config.get("cols") - row - 1].config(font=fontWin)
    elif type == "Diagonal Backward":
        for row in range(0, config.get("rows")):
            config['btns'][row][row]['bg'] = win_color
            config['btns'][row][row].config(font=fontWin)
    if config['x_turn']:
        display["text"] = "O Wins!"
    else:
        display["text"] = "X Wins!"

def player_wins(row, col, type="unknown"):
    winner = config['btns'][row][col]['text']
    disableAll()
    if (type != "unknown"):
        highlightWin(row, col, type)

def reset():
    for row in range(0, config.get("rows")):
        for col in range(0, config.get("cols")):
            cell = config['btns'][row][col]
            cell['text'] = config['blank']
            cell['bg'] = "#fff"
            cell['font'] = fontNormal
            cell['state'] = tk.NORMAL
    config['x_turn'] = True
    display['text'] = "X's Turn"

def disableAll():
    for row in range(0, config.get("rows")):
        for col in range(0, config.get("cols")):
            config['btns'][row][col]["state"] = tk.DISABLED


def update_cell(event):
    """Updates a cell on the board, bound to a button"""
    widget = event.widget
    txt = widget['text']
    if (txt != config.get("blank")):
        return
    if txt == config.get("blank") and config.get("x_turn"):
        widget['text'] = 'X'
        widget["state"] = tk.DISABLED
        config["x_turn"] = False
        display['text'] = "O's Turn"
    elif txt == config.get("blank") and not(config.get("x_turn")):
        widget['text'] = 'O'
        widget["state"] = tk.DISABLED
        config["x_turn"] = True
        display['text'] = "X's Turn"
    check_win()

root = tk.Tk()
root.title("Tic Tac Toe")
root.geometry("400x300");
fontNormal = tkFont.Font(family="Helvetica", size=36, weight="normal")
fontWin = tkFont.Font(family="Helvetica", size=36, weight="bold")
fontControl = tkFont.Font(family="Helvetica", size=16, weight="normal")

screen = tk.Frame(root)
screen.rowconfigure(0, weight=1)

game = tk.Frame(screen)
game.rowconfigure([0, 1, 2], minsize=5, weight=1)
game.columnconfigure([0, 1, 2], minsize=5, weight=1)

for row in range(0, config.get("rows")):
    config['btns'][row] = {}
    for col in range(0, config.get("cols")):
        btn = tk.Button(
            master=game,
            text=config["blank"],
            width=5,
            height=5,
            bg="#fff",
            fg="#000",
            font=fontNormal
        )
        btn.grid(row=row, column=col, sticky="nsew")
        btn.bind("<Button-1>", lambda e: update_cell(e))
        config['btns'][row][col] = btn

controls = tk.Frame(screen)
controls.columnconfigure([0], minsize=10, weight=2)
controls.columnconfigure([1], minsize=10, weight=1)

starting_display_text = "X's Turn"
if (not(config['x_turn'])):
    starting_display_text = "O's Turn"
display = tk.Label(master=controls, font=fontControl, height=1, text=starting_display_text)
display.grid(row=0, column=0, sticky="nsew")
resetBtn = tk.Button(master=controls, width=5, height=1,text="Reset", bg="#ff4444", activebackground="#ff4444", fg="#fff", activeforeground="#fff", font=fontControl, command=reset, relief="groove")
resetBtn.grid(row=0, column=1, sticky="nsew", padx=5, pady=5)

controls.pack(side="top", fill="x")
game.pack(side="bottom", fill="x")

screen.pack()


root.mainloop()
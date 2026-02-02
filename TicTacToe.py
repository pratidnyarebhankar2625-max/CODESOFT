import tkinter as tk
from tkinter import messagebox

# ===== YOUR ATTRIBUTES =====
size_of_board = 600
symbol_size = int((size_of_board / 3 - size_of_board / 8) / 2)
symbol_thickness = 5   # Tkinter uses smaller numbers
symbol_X_color = "#EE3591"
symbol_O_color = "#27B61A"
Green_color = "#4F28CE"

PLAYER = "X"
AI = "O"
EMPTY = ""

board = [[EMPTY for _ in range(3)] for _ in range(3)]

# ===== GAME LOGIC =====
def check_winner(b):
    for i in range(3):
        if b[i][0] == b[i][1] == b[i][2] != EMPTY:
            return b[i][0]
        if b[0][i] == b[1][i] == b[2][i] != EMPTY:
            return b[0][i]

    if b[0][0] == b[1][1] == b[2][2] != EMPTY:
        return b[0][0]
    if b[0][2] == b[1][1] == b[2][0] != EMPTY:
        return b[0][2]

    if all(b[i][j] != EMPTY for i in range(3) for j in range(3)):
        return "Draw"
    return None

def minimax(b, is_ai):
    winner = check_winner(b)
    if winner == AI:
        return 1
    if winner == PLAYER:
        return -1
    if winner == "Draw":
        return 0

    if is_ai:
        best = -float("inf")
        for i in range(3):
            for j in range(3):
                if b[i][j] == EMPTY:
                    b[i][j] = AI
                    score = minimax(b, False)
                    b[i][j] = EMPTY
                    best = max(best, score)
        return best
    else:
        best = float("inf")
        for i in range(3):
            for j in range(3):
                if b[i][j] == EMPTY:
                    b[i][j] = PLAYER
                    score = minimax(b, True)
                    b[i][j] = EMPTY
                    best = min(best, score)
        return best

def ai_move():
    best_score = -float("inf")
    move = None
    for i in range(3):
        for j in range(3):
            if board[i][j] == EMPTY:
                board[i][j] = AI
                score = minimax(board, False)
                board[i][j] = EMPTY
                if score > best_score:
                    best_score = score
                    move = (i, j)
    if move:
        i, j = move
        board[i][j] = AI
        buttons[i][j].config(text=AI, fg=symbol_O_color)

def on_click(i, j):
    if board[i][j] != EMPTY:
        return

    board[i][j] = PLAYER
    buttons[i][j].config(text=PLAYER, fg=symbol_X_color)

    if check_game_end():
        return

    ai_move()
    check_game_end()

def check_game_end():
    winner = check_winner(board)
    if winner:
        if winner == "Draw":
            messagebox.showinfo("Game Over", "It's a Draw!")
        else:
            messagebox.showinfo("Game Over", f"{winner} Wins!")
        reset_game()
        return True
    return False

def reset_game():
    for i in range(3):
        for j in range(3):
            board[i][j] = EMPTY
            buttons[i][j].config(text="", fg="black")

# ===== GUI SETUP =====
root = tk.Tk()
root.title("AI Tic Tac Toe (Unbeatable)")
root.geometry(f"{size_of_board}x{size_of_board}")
root.configure(bg=Green_color)

buttons = [[None for _ in range(3)] for _ in range(3)]

btn_size = size_of_board // 3

for i in range(3):
    for j in range(3):
        btn = tk.Button(
            root,
            text="",
            font=("Arial", symbol_size, "bold"),
            width=btn_size,
            height=btn_size,
            bg="white",
            bd=symbol_thickness,
            highlightbackground=Green_color,
            command=lambda i=i, j=j: on_click(i, j)
        )
        btn.place(x=j * btn_size, y=i * btn_size,
                  width=btn_size, height=btn_size)
        buttons[i][j] = btn

root.mainloop()

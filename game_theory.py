# -*- coding: utf-8 -*-
"""
Created on Thu Jun 19 16:45:53 2025

@author: evert
"""

def print_board(board):
    print("\n")
    for row in board:
        print(" | ".join(row))
        print("-" * 9)
    print()

def check_winner(board, player):
    # Check rows, columns and diagonals
    win_lines = (
        board,
        zip(*board),  # columns
        [[board[i][i] for i in range(3)]],  # main diagonal
        [[board[i][2 - i] for i in range(3)]]  # anti-diagonal
    )
    for lines in win_lines:
        for line in lines:
            if all(cell == player for cell in line):
                return True
    return False

def is_draw(board):
    return all(cell != " " for row in board for cell in row)

def get_move(player, board):
    while True:
        try:
            move = input(f"Player {player}, enter your move (row and column: 1 1 for top-left): ")
            row, col = map(int, move.strip().split())
            row -= 1
            col -= 1
            if board[row][col] == " ":
                return row, col
            else:
                print("❗ That cell is already taken.")
        except (ValueError, IndexError):
            print("❗ Invalid input. Please enter row and column as two numbers from 1 to 3 (e.g., '2 3').")

def play_game():
    board = [[" " for _ in range(3)] for _ in range(3)]
    current_player = "X"

    print("Welcome to Tic-Tac-Toe!")
    print_board(board)

    while True:
        row, col = get_move(current_player, board)
        board[row][col] = current_player
        print_board(board)

        if check_winner(board, current_player):
            print(f"🎉 Player {current_player} wins!")
            break
        if is_draw(board):
            print("🤝 It's a draw!")
            break

        current_player = "O" if current_player == "X" else "X"

if __name__ == "__main__":
    while True:
        play_game()
        again = input("Play again? (y/n): ").strip().lower()
        if again != "y":
            print("Thanks for playing!")
            break


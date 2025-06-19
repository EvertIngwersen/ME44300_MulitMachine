# -*- coding: utf-8 -*-
"""
Created on Thu Jun 19 16:45:53 2025

@author: evert
"""

import random

def print_board(board):
    print("\n")
    for row in board:
        print(" | ".join(row))
        print("-" * 9)
    print()

def check_winner(board, player):
    win_lines = (
        board,
        zip(*board),
        [[board[i][i] for i in range(3)]],
        [[board[i][2 - i] for i in range(3)]]
    )
    for lines in win_lines:
        for line in lines:
            if all(cell == player for cell in line):
                return True
    return False

def is_draw(board):
    return all(cell != " " for row in board for cell in row)

def get_human_move(board):
    while True:
        try:
            move = input("Your move (row col): ")
            row, col = map(int, move.strip().split())
            row -= 1
            col -= 1
            if board[row][col] == " ":
                return row, col
            else:
                print("❗ Cell already taken.")
        except (ValueError, IndexError):
            print("❗ Invalid input. Use two numbers from 1 to 3.")

def get_available_moves(board):
    return [(r, c) for r in range(3) for c in range(3) if board[r][c] == " "]

def make_move(board, row, col, player):
    board[row][col] = player

def copy_board(board):
    return [row[:] for row in board]

def ai_move(board):
    # 1. Win if possible
    for row, col in get_available_moves(board):
        test_board = copy_board(board)
        make_move(test_board, row, col, "O")
        if check_winner(test_board, "O"):
            return row, col

    # 2. Block opponent's win
    for row, col in get_available_moves(board):
        test_board = copy_board(board)
        make_move(test_board, row, col, "X")
        if check_winner(test_board, "X"):
            return row, col

    # 3. Otherwise random
    return random.choice(get_available_moves(board))

def play_game():
    board = [[" " for _ in range(3)] for _ in range(3)]
    print("Welcome to Tic-Tac-Toe! You are X, AI is O.")
    print_board(board)

    while True:
        # Human move
        row, col = get_human_move(board)
        make_move(board, row, col, "X")
        print_board(board)

        if check_winner(board, "X"):
            print("🎉 You win!")
            break
        if is_draw(board):
            print("🤝 It's a draw!")
            break

        # AI move
        print("AI is thinking...")
        row, col = ai_move(board)
        make_move(board, row, col, "O")
        print_board(board)

        if check_winner(board, "O"):
            print("💀 AI wins! Better luck next time.")
            break
        if is_draw(board):
            print("🤝 It's a draw!")
            break

if __name__ == "__main__":
    while True:
        play_game()
        again = input("Play again? (y/n): ").lower()
        if again != "y":
            print("Goodbye!")
            break



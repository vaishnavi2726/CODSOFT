# Tic-Tac-Toe game

# Function to print the board
def print_board(board):
    for row in board:
        print(" | ".join(row))
        print("-" * 10)

# Function to check if someone has won
def check_winner(board, player):
    # Check rows, columns, and diagonals
    for i in range(3):
        if all([cell == player for cell in board[i]]):  # Check row
            return True
        if all([board[j][i] == player for j in range(3)]):  # Check column
            return True
    if board[0][0] == player and board[1][1] == player and board[2][2] == player:  # Check diagonal
        return True
    if board[0][2] == player and board[1][1] == player and board[2][0] == player:  # Check other diagonal
        return True
    return False

# Function to check if the board is full (draw)
def board_full(board):
    for row in board:
        if " " in row:
            return False
    return True

# Function to get valid player move
def get_move():
    while True:
        try:
            row = int(input("Enter row (0, 1, 2): "))
            col = int(input("Enter column (0, 1, 2): "))
            if row not in range(3) or col not in range(3):
                print("Invalid input! Row and column must be between 0 and 2.")
            else:
                return row, col
        except ValueError:
            print("Invalid input! Please enter numbers only.")

# Main function to control the game
def tic_tac_toe():
    while True:  # Loop to restart the game after it ends
        # Initialize the board
        board = [[" " for _ in range(3)] for _ in range(3)]
        current_player = "X"  # Player X starts first

        while True:
            print_board(board)
            print(f"your {current_player}'s turn")

            # Get player move
            row, col = get_move()
            
            if board[row][col] != " ":
                print("Cell already taken,  try once more!")
                continue

            # Place the player's mark on the board
            board[row][col] = current_player

            # Check for winner
            if check_winner(board, current_player):
                print_board(board)
                print(f" {current_player} wins!")
                break

            # Check for draw
            if board_full(board):
                print_board(board)
                print("It's a draw!")
                break

            # Switch players
            current_player = "O" if current_player == "X" else "X"

        # Ask if the players want to restart
        restart = input("Do you want to play again? (y/n): ").lower()
        if restart != 'y':
            print("Thanks for playing we hope you enjoyed!")
            break  # Exit the game loop if they don't want to restart

# Run the game
if __name__ == "__main__":
    tic_tac_toe()

import time

from algorithm import AIPlayer
from player import Player



class Board:
    def __init__(self, size=3):
        self.size = size
        self.grid = [[' ' for _ in range(size)] for _ in range(size)]
        self.current_player = None

    def is_valid_move(self, move):
        row = (move - 1) // self.size
        col = (move - 1) % self.size
        return self.grid[row][col] == ' '

    def make_move(self, move, symbol):
        row = (move - 1) // self.size
        col = (move - 1) % self.size
        if self.is_valid_move(move):
            self.grid[row][col] = symbol
            return True
        return False

    def check_winner(self):
        # check rows
        for row in self.grid:
            if row.count(row[0]) == self.size and row[0] != ' ':
                return row[0]

        # check columns
        for col in range(self.size):
            if all(self.grid[row][col] == self.grid[0][col] != ' ' for row in range(self.size)):
                return self.grid[0][col]

        # check diagonals
        if all(self.grid[i][i] == self.grid[0][0] != ' ' for i in range(self.size)):
            return self.grid[0][0]
        if all(self.grid[i][self.size-1-i] == self.grid[0][self.size-1] != ' ' for i in range(self.size)):
            return self.grid[0][self.size-1]

        # check tie
        if all(cell != ' ' for row in self.grid for cell in row):
            return 'Tie'

        return None

    def display(self):
        max_width = len(str(self.size * self.size))  
        cell_width = max(max_width, 3)  # Ensure at least 3 spaces for X and O centering
        for i, row in enumerate(self.grid):
            display_row = []
            for j, cell in enumerate(row):
                if cell == ' ':
                    num = str(i * self.size + j + 1)
                    display_row.append(num.rjust(cell_width))  # right justify the number
                else:
                    display_row.append(cell.center(cell_width))  # center the X or O with consistent width
            print(' | '.join(display_row))
            if i < self.size - 1:  # don't print divider after the last row
                print('-' * (self.size * (cell_width + 3) - 1))

    def get_available_moves(self):
        return [i * self.size + j + 1 for i in range(self.size) for j in range(self.size) if self.grid[i][j] == ' ']

    def undo_move(self, move):
        row = (move - 1) // self.size
        col = (move - 1) % self.size
        self.grid[row][col] = ' '

def show_settings_menu():
    while True:
        print("\nSettings Menu:")
        print("1. Change grid size")
        print("2. Go back")
        
        choice = input("Enter your choice (1-2): ")
        if choice == "1":
            while True:
                try:
                    size = int(input("Enter new grid size (3-5): "))
                    if 3 <= size <= 5:
                        return size
                    print("Please enter a size between 3 and 5.")
                except ValueError:
                    print("Please enter a valid number.")
        elif choice == "2":
            return None
        else:
            print("Invalid choice. Please try again.")

def show_main_menu():
    grid_size = 3  # Default grid size
    
    while True:
        print("\nMain Menu:")
        print("1. Start game")
        print("2. Change settings")
        
        choice = input("Enter your choice (1-2): ")
        
        if choice == "2":
            new_size = show_settings_menu()
            if new_size:
                grid_size = new_size
        elif choice == "1":
            return grid_size
        else:
            print("Invalid choice. Please try again.")

def main():
    print("Welcome to Tic-Tac-Toe!")
    
    # Show main menu and get grid size
    grid_size = show_main_menu()
    
    print("\nChoose game mode:")
    print("1. Human vs Human")
    print("2. Human vs AI (Minimax)")
    print("3. Human vs AI (Alpha-Beta)")
    print("4. AI vs AI (Minimax vs Alpha-Beta)")

    mode = input("Enter your choice (1-4): ")
    while mode not in ["1", "2", "3", "4"]:
        print("Invalid choice. Try again.")
        mode = input("Enter your choice (1-4): ")

    player1 = Player("Player 1", "X")
    player2 = Player("Player 2", "O")

    if mode == "2":
        player2 = AIPlayer("AI (Minimax)", "O")
    elif mode == "3":
        player2 = AIPlayer("AI (Alpha-Beta)", "O", use_alpha_beta=True)
    elif mode == "4":
        player1 = AIPlayer("AI (Minimax)", "X")
        player2 = AIPlayer("AI (Alpha-Beta)", "O", use_alpha_beta=True)

    board = Board(grid_size)
    current_player = player1

    print(f"Starting game with {grid_size}x{grid_size} grid")
    print(f"Enter moves using numbers 1-{grid_size*grid_size}")

    while True:
        board.display()
        time.sleep(1)

        move = current_player.make_move(board)
        board.make_move(move, current_player.symbol)

        winner = board.check_winner()
        if winner:
            board.display()
            if winner == 'Tie':
                print("It's a tie!")
            else:
                print(f"{current_player.name} wins!")
            break

        # Switch players
        current_player = player2 if current_player == player1 else player1

if __name__ == "__main__":
    main() 
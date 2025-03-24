import time

class Player:
    def __init__(self, name, symbol):
        self.name = name
        self.symbol = symbol  # 'X' or 'O'

    def make_move(self, board):
        # override this method in the AI class
        while True:
            try:
                move = int(input(f"{self.name}, enter number (1-9): "))
                if 1 <= move <= 9 and board.is_valid_move(move):
                    return move
                else:
                    print("Invalid move! Try again.")
            except ValueError:
                print("Please enter a number between 1 and 9!")

class Board:
    def __init__(self):
        self.grid = [[' ' for _ in range(3)] for _ in range(3)]
        self.current_player = None

    def is_valid_move(self, move):
        row = (move - 1) // 3
        col = (move - 1) % 3
        return self.grid[row][col] == ' '

    def make_move(self, move, symbol):
        row = (move - 1) // 3
        col = (move - 1) % 3
        if self.is_valid_move(move):
            self.grid[row][col] = symbol
            return True
        return False

    def check_winner(self):
        # check rows
        for row in self.grid:
            if row.count(row[0]) == 3 and row[0] != ' ':
                return row[0]

        # check columns
        for col in range(3):
            if self.grid[0][col] == self.grid[1][col] == self.grid[2][col] != ' ':
                return self.grid[0][col]

        # check diagonals
        if self.grid[0][0] == self.grid[1][1] == self.grid[2][2] != ' ':
            return self.grid[0][0]
        if self.grid[0][2] == self.grid[1][1] == self.grid[2][0] != ' ':
            return self.grid[0][2]

        # check tie
        if all(cell != ' ' for row in self.grid for cell in row):
            return 'Tie'

        return None

    def display(self):
        for i, row in enumerate(self.grid):
            display_row = []
            for j, cell in enumerate(row):
                if cell == ' ':
                    display_row.append(str(i * 3 + j + 1))
                else:
                    display_row.append(cell)
            print(' | '.join(display_row))
            if i < 2:  #  don't print divider after the last row
                print('-' * 9)

def main():
    player1 = Player("Player 1", "X")
    player2 = Player("Player 2", "O")
    
    board = Board()
    current_player = player1
    
    print("Welcome to Tic-Tac-Toe!")
    print("Enter moves using numbers 1-9")
    
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
            
        # switch players
        current_player = player2 if current_player == player1 else player1
        

if __name__ == "__main__":
    main() 
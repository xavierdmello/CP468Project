class Player:
    def __init__(self, name, symbol):
        self.name = name
        self.symbol = symbol  # 'X' or 'O'

    def make_move(self, board):
        while True:
            try:
                max_moves = board.size * board.size
                move = int(input(f"{self.name}, enter number (1-{max_moves}): "))
                if 1 <= move <= max_moves and board.is_valid_move(move):
                    return move
                else:
                    print("Invalid move! Try again.")
            except ValueError:
                print(f"Please enter a number between 1 and {max_moves}!")
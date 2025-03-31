import time


class Player:
    def __init__(self, name, symbol):
        self.name = name
        self.symbol = symbol  # 'X' or 'O'
        self.total_thinking_time = 0

    def make_move(self, board):
        while True:
            try:
                max_moves = board.size * board.size
                start_time = time.time()
                move = int(input(f"{self.name}, enter number (1-{max_moves}): "))
                if 1 <= move <= max_moves and board.is_valid_move(move):
                    end_time = time.time()
                    thinking_time = end_time - start_time
                    self.total_thinking_time += thinking_time
                    return move
                else:
                    print("Invalid move! Try again.")
            except ValueError:
                print(f"Please enter a number between 1 and {max_moves}!")
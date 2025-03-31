import time
import math

from player import Player

class AIPlayer(Player):
    def __init__(self, name, symbol, use_alpha_beta=False):
        super().__init__(name, symbol)
        self.use_alpha_beta = use_alpha_beta
        self.total_thinking_time = 0
        self.node_count = 0

    def make_move(self, board):
        print(f"{self.name} is thinking...")
        time.sleep(1)
        best_move = self.find_best_move(board)
        return best_move

    def minimax(self, board, depth, is_maximizing):
        self.node_count += 1
        winner = board.check_winner()
        if winner == self.symbol:
            return 10 - depth
        elif winner is not None and winner != 'Tie':
            return depth - 10
        elif winner == 'Tie':
            return 0
        
        if is_maximizing:
            best_score = -math.inf
            for move in board.get_available_moves():
                board.make_move(move, self.symbol)
                score = self.minimax(board, depth + 1, False)
                board.undo_move(move)
                best_score = max(best_score, score)
            return best_score
        else:
            opponent_symbol = 'X' if self.symbol == 'O' else 'O'
            best_score = math.inf
            for move in board.get_available_moves():
                board.make_move(move, opponent_symbol)
                score = self.minimax(board, depth + 1, True)
                board.undo_move(move)
                best_score = min(best_score, score)
            return best_score

    def alpha_beta_pruning(self, board, depth, alpha, beta, is_maximizing):
        self.node_count += 1
        winner = board.check_winner()
        if winner == self.symbol:
            return 10 - depth
        elif winner is not None and winner != 'Tie':
            return depth - 10
        elif winner == 'Tie':
            return 0
        
        if is_maximizing:
            best_score = -math.inf
            for move in board.get_available_moves():
                board.make_move(move, self.symbol)
                score = self.alpha_beta_pruning(board, depth + 1, alpha, beta, False)
                board.undo_move(move)
                best_score = max(best_score, score)
                alpha = max(alpha, score)
                if beta <= alpha:
                    break
            return best_score
        else:
            opponent_symbol = 'X' if self.symbol == 'O' else 'O'
            best_score = math.inf
            for move in board.get_available_moves():
                board.make_move(move, opponent_symbol)
                score = self.alpha_beta_pruning(board, depth + 1, alpha, beta, True)
                board.undo_move(move)
                best_score = min(best_score, score)
                beta = min(beta, score)
                if beta <= alpha:
                    break
            return best_score
    
    def find_best_move(self, board):
        best_score = -math.inf
        best_move = None
        start_time = time.time()
        for move in board.get_available_moves():
            board.make_move(move, self.symbol)
            if self.use_alpha_beta:
                score = self.alpha_beta_pruning(board, 0, -math.inf, math.inf, False)
            else:
                score = self.minimax(board, 0, False)
            board.undo_move(move)
            if score > best_score:
                best_score = score
                best_move = move

        end_time = time.time()
        thinking_time = end_time - start_time
        self.total_thinking_time += thinking_time
        print(f"{self.total_thinking_time:.6f} seconds total to decide, {thinking_time:.6f} seconds thinking. ({self.node_count} nodes)")

        return best_move
    def evaluate_board(self, board):
        """Returns a heuristic score of the board state."""
        winner = board.check_winner()
        if winner == self.symbol:
            return 10
        elif winner and winner != 'Tie':
            return -10
        return 0  # Neutral score if no winner yet
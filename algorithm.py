import time
import math

from player import Player
from visualization import PruningVisualizer
class AIPlayer(Player):
    def __init__(self, name, symbol, use_alpha_beta=False, visualize_pruning=False):
        super().__init__(name, symbol)
        self.use_alpha_beta = use_alpha_beta
        self.visualize_pruning = visualize_pruning
        self.total_thinking_time = 0
        self.time_limit = 10  
        self.start_time = None
        self.best_found_move = None 
        if visualize_pruning:
            self.visualizer = PruningVisualizer()

    def make_move(self, board):
        print(f"{self.name} is thinking...")
        time.sleep(1)
        
        if self.visualize_pruning and self.use_alpha_beta:
            self.visualizer.reset()
            
        best_move = self.find_best_move(board)
        
        if self.visualize_pruning and self.use_alpha_beta:
            self.visualizer.visualize(f"{self.name} - Alpha-Beta Pruning Analysis")
            
        return best_move

    def minimax(self, board, depth, is_maximizing):
        if time.time() - self.start_time >= self.time_limit:
            return self.best_found_move 
        
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
                if score > best_score:
                    best_score = score
                    self.best_found_move = move
            return best_score
        else:
            opponent_symbol = 'X' if self.symbol == 'O' else 'O'
            best_score = math.inf
            for move in board.get_available_moves():
                board.make_move(move, opponent_symbol)
                score = self.minimax(board, depth + 1, True)
                board.undo_move(move)
                if score < best_score:
                    best_score = score
            return best_score

    def alpha_beta_pruning(self, board, depth, alpha, beta, is_maximizing, parent_node=None):
        if time.time() - self.start_time >= self.time_limit:
            return self.best_found_move 
        
        current_node = None
        if self.visualize_pruning:
            current_node = self.visualizer.add_node(
                board_state=str(board.grid), 
                depth=depth, 
                is_maximizing=is_maximizing, 
                alpha=alpha, 
                beta=beta, 
                parent=parent_node
            )
        
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
                score = self.alpha_beta_pruning(board, depth + 1, alpha, beta, False, current_node)
                board.undo_move(move)
                if score > best_score:
                    best_score = score
                    self.best_found_move = move
                alpha = max(alpha, score)
                if beta <= alpha:
                    break
            return best_score
        else:
            opponent_symbol = 'X' if self.symbol == 'O' else 'O'
            best_score = math.inf
            for move in board.get_available_moves():
                board.make_move(move, opponent_symbol)
                score = self.alpha_beta_pruning(board, depth + 1, alpha, beta, True, current_node)
                board.undo_move(move)
                if score < best_score:
                    best_score = score
                beta = min(beta, score)
                if beta <= alpha:
                    break
            return best_score
    
    def find_best_move(self, board):
        best_score = -math.inf
        self.best_found_move = None 
        
        root_node = None 
        
        if self.visualize_pruning and self.use_alpha_beta:
            root_node = self.visualizer.add_node(
                board_state="Root", 
                depth=0, 
                is_maximizing=True, 
                alpha=-math.inf, 
                beta=math.inf, 
                parent=None
            )
        
        self.start_time = time.time()
        for move in board.get_available_moves():
            if time.time() - self.start_time >= self.time_limit:
                break
            
            board.make_move(move, self.symbol)
            if self.use_alpha_beta:
                score = self.alpha_beta_pruning(board, 0, -math.inf, math.inf, False, root_node)
            else:
                score = self.minimax(board, 0, False)
            board.undo_move(move)
            
            if score > best_score:
                best_score = score
                self.best_found_move = move
        
        end_time = time.time()
        thinking_time = end_time - self.start_time
        self.total_thinking_time += thinking_time
        print(f"{self.total_thinking_time:.6f} seconds total to decide, {thinking_time:.6f} seconds thinking.")
        return self.best_found_move if self.best_found_move else board.get_available_moves()[0]  # Fallback move if needed

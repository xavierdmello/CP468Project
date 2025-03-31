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
        if visualize_pruning:
            self.visualizer = PruningVisualizer()

    def make_move(self, board):
        print(f"{self.name} is thinking...")
        time.sleep(1)
        
        if self.visualize_pruning and self.use_alpha_beta:
            # Reset visualizer for new move
            self.visualizer.reset()
            
        best_move = self.find_best_move(board)
        
        if self.visualize_pruning and self.use_alpha_beta:
            self.visualizer.visualize(f"{self.name} - Alpha-Beta Pruning Analysis")
            
        return best_move

    def minimax(self, board, depth, is_maximizing):
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

    def alpha_beta_pruning(self, board, depth, alpha, beta, is_maximizing, parent_node=None):
        # Create a node for the current state if visualizing
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
        
        # Terminal state evaluation
        winner = board.check_winner()
        if winner == self.symbol:
            value = 10 - depth
            if self.visualize_pruning:
                self.visualizer.set_node_value(current_node, value)
            return value
        elif winner is not None and winner != 'Tie':
            value = depth - 10
            if self.visualize_pruning:
                self.visualizer.set_node_value(current_node, value)
            return value
        elif winner == 'Tie':
            if self.visualize_pruning:
                self.visualizer.set_node_value(current_node, 0)
            return 0
        
        # Maximizing player
        if is_maximizing:
            best_score = -math.inf
            for move in board.get_available_moves():
                board.make_move(move, self.symbol)
                score = self.alpha_beta_pruning(board, depth + 1, alpha, beta, False, current_node)
                board.undo_move(move)
                best_score = max(best_score, score)
                alpha = max(alpha, score)
                
                # Pruning check
                if beta <= alpha:
                    # Mark remaining moves as pruned
                    if self.visualize_pruning:
                        # Mark future possible nodes as pruned
                        for future_move in board.get_available_moves():
                            if future_move != move:  # Skip the move we just evaluated
                                dummy_node = self.visualizer.add_node(
                                    board_state=f"Pruned at {depth+1}", 
                                    depth=depth+1, 
                                    is_maximizing=False, 
                                    alpha=alpha, 
                                    beta=beta, 
                                    parent=current_node
                                )
                                self.visualizer.mark_pruned(current_node, dummy_node)
                    break
            
            if self.visualize_pruning:
                self.visualizer.set_node_value(current_node, best_score)
            return best_score
        # Minimizing player
        else:
            opponent_symbol = 'X' if self.symbol == 'O' else 'O'
            best_score = math.inf
            for move in board.get_available_moves():
                board.make_move(move, opponent_symbol)
                score = self.alpha_beta_pruning(board, depth + 1, alpha, beta, True, current_node)
                board.undo_move(move)
                best_score = min(best_score, score)
                beta = min(beta, score)
                
                # Pruning check
                if beta <= alpha:
                    # Mark remaining moves as pruned
                    if self.visualize_pruning:
                        # Mark future possible nodes as pruned
                        for future_move in board.get_available_moves():
                            if future_move != move:  # Skip the move we just evaluated
                                dummy_node = self.visualizer.add_node(
                                    board_state=f"Pruned at {depth+1}", 
                                    depth=depth+1, 
                                    is_maximizing=True, 
                                    alpha=alpha, 
                                    beta=beta, 
                                    parent=current_node
                                )
                                self.visualizer.mark_pruned(current_node, dummy_node)
                    break
            
            if self.visualize_pruning:
                self.visualizer.set_node_value(current_node, best_score)
            return best_score
    
    def find_best_move(self, board):
        best_score = -math.inf
        best_move = None
        
        # Root node for visualization
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
        start_time = time.time()
        for move in board.get_available_moves():
            board.make_move(move, self.symbol)
            if self.use_alpha_beta:
                score = self.alpha_beta_pruning(board, 0, -math.inf, math.inf, False, root_node)
            else:
                score = self.minimax(board, 0, False)
            board.undo_move(move)
            if score > best_score:
                best_score = score
                best_move = move
                
        if self.visualize_pruning:
            self.visualizer.set_node_value(root_node, best_score)

        end_time = time.time()
        thinking_time = end_time - start_time
        self.total_thinking_time += thinking_time
        print(f"{self.total_thinking_time:.6f} seconds total to decide, {thinking_time:.6f} seconds thinking.")
        return best_move

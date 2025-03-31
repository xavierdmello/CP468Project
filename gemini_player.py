import os
import time
import google.generativeai as genai
from player import Player

# configure gemini api
apeye_key = "AIzaSyAe" + "9Wkot3b1CY" + "XB_TN5o3G_t-OtJew5un4"
genai.configure(api_key=apeye_key)

class GeminiPlayer(Player):
    def __init__(self, name, symbol, model_name="gemini-2.0-flash-lite"):
        super().__init__(name, symbol)
        self.model_name = model_name
        self.model = genai.GenerativeModel(model_name)
        self.total_thinking_time = 0
        
    def make_move(self, board):
        print(f"{self.name} is thinking...")
        start_time = time.time()
        time.sleep(1)
        
        # format the current board state for the prompt
        board_representation = self._format_board_for_prompt(board)
        available_moves = board.get_available_moves()
        opponent_symbol = 'X' if self.symbol == 'O' else 'O'
        
        # prompt for gemini
        prompt = f"""
        you are an expert tic-tac-toe player playing as '{self.symbol}'. your opponent is playing as '{opponent_symbol}'.
        
        current board state:
        {board_representation}
        
        available moves: {available_moves}
        
        follow these strategic priorities in order:
        1. if you can win immediately, make that move
        2. if opponent has two in a row/column/diagonal and can win next turn, block them immediately
        3. if center is available, take it
        4. if you can create a fork (two potential winning lines), make that move
        5. if opponent could create a fork next turn, block it
        6. take a corner if available
        7. take a side if available
        
        respond with ONLY the number of your chosen move (1-{board.size*board.size}). no explanations.
        """
        
        try:
            # generate response from gemini api
            response = self.model.generate_content(prompt)
            move_text = response.text.strip()
            print(f"Gemini response: {move_text}")
            # extract the move number from the response
            for word in move_text.split():
                if word.isdigit() and int(word) in available_moves:
                    self.time_calculation(start_time)
                    return int(word)
            
            # if no valid move found in response, choose first available move
            print(f"gemini api didn't return a valid move. using first available move.")
            self.time_calculation(start_time)
            return available_moves[0]
            
        except Exception as e:
            print(f"error communicating with gemini api: {e}")
            print("choosing first available move instead.")
            self.time_calculation(start_time)
            return available_moves[0]
    
    def _format_board_for_prompt(self, board):
        """Format the board as a string representation for the prompt"""
        formatted_board = ""
        for i, row in enumerate(board.grid):
            formatted_board += " | ".join(row) + "\n"
            if i < board.size - 1:
                formatted_board += "-" * (board.size * 3 + (board.size - 1) * 2) + "\n"
        return formatted_board

    def time_calculation(self, start_time):
        end_time = time.time()
        thinking_time = end_time - start_time
        self.total_thinking_time += thinking_time
        print(f"{self.total_thinking_time:.6f} seconds total to decide, {thinking_time:.6f} seconds thinking.")
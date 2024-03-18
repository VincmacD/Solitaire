import time

class Score:
    def __init__(self):
        self.score = 0
        self.moves_made = 0
        self.stockpile_refresh_count = 0
        self.start_time = time.time()
        self.last_penalty_time = time.time()
        self.consecutive_foundation_moves = 0  # Counter for consecutive moves to the foundation


    def move_to_tableau(self):
        self.score += 10
        print(f"Moved to Tableau (award 10 points): Score = {self.score}")

    def move_to_foundation(self):
        self.consecutive_foundation_moves += 1  # Increment the counter
        self.score += 10 * self.consecutive_foundation_moves  # Multiply the points by the consecutive counter
        print(f"Moved to Foundation (award {10 * self.consecutive_foundation_moves} points): Score = {self.score}")

    def move_from_foundation(self):
        self.score -= 10
        print(f"Moved from Foundation (reduce 10 points): Score = {self.score}")

    def reset_consecutive_moves(self):
        self.consecutive_foundation_moves = 0  # Reset the counter when a non-foundation move is made
        
    def refresh_stockpile(self):
        self.score -= 5
        print(f"Refreshed Stockpile (reduce 5 points): Score = {self.score}")

    # def apply_time_penalty(self):
    #     current_time = time.time()
    #     if current_time - self.last_penalty_time >= 10:
    #         self.score -= 1
    #         self.last_penalty_time = current_time
    #         print(f"Time Penalty (reduce 1 point): Score = {self.score}")

    # def apply_move_penalty(self):
    #     self.score -= 1
    #     print(f"Move made (reduce 1 point): Score = {self.score}")
    
    def increment_move_count(self):
        self.moves_made += 1
        print(f"Moves made: {self.moves_made}")  

    def display_score(self, screen):
        # Implement the display logic here
        pass

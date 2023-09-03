import json

class GameStats:
    """Track statistics for ALien Invasion."""

    def __init__(self, ai_game):
        """Inintialize stattistics."""
        self.settings = ai_game.settings
        self.reset_stats()

        # Start Alien Invasion in an active state.
        self.game_active = False

        # High score should never be reset.
        self.high_score = 0
        self.saved_high_score = 0
        # Filename for saved highscores
        self.filename = 'saved_scores.json'

        self.load_saved_highscore()

    def reset_stats(self):
        """Initialize statistics that can chagne during the game."""
        self.ships_left = self.settings.ship_limit
        self.score = 0
        self.level = 0
    
    def load_saved_highscore(self):
        with open(self.filename, 'r') as f:
            content = f.read()
            if len(content) != 0: 
                self.saved_high_score = int(content)
                self.high_score = self.saved_high_score       

    def save_new_highscore(self):
        if self.score > self.saved_high_score :
            with open(self.filename, 'w') as f:
                json.dump(self.score, f) 

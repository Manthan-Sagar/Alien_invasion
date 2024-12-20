class GameStats():
    #Track the stats of the alien invasion game 
    def __init__(self,ai_game):
        #start tracking stats
        self.settings = ai_game.settings
        self.reset_stats()
        # high score , should never be reset 
        self.high_score =0
        self.level = 1


    def reset_stats(self):
        #initalize statistics that can change during the game 
        self.ships_left = self.settings.ship_limit
        self.score = 0
    
    
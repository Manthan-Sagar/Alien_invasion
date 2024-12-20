class Settings():
    #this will store all the settings of alien invasion 
    def __init__(self):

        # initialize the game's static settings 
        #settings of the screen
        self.width = 1200
        self.height = 800
        self.bg_color = (128,128,128)

        #ship settings 
        
        self.ship_limit = 3


        #bullet settings
        
        self.bullet_width = 3
        self.bullet_height =15
        self.bullet_color = (60,60,60)

        #alien speed
        
        self.fleet_drop_speed = 10
        

     # initialize the game's dynamic setting
        self.speedUp_scale = 1.2

        # how quickly the alien point value increase 
        self.score_scale = 1.5
        self.initialize_dynamic_settings()

    def initialize_dynamic_settings(self):
        # initialize settings that change throught the game 
        self.bullet_speed = 4.0
        self.ship_speed = 3.5
        self.alien_speed = 5.0
        #fleet_direction of 1 represents right side and -1 represents left side 
        self.fleet_direction = 1
        # scoring settings 
        self.alien_points = 50

    def increase_speed(self):
        #increase speed and alien points 
        self.ship_speed *= self.speedUp_scale
        self.bullet_speed *= self.speedUp_scale
        self.alien_speed *= self.speedUp_scale

        self.alien_points = int(self.alien_points * self.score_scale)


    



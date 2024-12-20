import pygame
from pygame.sprite import Sprite
from pygame.sprite import Group
class ship(Sprite):
    # this class will manage ship
    def __init__(self,ai_game):
        # initilize the ship and set its starting position 
        super().__init__()
        self.screen = ai_game.screen
        self.screen_rect = ai_game.screen.get_rect()
        self.settings = ai_game.settings


        # load the image and get its rectangle
        self.image = pygame.image.load('images\Queen.bmp')
        self.rect = self.image.get_rect()

        # start the game at the bottom centre of the display 
        self.rect.midbottom = self.screen_rect.midbottom 

        #store a float value for ships exact horizontal position 
        self.x = float(self.rect.x)
        # movement flag : start the ship which is not moving 
        self.moving_right = False
        self.moving_left = False



    def update(self):
        #updates the movement of the flag 
        #update ships x value not rect 
        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.x += self.settings.ship_speed
        if self.moving_left and self.rect.left > self.screen_rect.left:
            self.x -=self.settings.ship_speed

        #update rect object from self.x
        self.rect.x = self.x


    def blitme(self):
        #draw the ship and its current location 
        self.screen.blit(self.image,self.rect) # blit is responsible to move the blocks from one part to another , and ofc its a method of pygame surface ( screen )

    def centre_ship(self):
        #centre the ship on the screen 
        self.rect.midbottom = self.screen_rect.midbottom
        self.x = float( self.rect.x)
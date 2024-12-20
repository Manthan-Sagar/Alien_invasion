import pygame.font

class Button():
    # A class to handle all the button work of the game 
    def __init__(self,ai_game,msg):
        self.screen = ai_game.screen
        self.screen_rect = ai_game.screen.get_rect()

        # set the dimensions and properties of the button 
        self.width,self.height = 200,50
        self.button_color = (0,255,0)
        self.font_color = (255,255,255)
        self.font = pygame.font.SysFont(None,48)


        # build the buttons rect and centre it 
        self.rect = pygame.Rect(0,0,self.width,self.height)
        self.rect.center = self.screen_rect.center


        # the button needs to be popped only once 
        self._prep_msg(msg)
    
    def _prep_msg(self,msg):
        # turn the message into rendered image and centre it to the bottom
        self.msg_img = self.font.render(msg , True, self.font_color, self.button_color)
        self.msg_img_rect = self.msg_img.get_rect()
        self.msg_img_rect.center = self.rect.center
    
    def draw_button(self):
        # draw blank button and then draw the message 
        self.screen.fill(self.button_color,self.rect)
        self.screen.blit(self.msg_img,self.msg_img_rect)




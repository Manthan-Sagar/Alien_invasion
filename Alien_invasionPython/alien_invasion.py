import sys 
import pygame
from time import sleep
from settings import Settings
from button import Button
from ship import ship
from game_stats import GameStats
from bullet import bullet
from alien import Alien
from scoreboard import ScoreBoard
class AlienInvasion:
    # This part will control all the assets and behaviour of the game 
    def __init__(self):
        pygame.init()
        self.settings = Settings()
        

        self.screen = pygame.display.set_mode((self.settings.width,self.settings.height))
        self.clock = pygame.time.Clock()
        self.bg_color=self.settings.bg_color# setting the background color in rgb 
        pygame.display.set_caption("Alien Invasion")

        # create an instance to store game statistics 
        # create an instance to show score 
        self.stats = GameStats(self)
        self.sb = ScoreBoard(self)
        self.ship = ship(self)
        self.bullets  = pygame.sprite.Group()
        self.aliens = pygame.sprite.Group()
        self._create_fleet()

        #start alien invasion in inactive state 
        self.game_active = False
        #make the play button 
        self.play_button =Button(self,"play")

    def RunGame(self):
        # Start the main loop of the game
        while True:
            self.check_events()

            if self.game_active:
             self.ship.update()
             self._update_aliens()
             self._update_bullets()
            self.update_screen()
            self.clock.tick(60)
            
               




    def check_events(self):
        #this part responds to the keyboard and mouse movement stuff
        # Watch for keyboard and mouse events
          for event in pygame.event.get():
            if event.type == pygame.QUIT:                      #it is just the way pygame works ngl  pygame.QUIT means that we have                                       
                sys.exit() 
            elif event.type == pygame.MOUSEBUTTONDOWN:
                 mouse_pos = pygame.mouse.get_pos()
                 self._check_play_button(mouse_pos)
            elif event.type == pygame.KEYDOWN:
                  self.check_event_KEYDOWN(event)
                
            elif event.type == pygame.KEYUP:
                 self.check_event_KEYUP(event)
               

    def check_event_KEYUP(self,event):
         if event.key == pygame.K_d:
                    self.ship.moving_right = False
         elif event.key == pygame.K_a:
                    self.ship.moving_left = False

    def check_event_KEYDOWN(self,event):
        if event.key == pygame.K_d:
                    #move the ship to right 
                   self.ship.moving_right = True
        elif event.key == pygame.K_a:
                    self.ship.moving_left = True

        elif event.key == pygame.K_SPACE:
              self._fire_bullet()
    
    def _fire_bullet(self):
          # create a bullet and add it to the group of bullets
        new_bullet = bullet(self)
        self.bullets.add(new_bullet)
    
    def _create_fleet(self):
          # create the fleet of alien 
          # create alien and keep adding them until there is no space left
          #spacing between them is one alien width /2 and height /2

          #make an alien 
          alien = Alien(self)
          alien_width,alien_height = alien.rect.size
          current_x , current_y = alien_width,alien_height

    def _create_fleet(self):
    # Create the fleet of aliens
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size
        current_x, current_y = alien_width, alien_height

        while current_y < (self.settings.height - 4 * alien_height):
            while current_x < (self.settings.width - 1.5 * alien_width):
                self._create_alien(current_x, current_y)
                current_x += 1.5 * alien_width
            
            # Finished a row, reset current_x and increment current_y
            current_x = alien_width
            current_y += 1.5 * alien_height

      
           
             

    def _create_alien(self,x_position,y_position):
        new_alien = Alien(self)
        new_alien.x = x_position              # still a little confusion in this part 
        new_alien.rect.x = x_position
        new_alien.rect.y = y_position
        self.aliens.add(new_alien)
    
    def _update_aliens(self):
         #check if the fleet is at the edge and then update positions 
         self._check_fleet_edge()
         self.aliens.update()

         #check for alien and ship collisions
         if pygame.sprite.spritecollideany(self.ship,self.aliens):
              print(f"Ship Hit!!!!!!!!!")
              self._ship_hit()
        
        # check for aliens hitting bottom 
         self._check_alien_bottom()

        #  print(f"Aliens Count: {len(self.aliens)}")


    def _check_fleet_edge(self):
         # respond appropriately if any of the alien has reached the edge 
         for alien in self.aliens.sprites():
              if alien.check_edges():
                   self._change_fleet_direction()
                   break
              
    def _change_fleet_direction(self):
         #drop the entire fleet and change the fleet direction 
        for alien in self.aliens.sprites():
              alien.rect.y += self.settings.fleet_drop_speed
        self.settings.fleet_direction *= -1

    def _check_play_button(self,mouse_pos):
         #start a new game if player clicks play 
         if self.play_button.rect.collidepoint(mouse_pos) and not self.game_active:
              # reset game statistics 
              self.settings.initialize_dynamic_settings()
              self.stats.reset_stats()
              self.sb.prep_score()
              self.sb.prep_level()
              self.sb.prep_ships()
              self.game_active = True
              #get rid of aliens and bullets
              self.bullets.empty()
              self.aliens.empty()

              # create a new fleet and centre the ship 
              self._create_fleet()
              self.ship.centre_ship()

              # hide the mouse cursor 
              pygame.mouse.set_visible(False)
         else:
              self.game_active = False
              pygame.mouse.set_visible(True)





        
    def update_screen(self):
        #updates the screen and flips it 
        self.screen.fill(self.bg_color) # redraw the screen during each loop 
        for bullet in self.bullets.sprites():
              bullet.draw_bullet()
        self.ship.blitme()

        self.aliens.draw(self.screen)
        #draw the scoreboard information 
        self.sb.show_score()
        #draw play button if the game is inactive
        if not self.game_active:
             self.play_button.draw_button()

        pygame.display.flip() # to make the created display drawn visible and shows the new changes which are made and removes the previous ones 

    def _update_bullets(self):
          # updates postion of the bullets and removes old bullets 
        self.bullets.update()
              #get rid of the bullets that have run off the screen 
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <=0:
              self.bullets.remove(bullet)
            # print(len(self.bullets))
        self._check_alien_bullet_collision()


        
    def _check_alien_bullet_collision(self):
 #check for any bullets that have hit the alien, if so then remove the alien 
        collisions = pygame.sprite.groupcollide(self.bullets,self.aliens,True,True)
        if collisions:
             for aliens in collisions.values():
                  self.stats.score += self.settings.alien_points * len(aliens)
             self.sb.prep_score()
             self.sb.check_high_score()

        if not self.aliens:
             #destroy the existing bullets and create a new fleet 
             self.bullets.empty()
             self._create_fleet()
             self.settings.increase_speed()

             # increase level 
             self.stats.level += 1
             self.sb.prep_level()

    

    def _ship_hit(self):
        # Respond to the ship being hit by an alien
        if self.stats.ships_left > 0:  
            self.stats.ships_left -= 1  # Decrement ships left
            self.sb.prep_ships()  # Update the scoreboard

            # Remove all remaining bullets and aliens
            self.bullets.empty()
            self.aliens.empty()

            # Create a new fleet and center the ship
            self._create_fleet()
            self.ship.centre_ship()

            # Pause for a moment
            sleep(1.5)
        else:
            self.game_active = False  # End the game
            pygame.mouse.set_visible(True)  # Show the mouse cursor
            
    
    def _check_alien_bottom(self):
    # Check if aliens have reached the bottom of the screen
     for alien in self.aliens.sprites():
        if alien.rect.bottom >= self.settings.height:
            self._ship_hit()  # Treat it as a ship hit
            break
        



if __name__ == '__main__':        #??
    # make the game instance and run the game
    ai = AlienInvasion()
    ai.RunGame()




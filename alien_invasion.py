import sys
import pygame
from Settings import Settings
from ship import Ship
import game_functions as gm_func
from pygame.sprite import Group
from alien import Alien
from game_stats import GameStats
from button import Button
from scoreboard import Scoreboard

def run_game():

    #Initializing the game and create a screen object
    pygame.init()
    game_settings=Settings()
    screen=pygame.display.set_mode((game_settings.screen_width,game_settings.screen_height))
    pygame.display.set_caption("Alien Invasion")

    # Make the Play button.
    play_button = Button(game_settings, screen, "Play")

    # Create an instance to store game statistics and create a scoreboard.
    stats = GameStats(game_settings)
    sb = Scoreboard(game_settings, screen, stats)

    #Making the ship
    ship=Ship(game_settings,screen)
    
    # Make a group to store bullets in.
    bullets = Group()

    # Make a group to store aliens in.
    aliens = Group()
    
    # Create the fleet of aliens.
    gm_func.create_fleet(game_settings, screen,ship, aliens)

    #Start the main loop of game
    while True:
        
        #Watching the keyboard and mouse events
        gm_func.check_events(game_settings,screen,stats,sb,play_button,ship,aliens,bullets)
        
        if stats.game_active==True:
            ship.update()
            gm_func.update_bullets(game_settings,screen,stats,sb,ship,aliens,bullets)
            bullets.update()
            gm_func.update_aliens(game_settings,stats,screen,sb,ship,aliens,bullets)
        
        gm_func.update_screen(game_settings,stats,sb,screen,ship,aliens,bullets,play_button)

run_game()
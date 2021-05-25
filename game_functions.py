import sys
import pygame
from Settings import Settings
from bullet import Bullet
from alien import Alien
from ship import Ship
from time import sleep

screen=pygame.display.set_mode((Settings().screen_width,Settings().screen_height))
ship=Ship(Settings,screen)


def check_events(Settings,screen,stats,sb,play_button,ship,aliens,bullets):
    """Respond to keypresses and mouse events."""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            check_keydown_events(event, Settings, screen, ship, bullets)
        elif event.type == pygame.KEYUP:
            check_keyup_events(event, ship)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            check_play_button(Settings,screen,stats,sb,play_button,ship,aliens,bullets,mouse_x, mouse_y)
            check_play_button(Settings, screen, stats, sb, play_button,ship, aliens, bullets, mouse_x, mouse_y)

def check_play_button(Settings,screen,stats,sb,play_button,ship,aliens,bullets,mouse_x,mouse_y):
    """Start a new game when the player clicks Play."""
    
    button_clicked = play_button.rect.collidepoint(mouse_x, mouse_y)
    if button_clicked and not stats.game_active:

        # Reset the game settings.
        Settings.initialize_dynamic_settings()
        
        # Hide the mouse cursor.
        pygame.mouse.set_visible(False)
        stats.game_active = True
        
        # Reset the game statistics.
        stats.reset_stats()
        stats.game_active = True

        # Reset the scoreboard images.
        sb.prep_score()
        sb.prep_high_score()
        sb.prep_level()
        sb.prep_ships()

        # Empty the list of aliens and bullets.
        aliens.empty()
        bullets.empty()
        
        # Create a new fleet and center the ship.
        create_fleet(Settings, screen, ship, aliens)
        ship.center_ship()

def check_keydown_events(event, Settings, screen, ship, bullets):
    """Respond to keypresses."""
    if event.key == pygame.K_RIGHT:
        ship.moving_right = True
    elif event.key == pygame.K_LEFT:
        ship.moving_left = True
    elif event.key == pygame.K_SPACE:
        fire_bullet(Settings, screen, ship, bullets)
    elif event.key == pygame.K_q:
        sys.exit()

def check_keyup_events(event, ship):
    """Respond to key releases."""
    if event.key == pygame.K_RIGHT:
        ship.moving_right = False
    elif event.key == pygame.K_LEFT:
        ship.moving_left = False

def update_screen(Settings,stats,sb,screen,ship,aliens,bullets,play_button):
    """Update images on the screen and flip to the new screen."""
    
    
    # Redraw the screen during each pass through the loop.
    screen.fill(Settings.bg_color)


    # Redraw all bullets behind ship and aliens.
    for bullet in bullets.sprites():
        bullet.draw_bullet()

    #Making the ship blit till the end of game
    ship.blit()
    aliens.draw(screen)

    # Draw the score information.
    sb.show_score()

    font = pygame.font.SysFont('comicsansms', 14)
    text = font.render('Press q to quit the game',True,(0,0,0))
    textRect = text.get_rect()
    textRect.center=(Settings.screen_width//2,10)
    screen.blit(text,textRect)

    # Draw the play button if the game is inactive.
    if not stats.game_active:
        play_button.draw_button()
    
    # Make the most recently drawn screen visible.
    pygame.display.flip()

def update_bullets(Settings, screen, stats, sb, ship, aliens, bullets):
    """Update position of bullets and get rid of old bullets."""
    
    # Update bullet positions.
    bullets.update()
    
    # Get rid of bullets that have disappeared.
    for bullet in bullets.copy():
        if bullet.rect.bottom <= 0:
            bullets.remove(bullet)
    
    # Check for any bullets that have hit aliens.
    # If so, get rid of the bullet and the alien.
    check_bullet_alien_collisions(Settings,screen,stats,sb,ship,aliens,bullets)


def check_bullet_alien_collisions(Settings, screen, stats, sb, ship, aliens, bullets):
    """Respond to bullet-alien collisions."""
    # Remove any bullets and aliens that have collided.
    collisions = pygame.sprite.groupcollide(bullets, aliens, True, True)
    
    if collisions:
        for aliens in collisions.values():
            stats.score += Settings.alien_points * len(aliens)
            sb.prep_score()
        check_high_score(stats, sb)

    if len(aliens) == 0:
        # If the entire fleet is destroyed, start a new level.
        bullets.empty()
        Settings.increase_speed()
        
        # Increase level.
        stats.level += 1
        sb.prep_level()
        
        create_fleet(Settings, screen, ship, aliens)

def fire_bullet(Settings, screen, ship, bullets):
    """Fire a bullet if limit not reached yet."""
    
    # Create a new bullet and add it to the bullets group.
    if len(bullets) < Settings.bullets_allowed:
        new_bullet = Bullet(Settings, screen, ship)
        bullets.add(new_bullet)

def get_number_aliens_x(Settings, alien_width):
    """Determine the number of aliens that fit in a row."""
    available_space_x = Settings.screen_width - 1.5 * alien_width
    number_aliens_x = int(available_space_x / (1.5 * alien_width))
    return number_aliens_x

def create_alien(Settings, screen, aliens, alien_number,row_number):
    """Create an alien and place it in the row."""
    alien = Alien(Settings, screen)
    alien_width = alien.rect.width
    alien.x = alien_width + 1.5 * alien_width * alien_number
    alien.rect.x = alien.x
    alien.rect.y = alien.rect.height +50+ 1.5 * alien.rect.height * row_number
    aliens.add(alien)

def create_fleet(Settings, screen,ship, aliens):
    """Create a full fleet of aliens."""
    
    # Create an alien and find the number of aliens in a row.
    alien = Alien(Settings, screen)
    number_aliens_x = get_number_aliens_x(Settings, alien.rect.width)
    number_rows = get_number_rows(Settings, ship.rect.height,alien.rect.height)
    
    # Create the fleet of aliens.
    for row_number in range(number_rows):
        for alien_number in range(number_aliens_x):
            create_alien(Settings, screen, aliens, alien_number,row_number)

def get_number_rows(Settings, ship_height, alien_height):
    """Determine the number of rows of aliens that fit on the screen."""
    available_space_y = (Settings.screen_height - (3 * alien_height) - ship_height)
    number_rows = int(available_space_y / (3 * alien_height))
    return number_rows

def update_aliens(Settings,stats,screen,sb,ship,aliens,bullets):
    """
    Check if the fleet is at an edge,
    and then update the postions of all aliens in the fleet.
    """
    check_fleet_edges(Settings, aliens)
    aliens.update()

    # Look for alien-ship collisions.
    if pygame.sprite.spritecollideany(ship, aliens):
        ship_hit(Settings, stats, screen, sb, ship, aliens, bullets)

    # Look for aliens hitting the bottom of the screen.
    check_aliens_bottom(Settings, stats, screen, sb, ship, aliens, bullets)

def check_fleet_edges(Settings, aliens):
    """Respond appropriately if any aliens have reached an edge."""
    for alien in aliens.sprites():
        if alien.check_edges():
            change_fleet_direction(Settings, aliens)
            break

def change_fleet_direction(Settings, aliens):
    """Drop the entire fleet and change the fleet's direction."""
    for alien in aliens.sprites():
        alien.rect.y += Settings.fleet_drop_speed
    Settings.fleet_direction *= -1

def ship_hit(Settings, stats, screen, sb, ship, aliens, bullets):
    """Respond to ship being hit by alien."""
    if stats.ships_left>0:
        # Decrement ships_left.
        stats.ships_left -= 1
        
        # Update scoreboard.
        sb.prep_ships()
        
        # Empty the list of aliens and bullets.
        aliens.empty()
        bullets.empty()
        
        # Create a new fleet and center the ship.
        create_fleet(Settings, screen, ship, aliens)
        ship.center_ship()
        
        # Pause.
        sleep(0.5)
    else:
        stats.game_active=False
        pygame.mouse.set_visible(True)

def check_aliens_bottom(Settings, stats, screen, sb, ship, aliens, bullets):
    """Check if any aliens have reached the bottom of the screen."""
    screen_rect = screen.get_rect()
    for alien in aliens.sprites():
        if alien.rect.bottom >= screen_rect.bottom:
            # Treat this the same as if the ship got hit.
            ship_hit(Settings, stats, screen, sb, ship, aliens, bullets)
            break

def check_high_score(stats, sb):
    """Check to see if there's a new high score."""
    if stats.score > stats.high_score:
        stats.high_score = stats.score
        sb.prep_high_score()
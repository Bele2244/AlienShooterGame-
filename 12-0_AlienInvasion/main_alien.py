import sys 
from time import sleep

import pygame

from settings import Settings
from game_stats import GameStats
from button import Button
from ship import Ship
from bullet import Bullet
from alien import Alien
from scoreboard import ScoreBoard


class AlienInvasion:
	"""Overall clas to manage game assets and behavior."""

	def __init__(self):
		# Initialize the game, and create game resources.
		pygame.init()
		self.settings = Settings()

		self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
		self.settings.screen_width = self.screen.get_rect().width
		self.settings.screen_height = self.screen.get_rect().height	
		pygame.display.set_caption("Alien Invasion")
		
		# Create an instance to store game statistics.
		# 	and create a scoreboard.
		self.stats = GameStats(self)
		self.sb = ScoreBoard(self)

		# Game sprites
		self.ship = Ship(self)
		self.bullets = pygame.sprite.Group()
		self.aliens = pygame.sprite.Group()

		# Make the buttons.
		self.easy_button = Button(self, "Easy", self.settings.easy_button_color, self.settings.text_color)
		self.hard_button = Button(self, "Hard", self.settings.hard_button_color, self.settings.text_color)
		self.play_button = Button(self, "Play", self.settings.play_button_color, self.settings.text_color)
		
		# Check if play button has been clicked
		self.clicked_play = False

	def run_game(self):
		# Start the main loop for the game.
		while True:
			self._check_events()

			if self.stats.game_active:
				self.ship.update()
				self._update_bullets()
				self._update_aliens()
			self._update_screen()

	def _check_events(self):
		"""Respond to keypresses and mouse events."""
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				self.stats.save_new_highscore()
				sys.exit()
			elif event.type == pygame.KEYDOWN:
				self._check_keydown_events(event)
			elif event.type == pygame.KEYUP:
				self._check_keyup_events(event)
			elif event.type == pygame.MOUSEBUTTONDOWN:
				mouse_pos = pygame.mouse.get_pos()
				self._check_clicked_button(mouse_pos)

	def _check_keydown_events(self, event):
		"""Respond to keypresses."""		
		if event.key == pygame.K_RIGHT:
			self.ship.moving_right = True
		elif event.key == pygame.K_LEFT:
			self.ship.moving_left = True
		elif event.key == pygame.K_q:
			self.stats.save_new_highscore()
			sys.exit()
		elif event.key == pygame.K_SPACE:
			self._fire_bullet()
		elif event.key == pygame.K_p:
			self._start_game()

	def _check_keyup_events(self, event):
		"""Respond to key releases."""
		if event.key == pygame.K_RIGHT:
			self.ship.moving_right = False
		elif event.key == pygame.K_LEFT:
			self.ship.moving_left = False

	def _start_game(self):
		# Reset the game stats.
		self.stats.reset_stats()
		self.stats.game_active = True
		# Hide the mosue cursor.
		pygame.mouse.set_visible(False)
		# Get rid of any remaining aliens and bullets.
		self.aliens.empty()
		self.bullets.empty()

	def _start_new_level(self):
		"""Create new sprites and increase game level"""
		# Destroy existing bullets and create new fleet.
		self.bullets.empty()
		self._create_fleet()
		self.settings.increase_speed()

		# Increase level.
		self.stats.level += 1
		self.sb.prep_level()

	def _fire_bullet(self):
		"""Create a new bullet and add it to the bullets group."""
		if len(self.bullets) < self.settings.bullets_allowed:
			new_bullet = Bullet(self)
			self.bullets.add(new_bullet)

	def _update_bullets(self):
		"""Update position of bullets and get rid of old bullets."""
		# Update bullet position
		self.bullets.update()

		# Get rid of bullets that have disappeared.
		for bullet in self.bullets.copy():
			if bullet.rect.bottom <= 0:
				self.bullets.remove(bullet)

		self._check_bullet_alien_collisions()

	def _create_alien(self, alien_number, row_number):
		"""Create an alien and place it in the row."""
		alien = Alien(self)
		alien_width, alien_height = alien.rect.size
		alien.x = alien_width + 2 * alien_width * alien_number
		alien.rect.x = alien.x
		alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number
		self.aliens.add(alien)

	def _create_fleet(self):
		"""Create the fleet of aliens."""
		# Create an alien and find the number of aliens in a row.
		# Spacing between each alien is equal to one alien widt.
		alien = Alien(self)
		alien_width, alien_height = alien.rect.size
		available_space_x = self.settings.screen_width - (2 * alien_width)
		number_aliens_x = available_space_x // (2 * alien_width)		
		
		# Detemine the number of rows od aliens that fit on the screen.
		ship_height = self.ship.rect.height
		available_space_y = (self.settings.screen_height - (3 * alien_height) - ship_height)
		number_rows = available_space_y // (2 * alien_height)

		# Create the full fleet of aliens.
		for row_number in range(number_rows):
			for alien_number in range(number_aliens_x):
				self._create_alien(alien_number, row_number)

	def _create_buttons(self):
		"""Create buttons and set their position, text and color."""
		# Draw the buttons if the game is inactive.
		if not self.stats.game_active and not self.clicked_play:
			self._create_play_button()
		else:
			self._create_easy_button()
			self._create_hard_button()

	def _create_play_button(self):
		# Settings for play button

		self.play_button.x = (self.settings.screen_width / 2) - 100
		self.play_button.y = (self.settings.screen_height / 2) - 50
		self.play_button._position_button()
		self.play_button.draw_button()

	def _create_easy_button(self):
		# Settings for easy button
		self.easy_button.x = (self.settings.screen_width / 2) - 100
		self.easy_button.y = (self.settings.screen_height / 2) - 50
		self.easy_button._position_button()
		self.easy_button.draw_button()

	def _create_hard_button(self):
		# Settings for hard button
		self.hard_button.x = (self.settings.screen_width / 2) - 100
		self.hard_button.y = (self.settings.screen_height / 2) + 50
		self.hard_button._position_button()
		self.hard_button.draw_button()

	def _check_clicked_button(self, mouse_pos):
		"""Start a new game when the player clicks Play."""
		self.button_clicked_play = self.play_button.rect.collidepoint(mouse_pos)
		self.button_clicked_easy = self.easy_button.rect. collidepoint(mouse_pos)
		self.button_clicked_hard = self.hard_button.rect.collidepoint(mouse_pos)
		

		if not self.clicked_play and not self.stats.game_active:
			self.clicked_play = True
			
			
		elif self.button_clicked_easy and self.clicked_play:
				self.settings.initialize_easy_settings()
				# Reset the game statistics.
				self.stats.reset_stats()
				self.sb.prep_score()
				self.sb.prep_level()
				self.sb.prep_ships()
				self._start_game()
			
		elif self.button_clicked_hard and self.clicked_play:
				self.settings.initialize_hard_settings()
				# Reset the game statistics.
				self.stats.reset_stats()
				self.sb.prep_score()
				self.sb.prep_level()
				self.sb.prep_ships()
				self._start_game()

	def _check_fleet_edges(self):
		"""Respond appropriately if any aliens have reached and edge."""
		for alien in self.aliens.sprites():
			if alien.check_edges():
				self._change_fleet_direction()
				break
	
	def _check_aliens_bottom(self):
		"""Check if any aliens have reached the bottom of the screen."""
		screen_rect = self.screen.get_rect()
		for alien in self.aliens.sprites():
			if alien.rect.bottom >= screen_rect.bottom:
				# Treat this the same as if the ship got hit.
				self._ship_hit()
				break

	def _check_bullet_alien_collisions(self):
		"""Respond to bullet-alien collisions."""
		# Remove any bullets and aliens that have collided.
		collisions = pygame.sprite.groupcollide(self.bullets, self.aliens, True, True)
		
		if collisions:
			for aliens in collisions.values():
				self.stats.score += self.settings.alien_points * len(aliens)
			self.sb.prep_score()
			self.sb.check_high_score()
		
		if not self.aliens:
			self._start_new_level()

	def _change_fleet_direction(self):
		"""Drop the entire fleet and chagne the fleet's direction."""
		for alien in self.aliens.sprites():
			alien.rect.y += self.settings.fleet_drop_speed
		self.settings.fleet_direction *= -1

	def _update_aliens(self):
		"""Update the positions of all aliens in the fleet."""
		self._check_fleet_edges()
		self.aliens.update()

		# Look for alien-ship collisions.
		if pygame.sprite.spritecollideany(self.ship, self.aliens):
			self._ship_hit()
		
		# Look for aliens hitting the bottom of the screen.
		self._check_aliens_bottom()

	def _ship_hit(self):
		"""Respond to the ship being hit by an alien."""
		if self.stats.ships_left > 0:
			# Decrement ships_left, and update scoreboard.
			self.stats.ships_left -= 1
			self.sb.prep_ships()

			# Get rid of any remaining aliens and bullets.
			self.aliens.empty()
			self.bullets.empty()

			# Create a new fleet and center the ship.
			self._create_fleet()
			self.ship.center_ship()

			# Pause.
			sleep(0.5)
		else:
			self.stats.game_active = False
			self.clicked_play = False
			pygame.mouse.set_visible(True)
			self.aliens.empty()
			self.bullets.empty()

	def _update_screen(self):
		"""Update images on the screen, and flip to the new screen."""
		self.screen.fill(self.settings.bg_color)
		self.ship.blitme()
		for bullet in self.bullets.sprites():
			bullet.draw_bullet()
		self.aliens.draw(self.screen)

		# Draw the score information.
		self.sb.show_score()

		# Draw the buttons if the game is inactive.
		if not self.stats.game_active:
			self._create_buttons()
	
		
		pygame.display.flip()
	
if __name__ == '__main__':
	# Make a game instance, and run the game
	ai = AlienInvasion()
	ai.run_game()
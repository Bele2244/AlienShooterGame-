class Settings:
    """ A class to store all settings for ALien Invasion. """

    def __init__(self):
        """ Initialize the game's settings."""
        # Screen Settings
        self.screen_width = 0
        self.screen_height = 0
        self.bg_color = (0,191,255)

        # Ship settings
        self.ship_speed = 1.5
        self.ship_limit = 3

        # Bullet settings
        self.bullet_speed = 3
        self.bullet_width = 3
        self.bullet_height = 15
        self.bullet_color = (60, 60, 60)
        self.bullets_allowed = 3

        # Button Settings
        self.text_color = [255, 255, 255]
        self.easy_button_color = [60, 179, 113]
        self.hard_button_color = [255, 0, 0]
        self.play_button_color = [0, 0, 0]

        # Alien settings
        self.alien_speed = 1.0
        self.fleet_drop_speed = 10
        
        # How quickly the game speeds up
        self.speedup_scale = 1.1

        # How quickly the alien point values increase
        self.score_scale = 1.5

        self.initialize_dynamic_settings()

    def initialize_dynamic_settings(self):
        """initialize settings that change throught the game."""
        self.ship_speed = 1.5
        self.bullet_speed = 3.0
        self.alien_speed = 1.0

        # Scoring
        self.alien_points = 50

        # Fleet direection of 1 represents rigth; -1 reperesents left.
        self.fleet_direction = 1
    
    def increase_speed(self):
        """Increase speed settings and alien point values."""
        self.ship_speed *= self.speedup_scale
        self.bullet_speed *= self.speedup_scale
        self.alien_speed *= self.speedup_scale

        self.alien_points = int(self.alien_points * self.score_scale)

    def initialize_easy_settings(self):
         # Ship settings
        self.ship_speed = 2.0

        # Bullet settings
        self.bullet_speed = 3.0
        self.bullet_width = 15
        self.bullet_height = 50
        self.bullets_allowed = 6

        # Alien settings
        self.alien_speed = 0.5
        self.fleet_drop_speed = 10

    def initialize_hard_settings(self):
            # Ship settings
        self.ship_speed = 1.0

        # Bullet settings
        self.bullet_speed = 1.0
        self.bullet_width = 5
        self.bullet_height = 10
        self.bullets_allowed = 3

        # Alien settings
        self.alien_speed = 1.0
        self.fleet_drop_speed = 15
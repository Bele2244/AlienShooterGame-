import pygame.font

class Button:
    
    def __init__(self, ss_game, msg, button_color, text_color):
        """Initialize button attributes."""
        self.screen = ss_game.screen
        self.screen_rect = self.screen.get_rect()
        

        # Set the dimensions and properties of the button.
        self.width, self.height = 200, 50
        self.button_color = button_color
        self.text_color = text_color
        self.font = pygame.font.SysFont("", 48)

        # Build the button's rect object and center it.
        self.rect = pygame.Rect(0, 0, self.width, self.height)
        self.button_image = self.rect
        
        self.x = float(self.rect.x)
        self.y = float(self.rect.y)


        # The button message needs to be prepped only once.
        self._prep_msg(msg, button_color, text_color)    

    def _prep_msg(self, msg, button_color, text_color):
        self.button_color = button_color
        self.text_color = text_color
        """Turn msg into a rendered image and center text on the button."""
        self.msg_image = self.font.render(msg, True, self.text_color, self.button_color)
        self.msg_image_rect = self.msg_image.get_rect()
        
    def _position_button(self):
        # Position the button on the screen 
        self.rect.x = int(self.x)
        self.rect.y = int(self.y)

        # Position the text on the blank button center
        self.msg_image_rect.center = self.button_image.center

    def draw_button(self):
        # Draw blank button and then draw message.
        self.screen.fill(self.button_color, self.rect)
        self.screen.blit(self.msg_image, self.msg_image_rect)
    
import pygame
from Label import Label

class Button(Label):
    def __init__(self, text, font, color, function, top_left=None, center=None, bg_color=None, anti_aliasing=True, size=None):
        super().__init__(text, font, color, top_left=top_left, center=center, bg_color=bg_color, anti_aliasing=anti_aliasing, size=size)
        self.function = function
        # Adjust size if specified
        #if size:
        #    self.rect.size = size
        #    self.image = pygame.Surface(self.rect.size)
        #    if self.bg_color:
        #        self.image.fill(self.bg_color)
        #    # Center the text image on the button
        #    self.text_image = self.font.render(self.text, self.anti_aliasing, self.color, self.bg_color)
        #    text_rect = self.text_image.get_rect(center=self.rect.center)
        #    self.image.blit(self.text_image, text_rect)


    def check_hit(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            # Check if the mouse click is within the button's rect
            if self.rect.collidepoint(event.pos):
                return True
        return False
                

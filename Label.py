import pygame

class Label:
    def __init__(self, text, font, color, top_left=None, center=None, bg_color=None, anti_aliasing=True, size=None):
        self.text = text
        self.font = font
        self.color = color
        self.bg_color = bg_color
        self.anti_aliasing = anti_aliasing
        self.size = size
        self.text_image = self.font.render(self.text, self.anti_aliasing, self.color, self.bg_color)

        # If a background color is specified, create a background surface
        if self.bg_color:
            if size:
                self.image = pygame.Surface(self.size)
            else:
                self.image = pygame.Surface(self.text_image.get_size())
            self.image.fill(self.bg_color)
            # Blit the text onto the background
            text_rect = self.text_image.get_rect(center=self.image.get_rect().center)
            self.image.blit(self.text_image, text_rect)
        else:
            self.image = self.text_image

        self.rect = self.image.get_rect()

        # Position the label based on the provided parameters
        if top_left:
            self.rect.topleft = top_left
        elif center:
            self.rect.center = center
        else:
            # Default position if no position is provided
            self.rect.topleft = (0, 0)

    def draw(self, screen):
        screen.blit(self.image, self.rect)

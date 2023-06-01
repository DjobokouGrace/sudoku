import pygame
import time

# Initialize Pygame
pygame.init()

# Define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

# Set up the display
width, height = 800, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Button and Time Example")

# Define the Button class
class Button:
    def __init__(self, x, y, width, height, color, hover_color, text, text_color):
        self.rect = pygame.Rect(x, y, width, height)
        self.color = color
        self.hover_color = hover_color
        self.text = text
        self.text_color = text_color

    def draw(self, surface):
        pygame.draw.rect(surface, self.color, self.rect)
        font = pygame.font.Font(None, 24)
        text = font.render(self.text, True, self.text_color)
        text_rect = text.get_rect(center=self.rect.center)
        surface.blit(text, text_rect)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.rect.collidepoint(event.pos):
                print("Button Clicked!")

# Create a Button instance
button = Button(300, 250, 200, 50, BLACK, RED, "Click Me", WHITE)

# Game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        button.handle_event(event)

    # Clear the screen
    screen.fill(WHITE)

    # Draw the button
    button.draw(screen)

    # Display the current time
    current_time = time.strftime("%H:%M:%S", time.localtime())
    font = pygame.font.Font(None, 36)
    text = font.render(current_time, True, BLACK)
    text_rect = text.get_rect(center=(width // 2, height // 2))
    screen.blit(text, text_rect)

    # Update the display
    pygame.display.flip()

# Quit the game
pygame.quit()

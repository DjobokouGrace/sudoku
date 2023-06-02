import pygame

class Button:
    def __init__(self, text, x, y, width, height, color):
        self.text = text
        self.rect = pygame.Rect(x, y, width, height)
        self.color = color

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)
        font = pygame.font.Font(None, 36)
        text = font.render(self.text, True, (0, 0, 0))
        screen.blit(text, self.rect)

    def is_clicked(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                return True
        return False


class MainWindow:
    def __init__(self):
        self.screen_size = (800, 600)
        self.screen = pygame.display.set_mode(self.screen_size)
        self.button = Button('Ouvrir', 350, 275, 100, 50, (200, 200, 200))
        self.message = "Hello, second window!"
        self.running = True

    def run(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                if self.button.is_clicked(event):
                    self.open_new_window()

            self.screen.fill((0, 0, 0))
            self.button.draw(self.screen)
            pygame.display.flip()

    def open_new_window(self):
        new_screen = SecondWindow(self.message)
        new_screen.run()


class SecondWindow:
    def __init__(self, message):
        self.screen_size = (800, 600)
        self.screen = pygame.display.set_mode(self.screen_size)
        self.message = message
        self.running = True

    def run(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

            self.screen.fill((0, 0, 0))
            font = pygame.font.Font(None, 36)
            text = font.render(self.message, True, (255, 255, 255))
            self.screen.blit(text, (20, 20))
            pygame.display.flip()


if __name__ == '__main__':
    pygame.init()
    window = MainWindow()
    window.run()
    pygame.quit()

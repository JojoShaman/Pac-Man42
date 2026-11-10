from .states.state import State
from .states.playing import Playing
import pygame

class App:
    def __init__(self) -> None:
        self.state: State = Playing()

    def run(self) -> None:
        pygame.init()
        screen = pygame.display.set_mode((1280, 720))
        running = True
        
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
            self.state.render(screen)
            pygame.display.flip()
        pygame.quit()


import sys

import pygame

class Window:
    def __init__(self, simulation):
        self.simulation = simulation
        # Ustawienia okna
        self.WINDOW_WIDTH = 800
        self.WINDOW_HEIGHT = 600
        self.FPS = 50

        # Ustawienia mapy
        self.GRID_SIZE = 5
        self.GRID_WIDTH = 50 ##WINDOW_WIDTH // GRID_SIZE
        self.GRID_HEIGHT = 50 ##WINDOW_HEIGHT // GRID_SIZE

        # Ustawienia obiektów
        self.OBJECT_SIZE = 10

        # Inicjalizacja Pygame
        pygame.init()
        self.screen = pygame.display.set_mode((self.WINDOW_WIDTH, self.WINDOW_HEIGHT))
        self.clock = pygame.time.Clock()

    # Funkcja rysująca kratki na mapie
    def draw_grid(self):
        for x in range(0, self.WINDOW_WIDTH, self.GRID_SIZE):
            pygame.draw.line(self.screen, (255, 255, 255), (x, 0), (x, self.WINDOW_HEIGHT))
        for y in range(0, self.WINDOW_HEIGHT, self.GRID_SIZE):
            pygame.draw.line(self.screen, (255, 255, 255), (0, y), (self.WINDOW_WIDTH, y))

    def loop(self):
        # Główna pętla gry
        while True:
            # Obsługa zdarzeń
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            # Wypełnienie tła
            self.screen.fill((0, 0, 0))

            # Rysowanie kratki na mapie
            self.draw_grid()

            # Rysowanie obiektów
            # object_positions = [(1, 0), (0, 15), (50, 0)] # Przykładowe pozycje obiektów
            # for pos in object_positions:
            #     rect = pygame.Rect(pos[0], pos[1], self.OBJECT_SIZE, self.OBJECT_SIZE)
            #     pygame.draw.rect(self.screen, (255, 0, 0), rect)

            for car in self.simulation.map.cars:
                rect = pygame.Rect(car.position.x , car.position.y , self.OBJECT_SIZE, self.OBJECT_SIZE)
                pygame.draw.rect(self.screen, (255, 0, 0), rect)



            # Aktualizacja ekranu
            pygame.display.update()
            self.clock.tick(self.FPS)

            self.simulation.update()

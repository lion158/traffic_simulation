import sys

import pygame


class Window:
    def __init__(self, engine):
        self.engine = engine
        # Ustawienia okna
        self.WINDOW_WIDTH = 700
        self.WINDOW_HEIGHT = 700
        self.FPS = 60
        self.tick = 0
        self.update_time = 0

        # Ustawienia mapy
        self.GRID_SIZE = 7
        self.GRID_WIDTH = 100  ##WINDOW_WIDTH // GRID_SIZE
        self.GRID_HEIGHT = 100  ##WINDOW_HEIGHT // GRID_SIZE

        # Ustawienia obiektów
        self.OBJECT_SIZE = 5

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

    def draw_cars(self, delta_time):
        cars = self.engine.simulation.cars

        for car in cars:
            self.engine.update(delta_time, car)
            rect = pygame.Rect(car.position.x, car.position.y, self.OBJECT_SIZE, self.OBJECT_SIZE)  ##*10
            pygame.draw.rect(self.screen, car.color, rect)

    def draw_roads(self):

        for i in range(self.engine.map.N):
            for j in range(self.engine.map.N):
                if self.engine.map.road_map[i][j] == -99:
                    rect = pygame.Rect(j * 7, i * 7, 7, 7)  ##*10
                    pygame.draw.rect(self.screen, (200, 200, 200), rect)
                if self.engine.map.lights_map[i][j] == 1:
                    rect = pygame.Rect(j * 7, i * 7, 7, 7)  ##*10
                    pygame.draw.rect(self.screen, (0, 255, 0), rect)
                if self.engine.map.lights_map[i][j] == 0:
                    rect = pygame.Rect(j * 7, i * 7, 7, 7)  ##*10
                    pygame.draw.rect(self.screen, (255, 0, 0), rect)
                if self.engine.map.car_v_map[i][j] >= 0:
                    rect = pygame.Rect(j * 7, i * 7, 7, 7)  ##*10
                    pygame.draw.rect(self.screen, (0, 0, 255), rect)

    def loop(self):
        # Główna pętla gry
        clock = pygame.time.Clock()
        while True:
            self.tick += 1
            # Obsługa zdarzeń
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            delta_time = clock.tick(self.FPS) / 1000.0

            # Wypełnienie tła
            self.screen.fill((0, 0, 0))

            # Rysowanie kratki na mapie
            # self.draw_grid()
            # Rysowanie obiektów
            # object_positions = [(1, 0), (0, 15), (50, 0)] # Przykładowe pozycje obiektów
            # for pos in object_positions:
            #     rect = pygame.Rect(pos[0], pos[1], self.OBJECT_SIZE, self.OBJECT_SIZE)
            #     pygame.draw.rect(self.screen, (255, 0, 0), rect)

            self.draw_roads()

            self.draw_cars(float(1 / 60))

            # Aktualizacja ekranu
            pygame.display.update()
            self.clock.tick(self.FPS)
            self.update_time += delta_time

            if self.tick % 60 == 0:
                self.engine.loop(self.update_time)
                self.update_time = 0
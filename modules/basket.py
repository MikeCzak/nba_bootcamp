import pygame
from pygame.sprite import Sprite


class Basket:
    def __init__(self, position: tuple, width: int, height: int):
        super().__init__()
        self.width = width
        self.height = height
        self.bg = Sprite()
        self.fg = Sprite()
        self.bg.layer = -1
        self.fg.layer = 1
        self.fg.image = pygame.Surface((width, height//2))
        self.fg.image.set_colorkey((0, 0, 0))
        self.bg.image = pygame.Surface((width, height//2))
        self.bg.image.set_colorkey((0, 0, 0))
        self.bg.rect = self.bg.image.get_rect()
        self.fg.rect = self.fg.image.get_rect()
        self.fg.rect.y = height // 2
        pygame.draw.ellipse(self.bg.image, (10, 10, 10), (0, 0, width, height), 15)
        pygame.draw.ellipse(self.fg.image, (10, 10, 10), (0, -height//2, width, height), 15)
        self.bg.rect.x, self.bg.rect.y = position
        self.fg.rect.x = position[0]
        self.fg.rect.y = position[1] + height // 2

        self.left_edge = Sprite()
        self.left_edge.image = pygame.Surface((15, 15))
        self.left_edge.radius = 7.5
        pygame.draw.circle(self.left_edge.image, (255, 0, 0), (self.left_edge.radius, self.left_edge.radius), self.left_edge.radius)
        self.left_edge.rect = self.left_edge.image.get_rect()
        self.left_edge.rect.y = self.fg.rect.y - self.left_edge.radius

        self.right_edge = Sprite()
        self.right_edge.image = pygame.Surface((15, 15))
        self.right_edge.radius = 7.5
        pygame.draw.circle(self.right_edge.image, (255, 0, 0), (self.right_edge.radius, self.right_edge.radius), self.right_edge.radius)
        self.right_edge.rect = self.right_edge.image.get_rect()
        self.right_edge.rect.y = self.fg.rect.y - self.right_edge.radius



    def update(self) -> None:
        self.bg.rect.x = self.fg.rect.x = pygame.mouse.get_pos()[0] - self.width//2
        self.left_edge.rect.x = pygame.mouse.get_pos()[0] - self.width//2
        self.right_edge.rect.x = pygame.mouse.get_pos()[0] + self.width // 2 - self.right_edge.rect.width





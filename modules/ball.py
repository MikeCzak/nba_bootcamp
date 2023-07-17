import pygame
from pygame.sprite import Sprite
from os.path import join as path_join


class Ball(Sprite):
    gravity = 0.4

    def __init__(self, position: tuple, ball_size: int):
        super().__init__()
        self.image = pygame.Surface((ball_size, ball_size))
        self.radius = ball_size//2
        pygame.draw.circle(self.image, (254, 113, 27), (self.radius, self.radius), self.radius)
        self.image.set_colorkey((0, 0, 0))
        self.image = pygame.image.load(path_join("img", "ball.png")).convert_alpha()
        self.image = pygame.transform.scale(self.image, (ball_size, ball_size))
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = position

        self.vel_y = 0
        self.vel_x = 0
        self.max_vel_x = 10
        self.caught = False
        self.mask = pygame.mask.from_surface(self.image)

    def update(self) -> None:
        self.vel_y += self.gravity
        self.rect.x += self.vel_x
        self.rect.y += self.vel_y

    def eval(self):
        if self.caught:
            pass


import pygame
from pygame.sprite import DirtySprite
import csv


class Scoreboard(DirtySprite):
    def __init__(self, player_name: str, width: int):
        super().__init__()
        self.width = width
        self.height = 80
        self.image = pygame.Surface((self.width, self.height))
        self.image.fill((200, 200, 200))
        self.rect = self.image.get_rect()
        self.x = self.y = 0
        self.score = 0
        self.player_name = player_name
        self.font = pygame.font.Font("font/pixel.ttf", 100)
        self.score_text = self.font.render(f"{self.player_name.upper()}: {self.score}", True, (0, 0, 0))
        self.image.blit(self.score_text, (self.width - self.score_text.get_width()-50, self.height//2 - self.score_text.get_height()//2))
        self.dirty = 1
        self.layer = 2

    def score_point(self):
        self.score += 1
        self.image.fill((200, 200, 200))
        self.score_text = self.font.render(f"{self.player_name.upper()}: {self.score}", True, (0, 0, 0))
        self.image.blit(self.score_text, (self.width - self.score_text.get_width() - 50, self.height // 2 - self.score_text.get_height() // 2))
        self.dirty = 1

    def reset(self):
        self.score = 0
        self.image.fill((200, 200, 200))
        self.score_text = self.font.render(f"{self.player_name.upper()}: {self.score}", True, (0, 0, 0))
        self.image.blit(self.score_text, (
        self.width - self.score_text.get_width() - 50, self.height // 2 - self.score_text.get_height() // 2))
        self.dirty = 1

    def draw(self, screen):
        screen.blit(self.image, (0, 0, self.width, self.height))

    def load_highscore(self):
        with open("highscore.txt", "r") as highscore:
            scores = highscore.read().splitlines()
        return scores

    def save_score(self, name, score):
        scores = self.load_highscore()
        if int(scores[-1].split(",")[1]) < score:
            scores.append(f"{name.upper()},{score}")
            scores_sorted = sorted(scores, key=lambda item: int(item.split(",")[1]), reverse=True)
            if len(scores_sorted) > 10:
                scores_sorted.pop()
            with open("highscore.txt", "w") as highscore:
                highscore.writelines(line + "\n" for line in scores_sorted)


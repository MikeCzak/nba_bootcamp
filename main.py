import math
import random
from pygame.math import Vector2 as V
import pygame
from pygame.locals import *
from modules.basket import Basket
from modules.ball import Ball
# from net import Net
from modules.scoreboard import Scoreboard
from os.path import join as path_join

pygame.init()
screen = pygame.display.set_mode((0, 0), DOUBLEBUF + FULLSCREEN)
SCREEN_WIDTH = screen.get_width()
SCREEN_HEIGHT = screen.get_height()
BASKET_WIDTH = 200
BASKET_HEIGHT = 60
BALL_SIZE = math.floor(BASKET_WIDTH / 1.5)
BOTTOM_CENTER = (SCREEN_WIDTH // 2, SCREEN_HEIGHT - 3 * BASKET_HEIGHT)

clock = pygame.time.Clock()
FPS = 60
pygame.mouse.set_visible(False)

player_name = ""
basket = Basket(BOTTOM_CENTER, BASKET_WIDTH, BASKET_HEIGHT)
sprites = pygame.sprite.LayeredUpdates()
basket.bg.add(sprites)
basket.fg.add(sprites)
ball = Ball((SCREEN_WIDTH//2, 0), BALL_SIZE)
ball.add(sprites)

# net = Net(sprites, basket)

sound_start = pygame.mixer.Sound(path_join("sound", "game_start.ogg"))
sound_ball = pygame.mixer.Sound(path_join("sound", "ball.wav"))
sound_score = pygame.mixer.Sound(path_join("sound", "score.mp3"))
music = pygame.mixer.music


new_game = True
name = ""
cursor = "|"

# ================ START SCREEN ==================

start_screen = True
music.load(path_join("sound", "start_screen.wav"))
music.play(-1)
title = pygame.image.load(path_join("img", "title.png")).convert_alpha()
ratio = title.get_height()/title.get_width()
title = pygame.transform.scale(title, (SCREEN_WIDTH//2, SCREEN_WIDTH//2*ratio))
big = pygame.font.Font("font/pixel.ttf", 50)
press_start = big.render("PRESS RETURN", True, (255, 255, 255))
instructions = big.render("Use your mouse to catch the basket ball!", True, (255, 255, 255))
i = -1
j = -1

while start_screen:
    screen.fill((0, 0, 0))
    for event in pygame.event.get():
        if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
            quit()
        if event.type == KEYDOWN:
            if event.key == K_RETURN:
                sound_start.play()
                i = 0
                j = 0

    screen.blit(title, (SCREEN_WIDTH/2 - title.get_width()/2, SCREEN_HEIGHT/2 - title.get_height()/2 - 200))
    screen.blit(press_start, (SCREEN_WIDTH/2 - press_start.get_width()/2, SCREEN_HEIGHT/2 - press_start.get_height()/2 + 100))
    screen.blit(instructions, (
    SCREEN_WIDTH / 2 - instructions.get_width() / 2, SCREEN_HEIGHT / 2 - instructions.get_height() / 2 + 250))

    if i >= 0:
        i += 1
        j += 1
    if i == 100:
        start_screen = False

    if 0 < j < 5:
        press_start.set_alpha(0)
    if 5 < j < 10:
        press_start.set_alpha(255)
    if j == 10:
        j = 0


    clock.tick(FPS)
    pygame.display.flip()


# ================ ENTER NAME ==================

while new_game:
    for event in pygame.event.get():
        if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
            quit()
        if event.type == KEYDOWN:
            if event.key == K_BACKSPACE:
                name = name[:-1]
            elif event.key == K_RETURN:
                new_game = False
                sound_start.play()
            else:
                name += event.unicode

    screen.fill((0, 0, 0))
    big = pygame.font.Font("font/pixel.ttf", 50)
    msg_text = big.render(f" Please enter your name: ", True, (200, 30, 30), (255, 255, 255, 90))
    name_text = big.render(f" {name}{cursor}", True, (255, 255, 255))
    screen.blit(msg_text,
                (SCREEN_WIDTH // 2 - msg_text.get_width() // 2,
                 SCREEN_HEIGHT // 2 - msg_text.get_height() // 2 - 50))
    screen.blit(name_text,
                (SCREEN_WIDTH // 2 - name_text.get_width() // 2,
                 SCREEN_HEIGHT // 2 - name_text.get_height() // 2 + 50))
    clock.tick(FPS)
    pygame.display.flip()

music.load(path_join("sound", "stadium.ogg"))
music.play(-1, 0, 3000)

# ================ COUNTDOWN ==================

scoreboard = Scoreboard(name, SCREEN_WIDTH)
countdown = True
now = pygame.time.get_ticks()
big = pygame.font.Font("font/pixel.ttf", 200)
counter_scale = 1
a = 255
three_text = big.render(f" 3 ", True, (200, 30, 30))
two_text = big.render(f" 2 ", True, (200, 30, 30))
one_text = big.render(f" 1 ", True, (200, 30, 30))

while countdown:
    for event in pygame.event.get():
        if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
            quit()
    duration = pygame.time.get_ticks()
    counter = pygame.transform.rotozoom(three_text, 0, counter_scale)
    if duration - now > 1000:
        counter = pygame.transform.rotozoom(two_text, 0, counter_scale)
    if duration - now > 2000:
        counter = pygame.transform.rotozoom(one_text, 0, counter_scale)
    if duration - now > 3000:
        countdown = False
    counter.set_alpha(a)
    if 1000 < duration - now < 1020 or 2000 < duration - now < 2020:
        counter_scale = 1
        a = 255

    counter_scale += 0.05
    a -= 5

    screen.fill((0, 0, 0))
    screen.blit(counter,
                (SCREEN_WIDTH // 2 - counter.get_width() // 2,
                 SCREEN_HEIGHT // 2 - counter.get_height() // 2 - 50))
    clock.tick(FPS)
    pygame.display.flip()

# ================ GAME LOOP ==================

running = True
background = pygame.image.load(path_join("img", "court.png")).convert()
ratio = background.get_height()/background.get_width()
background = pygame.transform.scale(background, (SCREEN_WIDTH, SCREEN_WIDTH * ratio))
screen.blit(background, (0, 0))
pygame.display.flip()

while running:
    for event in pygame.event.get():
        if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
            quit()

    screen.fill((0, 0, 0))
    screen.blit(background, (0, 0))

    vector = 0
    if pygame.sprite.collide_circle(ball, basket.left_edge):
        sound_ball.play()
        vector = V(basket.left_edge.rect.center) - V(ball.rect.center)
        ball.rect.x -= ball.vel_x
        ball.vel_x += -vector[0]*0.15
        if ball.rect.centery < basket.left_edge.rect.centery:
            ball.rect.y -= ball.vel_y
            ball.vel_y = ball.vel_y * -0.6

    if pygame.sprite.collide_circle(ball, basket.right_edge):
        sound_ball.play()
        vector = V(basket.right_edge.rect.center) - V(ball.rect.center)
        ball.rect.x -= ball.vel_x
        ball.vel_x += -vector[0]*0.15
        if ball.rect.centery < basket.right_edge.rect.centery:
            ball.rect.y -= ball.vel_y
            ball.vel_y = ball.vel_y * -0.6

    if ball.vel_x > ball.max_vel_x:
        ball.vel_x = ball.max_vel_x

    if ball.vel_x < -ball.max_vel_x:
        ball.vel_x = -ball.max_vel_x

    if ball.rect.collidepoint((basket.fg.rect.centerx, basket.fg.rect.centery+50)):
        if not ball.caught:
            sound_score.play()
        ball.caught = True

    if ball.rect.y > SCREEN_HEIGHT:
        if ball.caught:
            scoreboard.score_point()
            ball.gravity += 0.05
            ball.caught = False

        else:
            game_over = True
            ball.gravity = 0.4
            pause = pygame.time.get_ticks()
            score = scoreboard.score
            scoreboard.save_score(name, score)
            scoreboard.reset()
            big = pygame.font.Font("font/pixel.ttf", 300)
            small = pygame.font.Font("font/pixel.ttf", 100)
            name_text = big.render(f"  GAME OVER  ", True, (240, 0, 0), (255, 255, 255, 90))
            score_text = small.render(f"  YOUR SCORE: {score}  ", True, (0, 0, 0))
            while game_over:
                for event in pygame.event.get():
                    if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                        quit()
                screen.blit(name_text, (SCREEN_WIDTH // 2 - name_text.get_width() // 2, SCREEN_HEIGHT // 2 - name_text.get_height() // 2 - 100))
                screen.blit(score_text, (
                    SCREEN_WIDTH // 2 - score_text.get_width() // 2, SCREEN_HEIGHT // 2 - score_text.get_height() // 2 + 150))
                pygame.display.flip()
                duration = pygame.time.get_ticks()
                if duration - pause >= 1500:
                    game_over = False
                    show_highscore = True

                clock.tick(FPS)

            screen.fill((0, 0, 0))
            pause = pygame.time.get_ticks()
            music.load(path_join("sound", "start_screen.wav"))
            music.play(-1)
            while show_highscore:
                for event in pygame.event.get():
                    if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                        quit()
                    if event.type == KEYDOWN:
                        if event.key == K_RETURN:
                            show_highscore = False
                            music.load(path_join("sound", "stadium.ogg"))
                            music.play(-1, 0, 1000)
                            screen.fill((0, 0, 0))
                            screen.blit(background, (0, 0))
                            pygame.display.flip()
                highscore = scoreboard.load_highscore()
                top_10 = []
                smaller = pygame.font.Font("font/pixel.ttf", 80)
                for line in highscore:
                    s = smaller.render(f"{line.split(',')[0]:<10}{line.split(',')[1]:>10}", True, (255, 255, 255))
                    top_10.append(s)
                play_again = smaller.render(f"Press ESC to quit or RETURN to play again!", True, (170, 0, 0))

                for rank in range(len(top_10)):
                    screen.blit(top_10[rank], (SCREEN_WIDTH//2 - top_10[rank].get_width()//2, 100 + rank*50))
                if show_highscore:
                    screen.blit(play_again, (SCREEN_WIDTH // 2 - play_again.get_width() // 2, SCREEN_HEIGHT - 100))
                pygame.display.flip()


        ball.rect.y = -BALL_SIZE
        ball.vel_y = 0
        ball.vel_x = 0
        ball.rect.x = random.randint(0, SCREEN_WIDTH - BALL_SIZE)

    if ball.rect.x <= 0 or ball.rect.x >= SCREEN_WIDTH - ball.rect.width:
        ball.vel_x *= -1
        sound_ball.play()

    basket.update()
    ball.update()
    # net.update(basket)

    updated = sprites.draw(screen)

    scoreboard.draw(screen)
    debug_font = pygame.font.SysFont("Futura", 20)
    name_text = debug_font.render(f"", True, (0, 255, 0))
    screen.blit(name_text, (10, SCREEN_HEIGHT - 150))
    pygame.display.update(updated)
    clock.tick(FPS)

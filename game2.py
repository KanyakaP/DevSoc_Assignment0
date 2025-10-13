import pygame
import sys
import random

pygame.init()
pygame.mixer.init()
pygame.mixer.music.load("PongMusic.mp3")
pygame.mixer.music.play(-1)
pygame.mixer.music.set_volume(0.3)
pygame.display.set_caption('Pong')

global ball_speed_x
global ball_speed_y
global player_score
global opponent_score
global score_time

player_speed = 0
opponent_speed = 0
game_active = True
player_score = 0
opponent_score = 0
screen_width = 1200
screen_height = 800
light_grey = (200, 200, 200)
score_time = True


screen = pygame.display.set_mode((screen_width, screen_height))
fireball_img = pygame.image.load("fireball.png").convert_alpha()
fireball_img = pygame.transform.scale(fireball_img, (80, 80))
ball = pygame.Rect((screen_width-30)/2, (screen_height - 30)/2, 30, 30)
player = pygame.Rect((screen_width - 20), (screen_height - 140)/2, 10, 140)
opponent = pygame.Rect(10, (screen_height - 140)/2, 10, 140)
bg_color = pygame.Color('grey12')
game_font = pygame.font.Font("freesansbold.ttf", 32)
hit_sound = pygame.mixer.Sound("HitPong.mp3")
over_sound = pygame.mixer.Sound("GameOver.mp3")
clock = pygame.time.Clock()
ball_speed_x = 5 * random.choice((1, -1))
ball_speed_y = 5 * random.choice((1, -1))
font = pygame.font.Font("freesansbold.ttf", 74)
game_over_text = font.render(
    "Game Over! Press R to Restart", True, (255, 255, 255))
wave_img = pygame.image.load("waves.png").convert_alpha()
wave_side = pygame.transform.rotate(wave_img, 270)
edge_thickness = 120
wave_side = pygame.transform.scale(wave_side, (edge_thickness, screen_height))


def ball_animation():
    global ball_speed_x, ball_speed_y, game_active, opponent_score, player_score, score_time
    ball.x = ball.x + ball_speed_x
    ball.y = ball.y + ball_speed_y
    if ball.top <= 0 or ball.bottom >= screen_height:
        if ball_speed_y > 0:
            ball_speed_y = -5
        else:
            ball_speed_y = 5
        hit_sound.play()
    if ball.left <= 0:
        game_active = False
        player_score += 1
        ball_restart()
        over_sound.play()
        score_time = pygame.time.get_ticks()

    if ball.right >= screen_width:
        game_active = False
        opponent_score += 1
        ball_restart()
        over_sound.play()
        score_time = pygame.time.get_ticks()

    if ball.colliderect(player):
        if ball_speed_x > 0:
            ball_speed_x = -5
        else:
            ball_speed_x = 5
        ball.right = player.left
        hit_sound.play()

    if ball.colliderect(opponent):
        if ball_speed_x > 0:
            ball_speed_x = -5
        else:
            ball_speed_x = 5
        ball.left = opponent.right
        hit_sound.play()


def player_animation():
    player.y += player_speed
    if player.top <= 0:
        player.top = 0
    if player.bottom >= screen_height:
        player.bottom = screen_height


def opponent_animation():
    opponent.y += opponent_speed
    if opponent.top <= 0:
        opponent.top = 0
    if opponent.bottom >= screen_height:
        opponent.bottom = screen_height


def ball_restart():
    global ball_speed_y, ball_speed_x, score_time
    current_time = pygame.time.get_ticks()
    ball.center = (screen_width / 2, screen_height / 2)
    if score_time is None:
        return
    countdown = 4000 - (current_time - score_time)
    if countdown > 2000:
        number = game_font.render("3", False, light_grey)

    elif countdown > 1000:
        number = game_font.render("2", False, light_grey)

    elif countdown > 0:
        number = game_font.render("1", False, light_grey)

    else:
        ball_speed_y = 5 * random.choice((1, -1))
        ball_speed_x = 5 * random.choice((1, -1))
        score_time = None
        return

    screen.fill(bg_color)
    screen.blit(number, (screen_width/2,
                         screen_height/2))
    pygame.display.flip()
    pygame.time.delay(700)


while True:
    keys = pygame.key.get_pressed()
    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN and not game_active:
            if event.key == pygame.K_r:
                game_active = True
                if score_time is not None:
                    ball_restart()
                player.y = (screen_height-140)/2
                opponent.y = (screen_height-140)/2

    if game_active:
        if score_time is None:
            ball_animation()
            screen.fill(bg_color)
            pygame.draw.aaline(screen, light_grey, (screen_width/2,
                                                    0), (screen_width/2, screen_height))
            player_text = game_font.render(
                f"{player_score}", False, light_grey)
            screen.blit(player_text, (640, 400))
            opponent_text = game_font.render(
                f"{opponent_score}", False, light_grey)
            screen.blit(opponent_text, (550, 400))
            screen.blit(wave_side, (0, 0))
            screen.blit(pygame.transform.flip(wave_side, True, False),
                        (screen_width - edge_thickness, 0))
            pygame.draw.rect(screen, light_grey, player)
            pygame.draw.rect(screen, light_grey, opponent)
            screen.blit(fireball_img, (ball.x, ball.y))
        else:
            ball_restart()
        player_speed = 0
        opponent_speed = 0
        if keys[pygame.K_DOWN]:
            player_speed += 5
        if keys[pygame.K_UP]:
            player_speed -= 5
        if keys[pygame.K_s]:
            opponent_speed += 5
        if keys[pygame.K_w]:
            opponent_speed -= 5

        player_animation()
        opponent_animation()

    if not game_active:
        screen.fill(bg_color)
        screen.blit(game_over_text, (screen_width/2 - game_over_text.get_width()/2,
                                     screen_height/2 - game_over_text.get_height()/2))

    pygame.display.flip()
    clock.tick(60)

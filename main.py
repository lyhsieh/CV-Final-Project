import pygame
from pygame import mixer
from fighter import Fighter
import os
import natsort

mixer.init()
pygame.init()

# create game window
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 600

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Fighting game")

# set framerate
clock = pygame.time.Clock()
FPS = 60

# define colours
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)

# define game variables
intro_count = 3
last_count_update = pygame.time.get_ticks()
score = [0, 0]  # player scores. [P1, P2]
round_over = False
ROUND_OVER_COOLDOWN = 2000

# # define fighter variables
# WARRIOR_SIZE = 144
# WARRIOR_SCALE = 2
# WARRIOR_OFFSET = [72, 56]
# WARRIOR_DATA = [WARRIOR_SIZE, WARRIOR_SCALE, WARRIOR_OFFSET]
# WIZARD_SIZE = 144
# WIZARD_SCALE = 2
# WIZARD_OFFSET = [112, 56]
# WIZARD_DATA = [WIZARD_SIZE, WIZARD_SCALE, WIZARD_OFFSET]

# define fighter variables
P1_SIZE_X = 172 #153     # the step for cropping the sprite
P1_SIZE_Y = 165 #147
P1_SCALE = 2.5
P1_OFFSET = [60, 56]
P1_DATA = [P1_SIZE_X, P1_SIZE_Y, P1_SCALE, P1_OFFSET]
P2_SIZE_X = 172
P2_SIZE_Y = 165
P2_SCALE = 2.5
P2_OFFSET = [60, 56]
P2_DATA = [P2_SIZE_X, P2_SIZE_Y, P2_SCALE, P2_OFFSET]

# define fighter's head variables (i.e., style image)
HEAD1_SIZE = 180
HEAD1_SCALE = 1
HEAD1_OFFSET = [10, 125]
HEAD1_DATA = [HEAD1_SIZE, HEAD1_SCALE, HEAD1_OFFSET]
HEAD2_SIZE = 210
HEAD2_SCALE = 1
HEAD2_OFFSET = [52, 150]    # x bigger -> left
HEAD2_DATA = [HEAD2_SIZE, HEAD2_SCALE, HEAD2_OFFSET]

# load music and sounds
# pygame.mixer.music.load("assets/audio/music.mp3")
# pygame.mixer.music.set_volume(0.5)
# pygame.mixer.music.play(-1, 0.0, 5000)
sword_fx = pygame.mixer.Sound("assets/audio/sword.wav")
sword_fx.set_volume(0.1)
magic_fx = pygame.mixer.Sound("assets/audio/magic.wav")
magic_fx.set_volume(0.1)

# load background image
bg_image = pygame.image.load("assets/images/background/background.jpeg").convert_alpha()
alpha = 128
bg_image.fill((255, 255, 255, alpha), None, pygame.BLEND_RGBA_MULT)

# load spritesheets
# warrior_sheet = pygame.image.load("assets/images/stickman/test_frame.jpg").convert_alpha()
warrior_sheet = pygame.image.load("assets/images/stickman/blue_rmbg.png").convert_alpha()
wizard_sheet = pygame.image.load("assets/images/stickman/red_rmbg.png").convert_alpha()

# styleGAN player 1 image path list
style_path = "assets/images/stylegan/inference_result_rmbg1"
player_s1 = []  # player sytle 1 img list
for root, dirs, files in os.walk(os.path.abspath(style_path)):
    for file in files:
        player_s1.append(os.path.join(root, file))  # abs path
player_s1 = natsort.natsorted(player_s1)    # natural sorting a list

# styleGAN player 2
style_path = "assets/images/stylegan/inference_result_rmbg2"
player_s2 = []
for root, dirs, files in os.walk(os.path.abspath(style_path)):
    for file in files:
        player_s2.append(os.path.join(root, file))
player_s2 = natsort.natsorted(player_s2)

# load vicory image
victory_img = pygame.image.load("assets/images/icons/victory.png").convert_alpha()

# define number of steps in each animation
WARRIOR_ANIMATION_STEPS = [1, 1, 1, 5, 5, 5, 1, 5]
WIZARD_ANIMATION_STEPS = [1, 1, 1, 5, 5, 5, 1, 5]

# define font
count_font = pygame.font.Font("assets/fonts/turok.ttf", 80)
score_font = pygame.font.Font("assets/fonts/turok.ttf", 30)

# function for drawing text
def draw_text(text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    screen.blit(img, (x, y))

# function for drawing background
def draw_bg():
    scaled_bg = pygame.transform.scale(bg_image, (SCREEN_WIDTH, SCREEN_HEIGHT))
    screen.blit(scaled_bg, (0, 0))

# function for drawing fighter health bars
def draw_health_bar(health, x, y):
    ratio = health / 100
    pygame.draw.rect(screen, WHITE, (x - 2, y - 2, 404, 34))
    pygame.draw.rect(screen, RED, (x, y, 400, 30))
    pygame.draw.rect(screen, GREEN, (x, y, 400 * ratio, 30))


# create two instances of fighters
fighter_1 = Fighter(1, 200, 310, False, P1_DATA,
                    warrior_sheet, WARRIOR_ANIMATION_STEPS, sword_fx, player_s1, HEAD1_DATA)
fighter_2 = Fighter(2, 700, 310, True, P2_DATA,
                    wizard_sheet, WIZARD_ANIMATION_STEPS, magic_fx, player_s2, HEAD2_DATA)

# game loop
run = True
while run:

    P1_action = [False, False, False, False, False]  # bool list
    P2_action = [False, False, False, False, False]

    # ⬆︎ human pose estimation ⬆︎

    clock.tick(FPS)

    # draw background
    draw_bg()

    # show player stats
    draw_health_bar(fighter_1.health, 20, 20)
    draw_health_bar(fighter_2.health, 580, 20)
    draw_text("P1: " + str(score[0]), score_font, RED, 20, 60)
    draw_text("P2: " + str(score[1]), score_font, RED, 580, 60)

    # update countdown
    if intro_count <= 0:
        # move fighters
        fighter_1.move(SCREEN_WIDTH, SCREEN_HEIGHT,
                       screen, fighter_2, round_over, P1_action)
        fighter_2.move(SCREEN_WIDTH, SCREEN_HEIGHT,
                       screen, fighter_1, round_over, P2_action)
    else:
        # display count timer
        draw_text(str(intro_count), count_font, RED,
                  SCREEN_WIDTH / 2, SCREEN_HEIGHT / 3)
        # update count timer
        if (pygame.time.get_ticks() - last_count_update) >= 1000:
            intro_count -= 1
            last_count_update = pygame.time.get_ticks()

    # update fighters
    fighter_1.update()
    fighter_2.update()

    # draw fighters
    fighter_1.draw(screen)
    fighter_2.draw(screen)

    # check for player defeat
    if round_over == False:
        if fighter_1.alive == False:
            score[1] += 1
            round_over = True
            round_over_time = pygame.time.get_ticks()
        elif fighter_2.alive == False:
            score[0] += 1
            round_over = True
            round_over_time = pygame.time.get_ticks()
    else:
        # display victory image
        screen.blit(victory_img, (360, 150))
        if pygame.time.get_ticks() - round_over_time > ROUND_OVER_COOLDOWN:
            round_over = False
            intro_count = 3
            fighter_1 = Fighter(1, 200, 310, False, P1_DATA,
                                warrior_sheet, WARRIOR_ANIMATION_STEPS, sword_fx, player_s1, HEAD1_DATA)
            fighter_2 = Fighter(2, 700, 310, True, P2_DATA,
                                wizard_sheet, WIZARD_ANIMATION_STEPS, magic_fx, player_s2, HEAD2_DATA)

    # event handler
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    # update display
    pygame.display.update()

# exit pygame
pygame.quit()

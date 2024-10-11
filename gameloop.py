import pygame
from pygame import mixer
from fighter import Fighter

mixer.init()
pygame.init()

# create game window
SCREEN_WIDTH = 1500
SCREEN_HEIGHT = 750

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("gameloop")

# set framerate
clock = pygame.time.Clock()
FPS = 60

# define colours
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)

# define game variables
intro_count = 3
last_count_update = pygame.time.get_ticks()
score = [0, 0]  # player scores. [P1, P2]
round_over = False
ROUND_OVER_COOLDOWN = 2000

# load music and sounds
pygame.mixer.music.load("assets/audio/music.mp3")
pygame.mixer.music.set_volume(0.5)
pygame.mixer.music.play(-1, 0.0, 5000)
sword_fx = pygame.mixer.Sound("assets/audio/sword.wav")
sword_fx.set_volume(0.5)
magic_fx = pygame.mixer.Sound("assets/audio/magic.wav")
magic_fx.set_volume(0.75)

# load background image
bg_image = pygame.image.load("assets/images/background/back-ground.gif").convert_alpha()

# load spritesheets
warrior_sheet = pygame.image.load("assets/images/warrior/Sprites/warrior.png").convert_alpha()
evil_wizard_sheet = pygame.image.load("assets/images/wizard/Sprites/wizard.png")
wizard_sheet = pygame.image.load("assets/images/Wizard2/big_wizard.png").convert_alpha()
hero_sheet = pygame.image.load("assets/images/Hero/hero.png").convert_alpha()

# define warrior variables
WARRIOR_XFRAMES = 10
WARRIOR_YFRAMES = 7
WARRIOR_SIZE = (warrior_sheet.get_width() / WARRIOR_XFRAMES, warrior_sheet.get_height() / WARRIOR_YFRAMES)
WARRIOR_SCALE = 4
WARRIOR_OFFSET = [72, 56]
WARRIOR_DATA = [WARRIOR_SIZE[0], WARRIOR_SIZE[1], WARRIOR_SCALE, WARRIOR_OFFSET]

# define evil wizard variables
EVIL_WIZARD_XFRAMES = 8
EVIL_WIZARD_YFRAMES = 7
EVIL_WIZARD_SIZE = (wizard_sheet.get_width() / EVIL_WIZARD_XFRAMES, wizard_sheet.get_height() / EVIL_WIZARD_YFRAMES)
EVIL_WIZARD_SCALE = 3
EVIL_WIZARD_OFFSET = [112, 107]
EVIL_WIZARD_DATA = [250, 250, EVIL_WIZARD_SCALE, EVIL_WIZARD_OFFSET]  # made sizes(250,250) fixed because it kept moving

# define wizard variables
WIZARD_XFRAMES = 8
WIZARD_YFRAMES = 7
WIZARD_SIZE = (wizard_sheet.get_width() / WIZARD_XFRAMES, wizard_sheet.get_height() / WIZARD_YFRAMES)
WIZARD_SCALE = 2
WIZARD_OFFSET = [112, 52]
WIZARD_DATA = [WIZARD_SIZE[0], WIZARD_SIZE[1], WIZARD_SCALE, WIZARD_OFFSET]

# define hero variables
HERO_XFRAMES = 11
HERO_YFRAMES = 7
HERO_SIZE = (hero_sheet.get_width() / HERO_XFRAMES, hero_sheet.get_height() / HERO_YFRAMES)
HERO_SCALE = 3
HERO_OFFSET = [72, 22]
HERO_DATA = [HERO_SIZE[0], HERO_SIZE[1], HERO_SCALE, HERO_OFFSET]

# load victory image
victory_img = pygame.image.load("assets/images/icons/victory.png").convert_alpha()

# define number of steps in each animation
WARRIOR_ANIMATION_STEPS = [10, 8, 1, 7, 7, 3, 7]
EVIL_WIZARD_ANIMATION_STEPS = [8, 8, 1, 8, 8, 3, 7]
HERO_ANIMATION_STEPS = [10, 8, 1, 7, 6, 3, 10]
WIZARD_ANIMATION_STEPS = [6, 8, 1, 8, 8, 4, 7]

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
    pygame.draw.rect(screen, YELLOW, (x, y, 400 * ratio, 30))


# create two instances of fighters
fighter_1 = Fighter(1, 200, 310, False, EVIL_WIZARD_DATA, evil_wizard_sheet, EVIL_WIZARD_ANIMATION_STEPS, magic_fx)
fighter_2 = Fighter(2, SCREEN_WIDTH - 300, 310, True, WIZARD_DATA, wizard_sheet, WIZARD_ANIMATION_STEPS, magic_fx)

# game loop
def gameloop():

    global fighter_1, fighter_2, round_over, intro_count, last_count_update, round_over_time
    run = True
    while run:

        clock.tick(FPS)

        # draw background
        draw_bg()

        # show player stats
        draw_health_bar(fighter_1.health, 20, 20)
        draw_health_bar(fighter_2.health, SCREEN_WIDTH - 424, 20)
        draw_text("P1: " + str(score[0]), score_font, RED, 20, 60)
        draw_text("P2: " + str(score[1]), score_font, RED, SCREEN_WIDTH - 424, 60)

        # update countdown
        if intro_count <= 0:
            # move fighters
            fighter_1.move(SCREEN_WIDTH, SCREEN_HEIGHT, screen, fighter_2, round_over)
            fighter_2.move(SCREEN_WIDTH, SCREEN_HEIGHT, screen, fighter_1, round_over)
        else:
            # display count timer
            draw_text(str(intro_count), count_font, RED, SCREEN_WIDTH / 2, SCREEN_HEIGHT / 3)
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

        # check for player defeatF
        if not round_over:
            if not fighter_1.alive:
                score[1] += 1
                round_over = True
                round_over_time = pygame.time.get_ticks()
            elif not fighter_2.alive:
                score[0] += 1
                round_over = True
                round_over_time = pygame.time.get_ticks()
        else:
            # display victory image
            screen.blit(victory_img, (SCREEN_WIDTH / 2 - victory_img.get_width() / 2, SCREEN_HEIGHT / 3))
            if pygame.time.get_ticks() - round_over_time > ROUND_OVER_COOLDOWN:
                round_over = False
                intro_count = 3
                fighter_1 = Fighter(1, 200, 310, False, HERO_DATA, hero_sheet, HERO_ANIMATION_STEPS, sword_fx)
                fighter_2 = Fighter(2, SCREEN_WIDTH - 300, 310, True, WIZARD_DATA, wizard_sheet, WIZARD_ANIMATION_STEPS,
                                    magic_fx)

        # event handler
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        # update display
        pygame.display.update()

    # exit pygame
    pygame.quit()

gameloop()
import pygame
import sys
import random

"""Functions Needed For the Game"""


# This function will draw floor on the screen
def draw_floor():
    screen.blit(floor_surface, (floor_x_pos, 690))
    screen.blit(floor_surface, (floor_x_pos + 432, 690))


# This function will create pipe and we will store it to the list
def create_pipe():
    pipe_height_diff = [175, 185, 195, 205, 215]
    pipe_height = [300, 350, 400, 450, 500]
    random_pipe_position = random.choice(pipe_height)
    bottom_pipe = pipe_surface.get_rect(midtop=(525, random_pipe_position))
    top_pipe = pipe_surface.get_rect(midbottom=(525, random_pipe_position - random.choice(pipe_height_diff)))
    return bottom_pipe, top_pipe


# This function will move the pipes in the display
def move_pipes(pipes):
    for pipe in pipes:
        pipe.centerx -= 3
    visible_pipes = [pipe for pipe in pipes if pipe.right > - 50]
    return visible_pipes


# This function will draw pipes in the display
def draw_pipes(pipes):
    for pipe in pipes:
        if 0 <= score <= 10:
            if pipe.bottom >= 768:
                screen.blit(pipe_surface, pipe)
            else:
                flip_pipe = pygame.transform.flip(pipe_surface, False, True)
                screen.blit(flip_pipe, pipe)
        elif 11 <= score <= 20:
            if pipe.bottom >= 768:
                screen.blit(pipe_surface_night, pipe)
            else:
                flip_pipe = pygame.transform.flip(pipe_surface_night, False, True)
                screen.blit(flip_pipe, pipe)
        elif 21 <= score <= 30:
            if pipe.bottom >= 768:
                screen.blit(pipe_surface, pipe)
            else:
                flip_pipe = pygame.transform.flip(pipe_surface, False, True)
                screen.blit(flip_pipe, pipe)
        else:
            if pipe.bottom >= 768:
                screen.blit(pipe_surface_night, pipe)
            else:
                flip_pipe = pygame.transform.flip(pipe_surface_night, False, True)
                screen.blit(flip_pipe, pipe)


# This Function rotates the bird
def rotate_bird(bird):
    new_bird = pygame.transform.rotozoom(bird, -bird_movement * 3, 1)
    return new_bird


# This Function makes the animation for bird's flapping
def bird_animation():
    new_bird = bird_frames[bird_index]
    new_bird_rect = new_bird.get_rect(center=(100, bird_rect.centery))
    return new_bird, new_bird_rect


# This function displays the score
def score_display(game_state):
    if game_state == 'main_game':
        score_surface = game_font.render(str(int(score)), True, (255, 255, 255))
        score_rect = score_surface.get_rect(center=(216, 50))
        screen.blit(score_surface, score_rect)
    if game_state == 'game_over':
        score_surface = game_font.render(f'Your Score: {int(score)}', True, (255, 255, 255))
        score_rect = score_surface.get_rect(center=(216, 100))
        screen.blit(score_surface, score_rect)

        high_score_surface = game_font.render(f'High Score: {int(high_score)}', True, (255, 255, 255))
        high_score_rect = high_score_surface.get_rect(center=(216, 600))
        screen.blit(high_score_surface, high_score_rect)

        press_surface = game_font.render("PRESS 'P' TO PLAY AGAIN", True, (255, 100, 100))
        press_rect = press_surface.get_rect(center=(216, 500))
        screen.blit(press_surface, press_rect)


# This function updates the score on the screen
def update_score(score, high_score):
    if score > high_score:
        high_score = score
        with open("high_score.txt", "w") as file:
            file.write(str(high_score))
    return high_score


# This function validates a score count
def pipe_score_check():
    global score, can_score
    if pipe_list:
        for pipe in pipe_list:
            if 0 < pipe.centerx < 5 and can_score:
                score += 1
                score_sound.play()
                can_score = False
            if pipe.centerx < 0:
                can_score = True


# This function checks for collision
def check_collision(pipes):
    global can_score
    for pipe in pipes:
        if bird_rect.colliderect(pipe):
            death_sound.play()
            can_score = True
            return False
    if bird_rect.top <= -75 or bird_rect.bottom >= 675:
        can_score = True
        death_sound.play()
        return False
    return True


"""Game Variables & Initialization"""
# Initializing Pygame and Audio Mixer For Pygame
pygame.mixer.pre_init()
pygame.init()
pygame.display.set_caption("Pygame-FlappyBird")

# Creating a screen (height, width)
screen = pygame.display.set_mode((432, 768))

# Clock is used to set Frames Per Second
clock = pygame.time.Clock()

# Selecting font for score
game_font = pygame.font.Font('04B_19.TTF', 30)

# Game Variables
gravity = 0.15
bird_movement = 0
game_active = False
is_start_phase = True
score = 0
can_score = True
with open("high_score.txt", "r") as file:
    high_score = int(file.readline())

# Creating surfaces for pygame

# Game start phase
start_surface = pygame.transform.scale(pygame.image.load("assets/message.png").convert_alpha(), (276, 401))
start_rect = start_surface.get_rect(center=(216, 384))
start_text = game_font.render("PRESS SPACE TO START", True, (255, 100, 100))
start_text_rect = start_text.get_rect(center=(216, 625))

# Background Surface
bg_surface = pygame.transform.scale(pygame.image.load("assets/background-day.png").convert(), (432, 768))
bg_surface_night = pygame.transform.scale(pygame.image.load("assets/background-night.png").convert(), (432, 768))

# Floor Surface
floor_surface = pygame.transform.scale(pygame.image.load("assets/base.png").convert(), (504, 168))
floor_x_pos = 0

# Creating Pipes in the game
pipe_surface = pygame.transform.scale(pygame.image.load("assets/pipe-green.png").convert(), (78, 480))
pipe_surface_night = pygame.transform.scale(pygame.image.load("assets/pipe-red.png").convert(), (78, 480))
pipe_list = []  # This is used to store random positioned pipes, vars will get from a function
SPAWNPIPE = pygame.USEREVENT
pygame.time.set_timer(SPAWNPIPE, 1200)  # this will activate spawnpipe event after 1200 milisecconds

# Creating Bird Surface
bird_downflap = pygame.transform.scale(pygame.image.load("assets/bluebird-downflap.png").convert_alpha(), (51, 36))
bird_midflap = pygame.transform.scale(pygame.image.load("assets/bluebird-midflap.png").convert_alpha(), (51, 36))
bird_upflap = pygame.transform.scale(pygame.image.load("assets/bluebird-upflap.png").convert_alpha(), (51, 36))
bird_frames = [bird_downflap, bird_midflap, bird_upflap]
bird_index = 0
bird_surface = bird_frames[bird_index]
bird_rect = bird_surface.get_rect(center=(75, 384))

BIRDFLAP = pygame.USEREVENT + 1
pygame.time.set_timer(BIRDFLAP, 200)

# Creating Game Over Screen
game_over_surface = pygame.transform.scale(pygame.image.load("assets/gameover.png"), (288, 63))
game_over_rect = game_over_surface.get_rect(center=(216, 384))

# Game Sounds
flap_sound = pygame.mixer.Sound('sound/sfx_wing.wav')
death_sound = pygame.mixer.Sound('sound/sfx_hit.wav')
score_sound = pygame.mixer.Sound('sound/sfx_point.wav')

"""Main Game Loop"""
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and is_start_phase and not game_active:
                is_start_phase = False
                game_active = True
            elif event.key == pygame.K_SPACE and game_active:
                bird_movement = 0
                bird_movement -= 5
                flap_sound.play()
            elif event.key == pygame.K_p and game_active is False:
                game_active = True
                pipe_list.clear()
                bird_rect.center = (75, 384)
                bird_movement = 0
                score = 0
        if event.type == SPAWNPIPE and game_active:
            pipe_list.extend(create_pipe())
        if event.type == BIRDFLAP:
            if bird_index < 2:
                bird_index += 1
            else:
                bird_index = 0
            bird_surface, bird_rect = bird_animation()

    # bilt arguments = surface, (xpos, ypos), Main Screen Creating
    if 0 <= score <= 10:
        screen.blit(bg_surface, (0, 0))
    elif 11 <= score <= 20:
        screen.blit(bg_surface_night, (0, 0))
    elif 21 <= score <= 30:
        screen.blit(bg_surface, (0, 0))
    else:
        screen.blit(bg_surface_night, (0, 0))

    if is_start_phase:
        screen.blit(start_surface, start_rect)
        screen.blit(start_text, start_text_rect)
    elif game_active:
        # Drawing Birds
        bird_movement += gravity
        rotated_bird = rotate_bird(bird_surface)
        bird_rect.centery += bird_movement
        screen.blit(rotated_bird, bird_rect)
        game_active = check_collision(pipe_list)
        
        # Drawing Pipes
        pipe_list = move_pipes(pipe_list)
        draw_pipes(pipe_list)

        # Drawing Score
        pipe_score_check()
        score_display('main_game')

        # Drawing Floor
        floor_x_pos -= 3
        draw_floor()
        if floor_x_pos <= -432:
            floor_x_pos = 0
    else:
        screen.blit(game_over_surface, game_over_rect)
        high_score = update_score(score, high_score)
        score_display('game_over')

    pygame.display.update()
    clock.tick(120)

# Reference - https://youtu.be/UZg49z76cLw
# Changes made - 
# 1. Added game starting screen, game over screen, night mode, random pipe gaps
# 2. Highscore is saving in file, so it doesn't reset ecery time while closing the game
# 3. Made suitable for 1080P displays

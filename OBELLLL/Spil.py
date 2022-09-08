from turtle import speed
import pygame
from pygame.locals import *
import random

clock = pygame.time.Clock()

size = width, height = (1080,800)
road_w = int(width/1.6)
roadmark_w = int(width/80)
right_lane = width / 2 + road_w / 4
left_lane = width / 2 - road_w / 4
pygame.init()
running = True

font = pygame.font.SysFont(None, 32)

start_time = pygame.time.get_ticks() 

level = 1
# Window size
screen = pygame.display.set_mode((size))
# Set title
pygame.display.set_caption("OBEL FLYGTER FRA GUD (NO WAYYYY)")
#background color
screen.fill((10, 20, 30))
# apply changes
pygame.display.update()

# load good guy
obel = pygame.image.load("obelOnd.png")
obel_loc = obel.get_rect()
obel_loc.center = right_lane, height * 0.8

# load bad guy
obel2 = pygame.image.load("obelGud.jpg")
obel2_loc = obel2.get_rect()
obel2_loc.center = left_lane, height * 0.2

counter = 0

obel_on_right = True

# game loop
while running:
    # level up
    counter += 1

    # Timer:
    counting_time = pygame.time.get_ticks() - start_time

    # Change milliseconds into minutes, seconds, milliseconds
    counting_minutes = str(counting_time/60000).zfill(2)
    counting_seconds = str( (counting_time%60000)/1000 ).zfill(2)
    counting_millisecond = str(counting_time%1000).zfill(3)

    counting_string = f"{counting_seconds}S Level {level}"

    counting_text = font.render(str(counting_string), 1, (255,255,255))
    counting_rect = counting_text.get_rect(center = (300,50))

    # Increase game difficulty overtime
    if counter == 100:
        level += 1 
        counter = 0
        print("level up", level, level*0.25 + 0.75)

    ms = clock.tick(200)
    # Gud animation
    obel2_loc[1] += ms * (level*0.25 + 0.75)
    if obel2_loc[1] > height:
        if random.randint(0,1) == 0:
            obel2_loc.center=right_lane, -200
        else:
            obel2_loc.center=left_lane, -200

    # Lose condition
    collide = obel_loc.colliderect(obel2_loc)
    if collide:
        print("gud fik dig du kommer nu i himlen")
        break

    # Event listeners
    for event in pygame.event.get():
        if event.type == QUIT:
            running = False
        if event.type == KEYDOWN:
            if event.key in [K_a, K_LEFT] and obel_on_right:
                obel_on_right = False
                obel_loc = obel_loc.move([-int(road_w/2), 0])
            if event.key in [K_d, K_RIGHT] and not obel_on_right:
                obel_on_right = True
                obel_loc = obel_loc.move([int(road_w/2), 0])

    pygame.draw.rect(
    screen,
        (50, 50, 50),
        (width/2-road_w/2, 0, road_w, height)
    )
    pygame.draw.rect(
        screen,
        (255, 240, 60),
        (width/2 - roadmark_w/2, 0, roadmark_w, height)
    )
    pygame.draw.rect(
        screen,
        (255, 255, 255),
        (width/2 - road_w/2 + roadmark_w*2, 0, roadmark_w, height)
    )
    pygame.draw.rect(
        screen,
        (255, 255, 255),
        (width/2 + road_w/2 - roadmark_w*3, 0, roadmark_w, height)
    )


    screen.blit(counting_text, counting_rect)

    screen.blit(obel, obel_loc)
    screen.blit(obel2, obel2_loc)
    pygame.display.update()




pygame.quit() 

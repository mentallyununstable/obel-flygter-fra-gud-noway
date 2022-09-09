import pygame, sys
from button import Button
from pygame.locals import *
import random
import time
import json

with open("highscore.json", "r") as file:
    highscores = json.load(file)

clock = pygame.time.Clock()

gold = None

size = width, height = (1080,800)
road_w = int(width/1.6)
roadmark_w = int(width/80)
right_lane = width / 2 + road_w / 4
left_lane = width / 2 - road_w / 4
pygame.init()

font = pygame.font.SysFont("cambria", 25)
main_font = pygame.font.SysFont("cambria", 50)

# Window size
screen = pygame.display.set_mode((size))
# Set title
pygame.display.set_caption("OBEL FLYGTER FRA GUD (NO WAYYYY)")
# apply changes
pygame.display.update()

# load bad guy
obel2 = pygame.image.load("obelGud.jpg")



SCREEN = pygame.display.set_mode((1280, 720))

DEAD = pygame.image.load("dodlol.png")
BG = pygame.image.load("assets/Background.png")

def get_font(size): # Returns Press-Start-2P in the desired size
    return pygame.font.Font("assets/font.ttf", size)

def play():

    global gold

    if highscores.get("Highscore:") is not None:
        gold = highscores["Highscore:"] > 45
    else:
        gold = False

    # load good guy 
    if gold == True:
        obel = pygame.image.load("goldObel.png")
    else:
        obel = pygame.image.load("obelOnd.png")

    start_time = time.time()

    screen.fill((10, 20, 30))

    counter = 0

    level = 1

    obel_loc = obel.get_rect()
    obel_loc.center = right_lane, height * 0.8

    obel2_loc = obel2.get_rect()
    obel2_loc.center = left_lane, height * 0.2

    obel_on_right = True

    highscore_d = font.render(f"Highscore: {highscores['Highscore:']}", 1, (255,255,255))
    highscore_e = font.render(f"Dev Highscore: {highscores['DevHighscore:']}", 1, (255,255,255))



    screen.blit(highscore_d, (0, 0))
    screen.blit(highscore_e, (950, 5))

    while True:
            
        # level up
        counter += 1

        # Timer:
        counting_time = pygame.time.get_ticks() - start_time

        counting_seconds = round(time.time() - start_time, 2)

        counting_string = f"Level {level} {counting_seconds}s"

        counting_text = font.render(str(counting_string), 1, (255,255,255))
        counting_rect = counting_text.get_rect(left = 300)

        # Increase game difficulty overtime
        if counter == 1000:
            level += 1 
            counter = 0
            print("level up", level, level*0.25 + 0.75)

        ms = clock.tick(200)
        # Gud animation
        obel2_loc[1] += ms * (level*0.125 + 0.75)
        if obel2_loc[1] > height:
            if random.randint(0,1) == 0:
                obel2_loc.center=right_lane, -200
            else:
                obel2_loc.center=left_lane, -200

        # Lose condition
        collide = obel_loc.colliderect(obel2_loc)
        if collide:
            print("gud fik dig du kommer nu i himlen")
            if highscores.get("Highscore:") is not None:
                if highscores["Highscore:"] < counting_seconds:
                    highscores["Highscore:"] = counting_seconds
            else:
                highscores["Highscore:"] = counting_seconds
            endScreen(counting_seconds)
            
        # Event listeners
        for event in pygame.event.get():
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

        
def endScreen(counting_seconds: float):

    while True:
        DEAD_MOUSE_POS = pygame.mouse.get_pos()

        SCREEN.fill("white")
        SCREEN.blit(DEAD, (350, 350))


        DEAD_TEXT = get_font(30).render("Gud fangede dig", True, "Black")
        DEAD_RECT = DEAD_TEXT.get_rect(center=(640, 160))
        SCREEN.blit(DEAD_TEXT, DEAD_RECT)

        DEAD_BACK = Button(image=None, pos=(640, 660), 
                    text_input="BACK", font=get_font(75), base_color="Black", hovering_color="Green")
        DEAD_BACK.changeColor(DEAD_MOUSE_POS)
        DEAD_BACK.update(SCREEN)

        DEAD_TEXT2 = get_font(30).render("du kommer nu i himlen. L", True, "Black")
        DEAD_RECT2 = DEAD_TEXT2.get_rect(center=(640, 200))
        SCREEN.blit(DEAD_TEXT2, DEAD_RECT2)

        SCORE_TEXT = get_font(30).render(f"Du holdte kun {counting_seconds} sekunder", True, "Black")
        SCORE_RECT = SCORE_TEXT.get_rect(center=(640, 300))
        SCREEN.blit(SCORE_TEXT, SCORE_RECT)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if DEAD_BACK.checkForInput(DEAD_MOUSE_POS):
                    main_menu()

        pygame.display.update()



def options():

    while True:
        OPTIONS_MOUSE_POS = pygame.mouse.get_pos()

        SCREEN.fill("white")

        OPTIONS_TEXT = get_font(45).render("This is the OPTIONS screen.", True, "Black")
        OPTIONS_RECT = OPTIONS_TEXT.get_rect(center=(640, 260))
        SCREEN.blit(OPTIONS_TEXT, OPTIONS_RECT)

        OPTIONS_BACK = Button(image=None, pos=(640, 460), 
                            text_input="BACK", font=get_font(75), base_color="Black", hovering_color="Green")

        OPTIONS_BACK.changeColor(OPTIONS_MOUSE_POS)
        OPTIONS_BACK.update(SCREEN)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if OPTIONS_BACK.checkForInput(OPTIONS_MOUSE_POS):
                    main_menu()

        pygame.display.update()

def main_menu():
    while True:
        SCREEN.blit(BG, (0, 0))

        MENU_MOUSE_POS = pygame.mouse.get_pos()

        MENU_TEXT = get_font(50).render("OBEL FLYGTER FRA GUD", True, "#b68f40")
        MENU_RECT = MENU_TEXT.get_rect(center=(640, 100))

        PLAY_BUTTON = Button(image=pygame.image.load("assets/Play Rect.png"), pos=(640, 250), 
                            text_input="PLAY", font=get_font(75), base_color="#d7fcd4", hovering_color="White")
        OPTIONS_BUTTON = Button(image=pygame.image.load("assets/Options Rect.png"), pos=(640, 400), 
                            text_input="OPTIONS", font=get_font(75), base_color="#d7fcd4", hovering_color="White")
        QUIT_BUTTON = Button(image=pygame.image.load("assets/Quit Rect.png"), pos=(640, 550), 
                            text_input="QUIT", font=get_font(75), base_color="#d7fcd4", hovering_color="White")

        SCREEN.blit(MENU_TEXT, MENU_RECT)

        for button in [PLAY_BUTTON, OPTIONS_BUTTON, QUIT_BUTTON]:
            button.changeColor(MENU_MOUSE_POS)
            button.update(SCREEN)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if PLAY_BUTTON.checkForInput(MENU_MOUSE_POS):
                    if event.key in [K_SPACE]:
                        play()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if PLAY_BUTTON.checkForInput(MENU_MOUSE_POS):
                    play()
                if OPTIONS_BUTTON.checkForInput(MENU_MOUSE_POS):
                    options()
                if QUIT_BUTTON.checkForInput(MENU_MOUSE_POS):
                    pygame.quit()
                    with open("highscore.json", "w") as file:
                        json.dump(highscores, file, indent = 2)
                        print(json.dumps(highscores, indent = 2))
                    sys.exit()

        pygame.display.update()

main_menu()
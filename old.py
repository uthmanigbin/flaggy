#play_Cname == Country name

import pygame, sys
import json
import requests
import io
from pygame import mixer
from random import randint
from button import Button
from io import BytesIO
import imageio


pygame.init()
mixer.init()
mixer.music.load('assets/song.mp3')
mixer.music.set_volume(0)
mixer.music.play(loops=0, start=18.0, fade_ms = 0)

frame_width = 1280
frame_height = 720

screen = pygame.display.set_mode((frame_width, frame_height))
pygame.display.set_caption("Flaggy")

bg = pygame.image.load("assets/Background.png")

def get_font(size): # Returns Press-Start-2P in the desired size
    return pygame.font.Font("assets/font.ttf", size)

global randomizer
def randomizer():
        #retrieves json file
        with open('assets/flags.json') as fp:
            #sets var data to load json file
            data = json.load(fp)
            info = data["flags"]
            #picks a random number between the index of the array
            random_index = randint(0, len(info)-1)
            #returns json values for Country && URL at preditermined random number
            return info[random_index]["Country"], info[random_index]["URL"]

country, flag_url = randomizer()
wrong_flag_url = randomizer()[1]
print(country, 'this is the url', flag_url)

def load_gif_from_url(url):
    response = requests.get(url)
    gif_bytes = BytesIO(response.content)
    gif = imageio.mimread(gif_bytes)
    return gif


def play():
    score = 0
    global country, flag_url, wrong_country, wrong_flag_url

    while True:
        play_mouse_pos = pygame.mouse.get_pos()
        
        screen.blit(bg, (0,0))

        

        # Load information for the first flag
        url = flag_url
        frames1 = load_gif_from_url(url)
        current_frame_index1 = 0
        current_frame1 = frames1[current_frame_index1]
        pygame_frame1 = pygame.image.fromstring(current_frame1.tobytes(), current_frame1.shape[:2][::-1], "RGB")
        screen.blit(pygame_frame1, (107, 268))

        # Load information for the second flag
        wrong_url = wrong_flag_url
        frames2 = load_gif_from_url(wrong_url)
        current_frame_index2 = 0
        current_frame2 = frames2[current_frame_index2]
        pygame_frame2 = pygame.image.fromstring(current_frame2.tobytes(), current_frame2.shape[:2][::-1], "RGB")
        screen.blit(pygame_frame2, (824, 268))


        play_ques = get_font(30).render("Which of these is the flag off", True, "White")
        play_Cname = get_font(40).render(country, True, "#FA2C26")
        play_score = get_font(40).render("Score: "+str(score), True, "white")
        play_ques_rect = play_ques.get_rect(center=(640, 55))
        play_C_rect = play_Cname.get_rect(center=(640,138))
        play_score_rect = play_score.get_rect(center=(640, 519))
        screen.blit(play_ques, play_ques_rect)
        screen.blit(play_Cname, play_C_rect)
        screen.blit(play_score, play_score_rect)

        play_btn = Button(image=None, pos=(107, 268), text_input="BACK", font=get_font(75), base_color="Black", hovering_color="Green")

        

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if (107 <= play_mouse_pos[0] <= 107 + pygame_frame1.get_width()) and (268 <= play_mouse_pos[1] <= 268 + pygame_frame1.get_height()):
                    # Clicked on the first flag
                    score += 1
                    print('Clicked on the first flag')
                    country, flag_url = randomizer()
                    wrong_flag_url = randomizer()
                elif (107 + pygame_frame1.get_width() + 50 <= play_mouse_pos[0] <= 107 + pygame_frame1.get_width() + 50 + pygame_frame2.get_width()) and (268 <= play_mouse_pos[1] <= 268 + pygame_frame2.get_height()):
                    # Clicked on the second flag
                    print('Clicked on the second flag')
                    country, flag_url = randomizer()
                    wrong_flag_url = randomizer()
                    
                # if play_btn.checkForInput(play_mouse_pos):
                #     #increases score
                #     score += 1
                #     print('clicked on image')
                #     #renders a new country and flag when right country is picked
                #     country, flag_url = randomizer()
                #     wrong_flag_url = randomizer()[1]

        pygame.display.update()
    
def options():
    while True:
        OPTIONS_MOUSE_POS = pygame.mouse.get_pos()

        screen.fill("white")

        OPTIONS_TEXT = get_font(45).render("This is the OPTIONS screen.", True, "Black")
        OPTIONS_RECT = OPTIONS_TEXT.get_rect(center=(640, 260))
        screen.blit(OPTIONS_TEXT, OPTIONS_RECT)

        OPTIONS_BACK = Button(image=None, pos=(640, 460), 
                            text_input="BACK", font=get_font(75), base_color="Black", hovering_color="Green")

        OPTIONS_BACK.changeColor(OPTIONS_MOUSE_POS)
        OPTIONS_BACK.update(screen)

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
        screen.blit(bg, (0, 0))



        MENU_MOUSE_POS = pygame.mouse.get_pos()

        MENU_TEXT = get_font(100).render("MAIN MENU", True, "#ffffff")
        MENU_RECT = MENU_TEXT.get_rect(center=(640, 100))

        PLAY_BUTTON = Button(image=pygame.image.load("assets/Play Rect.png"), pos=(640, 250), 
                            text_input="PLAY", font=get_font(75), base_color="#d7fcd4", hovering_color="White")
        OPTIONS_BUTTON = Button(image=pygame.image.load("assets/Options Rect.png"), pos=(640, 400), 
                            text_input="OPTIONS", font=get_font(75), base_color="#d7fcd4", hovering_color="White")
        QUIT_BUTTON = Button(image=pygame.image.load("assets/Quit Rect.png"), pos=(640, 550), 
                            text_input="QUIT", font=get_font(75), base_color="#d7fcd4", hovering_color="White")

        screen.blit(MENU_TEXT, MENU_RECT)

        for button in [PLAY_BUTTON, OPTIONS_BUTTON, QUIT_BUTTON]:
            button.changeColor(MENU_MOUSE_POS)
            button.update(screen)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if PLAY_BUTTON.checkForInput(MENU_MOUSE_POS):
                    play()
                if OPTIONS_BUTTON.checkForInput(MENU_MOUSE_POS):
                    options()
                if QUIT_BUTTON.checkForInput(MENU_MOUSE_POS):
                    pygame.quit()
                    sys.exit()

        pygame.display.update()

main_menu()
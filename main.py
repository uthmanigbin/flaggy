import pygame
import json
import requests
from random import randint
from button import Button
from io import BytesIO
import imageio
from pygame import mixer
import sys

# Constants
FRAME_WIDTH = 1280
FRAME_HEIGHT = 720
MENU_BUTTON_HEIGHT = 150
PLAY_BUTTON_POSITION = (640, 250)
OPTIONS_BUTTON_POSITION = (640, 400)
QUIT_BUTTON_POSITION = (640, 550)

# Initialize pygame and mixer
pygame.init()
mixer.init()
mixer.music.load('assets/song.mp3')
mixer.music.set_volume(1)
mixer.music.play(loops=2, start=18.0, fade_ms=0)

# Set up the display
screen = pygame.display.set_mode((FRAME_WIDTH, FRAME_HEIGHT))
pygame.display.set_caption("Flaggy")

# Load background image
bg = pygame.image.load("assets/Background.png")

# Fonts
font_path = "assets/font.ttf"
font_large = pygame.font.Font(font_path, 100)
font_medium = pygame.font.Font(font_path, 75)
font_small = pygame.font.Font(font_path, 45)

# Functions
def randomizer():
    with open('assets/flags.json') as fp:
        data = json.load(fp)
        info = data["flags"]
        random_index = randint(0, len(info) - 1)
        return info[random_index]["Country"], info[random_index]["URL"]
    
# Initializations
country, flag_url = randomizer()
wrong_flag_url = randomizer()[1]

def load_gif_from_url(url):
    response = requests.get(url)
    gif_bytes = BytesIO(response.content)
    return imageio.mimread(gif_bytes)

def render_flag(x, y, url):
    frames = load_gif_from_url(url)
    current_frame = frames[0]
    new_width = 350
    new_height = 184
    pygame_frame = pygame.transform.scale(pygame.image.fromstring(current_frame.tobytes(), current_frame.shape[:2][::-1], "RGB"), (new_width, new_height))
    screen.blit(pygame_frame, (x, y))
    return pygame_frame

def display_text(text, size, color, position):
    font = pygame.font.Font(font_path, size)
    rendered_text = font.render(text, True, color)
    rect = rendered_text.get_rect(center=position)
    screen.blit(rendered_text, rect)

def game_over(score):
    while True:
        screen.fill("black")

        display_text("Game Over", 100, "red", (640, 200))
        display_text(f"Score: {score}", 75, "white", (640, 350))

        play_btn = Button(image=None, pos=(640, 500), text_input="Play Again", font=font_medium, base_color="Black", hovering_color="Green")
        play_btn.changeColor(pygame.mouse.get_pos())
        play_btn.update(screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if play_btn.checkForInput(pygame.mouse.get_pos()):
                    return True  # Restart the game

        pygame.display.update()

def play():
    global country, flag_url, wrong_flag_url

    score = 0
    game_over_flag = False

    while not game_over_flag:
        play_mouse_pos = pygame.mouse.get_pos()
        
        screen.blit(bg, (0, 0))

        # Load information for the first flag
        pygame_frame1 = render_flag(107, 268, flag_url)

        # Load information for the second flag
        pygame_frame2 = render_flag(824, 268, wrong_flag_url)

        # Render text and buttons
        display_text("Which of these is the flag off", 30, "White", (640, 55))
        display_text(country, 40, "#FA2C26", (640, 138))
        display_text(f"Score: {score}", 40, "white", (640, 519))

        play_btn = Button(image=None, pos=(107, 268), text_input="BACK", font=font_medium, base_color="Black", hovering_color="Green")

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
                    wrong_flag_url = randomizer()[1]
                elif (824 <= play_mouse_pos[0] <= 824 + pygame_frame2.get_width()) and (268 <= play_mouse_pos[1] <= 268 + pygame_frame2.get_height()):
                    # Clicked on the second flag
                    print('Clicked on the second flag')
                    country, flag_url = randomizer()
                    wrong_flag_url = randomizer()[1]

        if score >= 5:
            game_over_flag = True
            game_over(score)

        pygame.display.update()

def options():
    while True:
        options_mouse_pos = pygame.mouse.get_pos()

        screen.fill("white")

        # Display centered header and body in the options menu
        display_text("Credits:", 60, "Black", (640, 100))
        display_text("Flag Game", 40, "Black", (640, 200))
        display_text("Made by: Uthman Igbin", 30, "Black", (640, 350))
        display_text("Semester 1 study project", 30, "Black", (640, 450))

        options_back = Button(image=None, pos=(640, 600), text_input="BACK", font=font_medium, base_color="Black", hovering_color="Green")
        options_back.changeColor(options_mouse_pos)
        options_back.update(screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if options_back.checkForInput(options_mouse_pos):
                    main_menu()

        pygame.display.update()

def main_menu():
    while True:
        screen.blit(bg, (0, 0))

        menu_mouse_pos = pygame.mouse.get_pos()

        display_text("MAIN MENU", 100, "#ffffff", (640, 100))

        play_button = Button(image=pygame.image.load("assets/Play Rect.png"), pos=PLAY_BUTTON_POSITION, text_input="PLAY", font=font_medium, base_color="#d7fcd4", hovering_color="White")
        options_button = Button(image=pygame.image.load("assets/Options Rect.png"), pos=OPTIONS_BUTTON_POSITION, text_input="OPTIONS", font=font_medium, base_color="#d7fcd4", hovering_color="White")
        quit_button = Button(image=pygame.image.load("assets/Quit Rect.png"), pos=QUIT_BUTTON_POSITION, text_input="QUIT", font=font_medium, base_color="#d7fcd4", hovering_color="White")

        for button in [play_button, options_button, quit_button]:
            button.changeColor(menu_mouse_pos)
            button.update(screen)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if play_button.checkForInput(menu_mouse_pos):
                    play()
                if options_button.checkForInput(menu_mouse_pos):
                    options()
                if quit_button.checkForInput(menu_mouse_pos):
                    pygame.quit()
                    sys.exit()

        pygame.display.update()

main_menu()

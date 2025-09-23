import pygame

FILE_RECORDS = "records.txt"

WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
DARK_BLUE = (0, 0, 180)
BEIGE = (244, 239, 231)
BROWN = (61, 43, 39)

FONT = "Comic Sans MS"

GAME_WIDTH = 360
GAME_HEIGHT = 640

TIME_DELAY = 700

poki_x = GAME_WIDTH / 4
poki_y = GAME_HEIGHT / 2
poki_width = 79
poki_height = 95

# columns
column_x = GAME_WIDTH
column_y = 0
column_width = 60
column_height = 512

# load assets
kite_logo = pygame.image.load("../assets/Kite-Logo.png")

poki_image = pygame.image.load("../assets/PoKi-icon.png")
poki_image = pygame.transform.scale(poki_image, (poki_width, poki_height))

start_menu_image = pygame.image.load("../assets/start_menu.png")
background_image = pygame.image.load("../assets/background.png")
points_bar_image = pygame.image.load("../assets/points-bar.png")
game_over_image = pygame.image.load("../assets/game_over_menu.png")

top_column_image = pygame.image.load("../assets/column-top.png")
top_column_image = pygame.transform.scale(top_column_image, (column_width, column_height))

bottom_column_image = pygame.image.load("../assets/column-bottom.png")
bottom_column_image = pygame.transform.scale(bottom_column_image, (column_width, column_height))

FLAP_SOUND = "../assets/flappy_sound.mp3"
POINT_SOUND = "../assets/point_sound.mp3"
GAME_OVER_SOUND = "../assets/game_over_sound.mp3"
MENU_OST = "../assets/menu_ost.mp3"

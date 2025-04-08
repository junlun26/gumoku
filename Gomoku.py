import pygame
import numpy as np

pygame.init()
pygame.mixer.init()
pygame.display.set_caption("Gomoku")
icon = pygame.image.load("./Images/icon.jpg")
pygame.display.set_icon(icon)
WIDTH, HEIGHT = 900, 900
FPS = 60
BACKGROUND = pygame.transform.scale(pygame.image.load("./Images/board.jpg"), (WIDTH, HEIGHT))
screen = pygame.display.set_mode((WIDTH,HEIGHT))
screen.blit(BACKGROUND, (0, 0))
origin = WIDTH*0.037
space = WIDTH*2/30
img_size = round(origin*8/5)
blackstone = pygame.transform.scale(pygame.image.load("./Images/black.jpg").convert(), (img_size, img_size))
whitestone = pygame.transform.scale(pygame.image.load("./Images/white.jpg").convert(), (img_size, img_size))
blackmark = pygame.transform.scale(pygame.image.load("./Images/black mark.jpg").convert(), (img_size, img_size))
whitemark = pygame.transform.scale(pygame.image.load("./Images/white mark.jpg").convert(), (img_size, img_size))
blackstone.set_colorkey((255, 255, 255))
whitestone.set_colorkey((255, 255, 255))
blackmark.set_colorkey((255, 255, 255))
whitemark.set_colorkey((0, 0, 0))
play_sound = pygame.mixer.Sound("./Sounds/play.wav")
win_sound = pygame.mixer.Sound("./Sounds/win.wav")

clock = pygame.time.Clock()
show_init = True
running = True
LIMIT = 15
stone_color = {1:blackstone,-1:whitestone}
mark_color = {1:blackmark,-1:whitemark}

class Locate(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = blackmark
        self.rect = self.image.get_rect()

    def update(self, new_x, new_y, color):
        self.image = mark_color[color]
        self.rect.centerx = new_x*space+origin
        self.rect.centery = new_y*space+origin

class Stone(pygame.sprite.Sprite):
    def __init__(self, x, y, color):
        super().__init__()
        self.image = stone_color[color]
        self.rect = self.image.get_rect()
        self.rect.centerx = x*space+origin
        self.rect.centery = y*space+origin

font_name = pygame.font.match_font("SimSun")
def draw_text(surf, text, size, x, y):
    font = pygame.font.Font(font_name, size)
    text_surface = font.render(text, True, (0,0,0))
    text_rext = text_surface.get_rect()
    text_rext.centerx = x
    text_rext.top = y
    surf.blit(text_surface, text_rext)

def draw_init():
    draw_text(screen, "五子棋", 128, WIDTH/2, HEIGHT/3)
    draw_text(screen, "點擊任意處開始遊戲", 64, WIDTH/2, HEIGHT/2)
    pygame.display.flip()

def wait():
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    waiting = False

def reset_the_game():
    global LIMIT, board, go, times, all_sprites, location
    board = np.zeros((LIMIT,LIMIT))
    go = 1
    times = 0
    all_sprites = pygame.sprite.Group()
    location = Locate()
    all_sprites.add(location)

def refresh_screen():
    screen.blit(BACKGROUND, (0, 0))
    all_sprites.draw(screen)
    pygame.display.flip()
    clock.tick(FPS)

def play_gomoku(x, y):
    global board, go, times
    if board[y][x]==0:
        play_sound.play()
        board[y][x]=go
        stone = Stone(x,y,go)
        all_sprites.add(stone)
        x_winnig_method = {0:1, 1:0, 2:1, 3:1}
        y_winnig_method = {0:0, 1:1, 2:1, 3:-1}
        for i in range(4):
            sum = 0
            X = x + x_winnig_method[i]
            Y = y + y_winnig_method[i]
            if X<LIMIT and Y<LIMIT:
                while board[Y][X] == go:
                    sum += 1
                    X += x_winnig_method[i]
                    Y += y_winnig_method[i]
                    if X>=LIMIT or Y>=LIMIT:
                        break
            X = x - x_winnig_method[i]
            Y = y - y_winnig_method[i]
            if X<LIMIT and Y<LIMIT:
                while board[Y][X] == go:
                    sum += 1
                    X -= x_winnig_method[i]
                    Y -= y_winnig_method[i]
                    if X>=LIMIT or Y>=LIMIT:
                        break
            if sum >= 4:
                return "someone_wan"
        times += 1
        if times == LIMIT**2:
            return "draw"
        go=go*(-1)

def draw_winning(stone):
    global board, go, times
    who_win = {1:"黑棋贏了", -1:"白棋贏了", 0:"平手"}
    draw_text(screen, who_win[stone], 128, WIDTH/2, HEIGHT/3)
    draw_text(screen, "點擊任意處重新開始遊戲", 64, WIDTH/2, HEIGHT/2)
    pygame.display.flip()
    win_sound.play()
    reset_the_game()

draw_init()
wait()
reset_the_game()
while running:
    mouse_x, mouse_y = pygame.mouse.get_pos()
    x, y = round((mouse_x-origin)/space), round((mouse_y-origin)/space)
    location.update(x, y, go)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                result = play_gomoku(x,y)
                refresh_screen()
                if result == "someone_wan":                    
                    draw_winning(go)
                    wait()
                elif result == "draw":
                    draw_winning(0)
                    wait()

    refresh_screen()

pygame.quit()

# kullanılan görseller https://www.shutterstock.com/tr/ den alınmıştır.
# https://www.shutterstock.com/tr/image-vector/stone-wall-flat-icon-pixel-art-759577363

# gerekli kütüphaneleri ekliyoruz-----------------------------

import pygame
import sys
clock = pygame.time.Clock()
from pygame.locals import *

# ------------------------------------------------------------
# oyunumuzun çalışacağı pencere boyutlarını ayarlıyoruz-------

pygame.init()
pygame.display.set_caption('Altın Mağarası')
WINDOW_SIZE = (900, 600)
screen = pygame.display.set_mode(WINDOW_SIZE, 0, 32)
display = pygame.Surface((300, 200))
font = pygame.font.Font('gameFont.otf', 50)
font2 = pygame.font.Font('gameFont.otf', 10)

# ------------------------------------------------------------
# fonksiyonlarımızı tanımlıyoruz -----------------------------

# harita oluşturma -------------------------------------------

def load_map(path):
    f = open(path + '.txt', 'r')
    data = f.read()
    f.close()
    data = data.split('\n')
    game_map = []
    for row in data:
        game_map.append(list(row))
    return game_map


# cisimlerin yerleri -----------------------------------------

def collision_comp(rect, tiles):
    hit_list = []
    for tile in tiles:
        if rect.colliderect(tile):
            hit_list.append(tile)
    return hit_list


# karakterimizin hareket edebilmesini sağlıyoruz -------------
def move(rect, movement, tiles):
    collision_types = {'top': False, 'bottom': False, 'right': False, 'left': False}
    rect.x += movement[0]
    object_list = collision_comp(rect, tiles)
    for tile in object_list:
        if movement[0] > 0:
            rect.right = tile.left
            collision_types['right'] = True
        elif movement[0] < 0:
            rect.left = tile.right
            collision_types['left'] = True
        elif movement[0] > 0:
            rect.right = tile.left
            collision_types['right'] = True
        elif movement[0] < 0:
            rect.left = tile.right
            collision_types['left'] = True
    rect.y += movement[1]
    object_list = collision_comp(rect, tiles)
    for tile in object_list:
        if movement[1] > 0:
            rect.bottom = tile.top
            collision_types['bottom'] = True
        elif movement[1] < 0:
            rect.top = tile.bottom
            collision_types['top'] = True
    return rect, collision_types


# metin yazmak için ------------------------------------------
def draw_text(text, font, color, surface, x, y):
    textobj = font.render(text, 1, color)
    textrect = textobj.get_rect()
    textrect.topleft = (x, y)
    surface.blit(textobj, textrect)


# oyunu yeniden başlatmak için -------------------------------
def restart():
    while True:

        screen.blit(bg, (0, 0))
        draw_text('CANIN KALMADI', font, (255, 215, 0, 255), screen, 260, 100)
        draw_text('TEKRAR OYNAMAK ICIN R TUSUNA BAS', font, (255, 215, 0, 255), screen, 0, 200)
        draw_text('CIKMAK ICIN Q TUSUNA BAS', font, (255, 215, 0, 255), screen, 120, 300)

        for event in pygame.event.get():

            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_r:
                    game()
                if event.key == K_q:
                    pygame.quit()
                    sys.exit()

        pygame.display.update()
        clock.tick(60)


# oyun bittiğinde --------------------------------------------
def finish():
    while True:

        screen.blit(bg, (0, 0))
        draw_text('OYUN BITTI', font, (255, 215, 0, 255), screen, 330, 100)
        draw_text('TEKRAR OYNAMAK ICIN R TUSUNA BAS', font, (255, 215, 0, 255), screen, 0, 200)
        draw_text('CIKMAK ICIN Q TUSUNA BAS', font, (255, 215, 0, 255), screen, 120, 300)

        for event in pygame.event.get():

            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_r:
                    game()
                if event.key == K_q:
                    pygame.quit()
                    sys.exit()

        pygame.display.update()
        clock.tick(60)


# ana menu ---------------------------------------------------
def main_menu():
    click = False
    while True:

        screen.blit(bg, (0, 0))

        draw_text('ALTIN MAGARASI', font, (255, 215, 0, 255), screen, 270, 100)

        mx, my = pygame.mouse.get_pos()

        button_1 = pygame.Rect(350, 200, 200, 100)

        if button_1.collidepoint((mx, my)):
            if click:
                game()

        draw_text('BASLAT', font, (255, 215, 0, 255), screen, 378, 230)
        click = False
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    pygame.quit()
                    sys.exit()
            if event.type == MOUSEBUTTONDOWN:
                if event.button == 1:
                    click = True

        pygame.display.update()
        clock.tick(60)

# ------------------------------------------------------------
# kullanılacak resimleri ekliyoruz ---------------------------

true_scroll = [0, 0]
player_img = pygame.image.load('images/player.png')
grass_img = pygame.image.load('images/1.png')
vazo_img = pygame.image.load('images/2.png')
coin_img = pygame.image.load('images/3.png')
bullet_img = pygame.image.load('images/4.png')
lav_img = pygame.image.load('images/lav1.png')
lav2_img = pygame.image.load('images/lav2.png')
heal_img = pygame.image.load('images/heart.png')
bg = pygame.image.load("images/bg2.png")
bg2 = pygame.image.load("images/bg1.png")
new_img = pygame.image.load('images/fire.png')
door1 = pygame.image.load('images/door32.png')
wall = pygame.image.load('images/wall.png')

current_map = 'map'
# oyuna başladığımızda ---------------------------------------
def game():
    # gerekli tanımlamaları yazpıyoruz
    game_map = load_map(current_map)
    next_map = 'map2'
    collected = 0
    moving_right = False
    moving_left = False
    bullet_right = False
    bullet_left = False
    player_flip = False

    air_timer = 0
    air_timer_bullet = 0

    # karaterimiz ve mermiyi ekliyoruz
    player_rect = pygame.Rect(80, 100, 12, 15)
    bullet_rect = pygame.Rect(80, 100, 9, 1)

    player_heal = 5
    heal_rect = []
    for i in range(player_heal):
        heal_rect.append(pygame.Rect(i * 10, 0, 9, 1))

    player_y_momentum = 0

    sayac = 0
    running = True

    while running:

        display.blit(bg2, (0, 0))
        for i in range(player_heal):
            display.blit(heal_img, heal_rect[i])

        if player_heal <= 0:
            restart()
        display.blit(coin_img, (3,15))

        draw_text(str(collected), font2, (255, 255, 255), display, 22, 18)

        # karakterimizle beraber görüntünün hareket etmesini saylıyor
        true_scroll[0] += (player_rect.x - true_scroll[0] - 120) / 20
        true_scroll[1] += (player_rect.y - true_scroll[1] - 100) / 20
        scroll = true_scroll.copy()
        scroll[0] = int(scroll[0])
        scroll[1] = int(scroll[1])

        tile_rects = []
        tile_coins = []
        tile_vazo = []
        tile_enemies = []

        tile_finis = []
        y = 0

        # map.txt dosyasında belirlediğimiz kısımlara gerekli cisimleri yerleştiriyoruz
        for layer in game_map:
            x = 0
            for tile in layer:
                if tile == '1':
                    display.blit(grass_img, (x * 16 - scroll[0], y * 16 - scroll[1]))
                    tile_rects.append(pygame.Rect(x * 16, y * 16, 15, 15))
                if tile == '2':
                    display.blit(coin_img, (x * 16 - scroll[0], y * 16 - scroll[1]))
                    tile_coins.append(pygame.Rect(x * 16, y * 16, 15, 15))
                    for c in tile_coins:
                        if c.colliderect(player_rect):
                            game_map[y][x] = '0'
                            tile_coins.remove(c)
                            collected += 1
                if tile == '3':
                    display.blit(vazo_img, (x * 16 - scroll[0], y * 16 - scroll[1]))
                    tile_vazo.append(pygame.Rect(x * 16, y * 16, 15, 15))
                    for c in tile_vazo:
                        if c.colliderect(bullet_rect):
                            display.blit(new_img, (bullet_rect.x - scroll[0], bullet_rect.y - 5 - scroll[1]))
                            bullet_right = False
                            bullet_left = False
                            air_timer_bullet = 0
                            sayac = 0
                            game_map[y][x] = '2'
                            tile_vazo.remove(c)
                if tile == '4':
                    display.blit(lav_img, (x * 16 - scroll[0], y * 16 - scroll[1]))
                    tile_enemies.append(pygame.Rect(x * 16, y * 16, 15, 15))
                    for c in tile_enemies:
                        if c.colliderect(player_rect):
                            player_heal -= 1
                            player_rect.y -= 5
                            game_map[y][x] = '5'
                            tile_enemies.remove(c)
                if tile == '5':
                    display.blit(lav2_img, (x * 16 - scroll[0], y * 16 - scroll[1]))
                    tile_rects.append(pygame.Rect(x * 16, y * 16, 15, 15))
                if tile == '7':
                    display.blit(wall, (x * 16 - scroll[0], y * 16 - scroll[1]))
                if tile == '8':
                    display.blit(door1, (x * 16 - scroll[0], y * 16 - scroll[1]))
                if tile == '9':
                    tile_finis.append(pygame.Rect(x * 16, y * 16, 15, 15))
                    for c in tile_finis:
                        if c.colliderect(player_rect):
                            if next_map == 'map2':
                                game_map = load_map(next_map)
                                player_rect.x = 100
                                player_rect.y = 100
                                moving_right = False
                                next_map = ''
                            else:
                                finish()
                x += 1
            y += 1


        # karakterin sağa veya sola gitmesi
        player_movement = [0, 0]
        if moving_right:
            player_movement[0] += 2

        if moving_left:
            player_movement[0] -= 2

        # karakterimizin baktığı yöne doğru ateş etmek
        if not player_flip:
            if bullet_right:
                if sayac == 0:
                    bullet_rect.x = player_rect.x
                    bullet_rect.y = player_rect.y + 6
                    sayac += 1
                air_timer_bullet += 1
                if air_timer_bullet < 48:
                    display.blit(bullet_img, (bullet_rect.x - scroll[0], bullet_rect.y - scroll[1]))
                    bullet_rect.x += 3
                    hit_list = collision_comp(bullet_rect, tile_rects)
                    for tile in hit_list:
                        display.blit(new_img, (bullet_rect.x - scroll[0], bullet_rect.y - 5 - scroll[1]))
                        bullet_right = False
                        bullet_left = False
                        air_timer_bullet = 0
                        sayac = 0
                else:
                    bullet_right = False
                    bullet_left = False
                    air_timer_bullet = 0
                    sayac = 0
        if player_flip:
            if bullet_left:
                if sayac == 0:
                    bullet_rect.x = player_rect.x
                    bullet_rect.y = player_rect.y + 6
                    sayac += 1
                air_timer_bullet += 1
                if air_timer_bullet < 48:
                    display.blit(bullet_img, (bullet_rect.x - scroll[0], bullet_rect.y - scroll[1]))
                    bullet_rect.x -= 3
                    hit_list = collision_comp(bullet_rect, tile_rects)
                    for tile in hit_list:
                        display.blit(new_img, (bullet_rect.x - scroll[0], bullet_rect.y - 5 - scroll[1]))
                        bullet_left = False
                        bullet_right = False
                        air_timer_bullet = 0
                        sayac = 0
                else:
                    bullet_left = False
                    bullet_right = False
                    air_timer_bullet = 0
                    sayac = 0

        # karakterin zıplaması
        player_movement[1] += player_y_momentum
        player_y_momentum += 0.4
        if player_y_momentum > 3:
            player_y_momentum = 3

        # karakter hareketlerini engellemek için
        player_rect, collisions = move(player_rect, player_movement, tile_rects)

        if collisions['bottom']:
            player_y_momentum = 0
            air_timer = 0
        else:
            air_timer += 1
        if collisions['top']:
            player_y_momentum = 0
            air_timer = 0

        if player_movement[0] > 0:
            player_flip = False

        if player_movement[0] < 0:
            player_flip = True

        if player_rect.y > 200:
            player_rect.x = 100
            player_rect.y = 100
            player_heal -= 1
        display.blit(pygame.transform.flip(player_img, player_flip, False),
                     (player_rect.x - scroll[0], player_rect.y - scroll[1]))

        # bir tuşa basıldığında yapılacak olan işlemler
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

            if event.type == KEYDOWN:
                if event.key == K_r:
                    game()
                if event.key == K_RIGHT:
                    moving_right = True
                if event.key == K_LEFT:
                    moving_left = True
                if event.key == K_UP:
                    if air_timer < 6:
                        player_y_momentum = -5
                if event.key == K_SPACE:
                    bullet_right = True
                    bullet_left = True
            if event.type == KEYUP:
                if event.key == K_RIGHT:
                    moving_right = False
                if event.key == K_LEFT:
                    moving_left = False

        surf = pygame.transform.scale(display, WINDOW_SIZE)
        screen.blit(surf, (0, 0))
        pygame.display.update()
        clock.tick(60)


main_menu()

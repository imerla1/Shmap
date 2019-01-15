import pygame
import random
from os import path
from os import listdir

WIDTH = 800
HEIGHT = 600
fps = 30
white = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 153, 18)
GREEN = (0, 255, 0)
score = 0

# assets
img_dir = path.join(path.dirname(__file__), 'img')
meteors = path.join(path.dirname(__file__), 'Meteors')
sound_dir = path.join(path.dirname(__file__), 'sounds')
explosion_dir = path.join(path.dirname(__file__), 'damage')
player_explosion = path.join(path.dirname(__file__), 'player_exp')
power_up_dir = path.join(path.dirname(__file__), 'pow_ups')
explosion_list = listdir(explosion_dir)




font_Name = pygame.font.match_font('arial')


def draw_score(surf, text, size, x, y):
    font = pygame.font.Font(font_Name, size)
    text_surface = font.render(text, True, RED)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    surf.blit(text_surface, text_rect)


def new_mob():  # creates new mobs
    new_mo = Mob()
    all_sprites.add(new_mo)
    mobs.add(new_mo)


def health_bar(surf, x, y, pct):
    if pct < 0:
        pct = 0
    bar_len = 100
    bar_height = 10
    fill = (pct / 100) * bar_len
    outline_rect = pygame.Rect(x, y, bar_len, bar_height)
    fill_rect = pygame.Rect(x, y, fill, bar_height)
    pygame.draw.rect(surf, GREEN, fill_rect)
    pygame.draw.rect(surf, white, outline_rect, 2)


def draw_lives(surf, x, y, lives, lives_image):

    for live in range(lives):
        img_rect = lives_image.get_rect()
        img_rect.x = x + 30 * live
        img_rect.y = y
        surf.blit(lives_image, img_rect)
#  player sprite


class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(player_img, (60, 40))
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.radius = 25
        self.rect.x = WIDTH/2
        self.rect.bottom = HEIGHT - 10
        self.shield = 100
        self.lives = 3
        self.hidden = True
        self.hidden_timer = pygame.time.get_ticks()


    def update(self, *args):
        # unhide if hidden
        if self.hidden and pygame.time.get_ticks() - self.hidden_timer > 1000:
            self.hidden = False
            self.rect.centerx = WIDTH / 2
            self.rect.bottom = HEIGHT - 10
        speed = 5
        press = pygame.key.get_pressed()
        if press[pygame.K_LEFT]:
            self.rect.x -= speed
        if press[pygame.K_RIGHT]:
            self.rect.x += speed
        if self.rect.x > WIDTH + 25:
            self.rect.x = 0
        if self.rect.x < -25:
            self.rect.x = WIDTH


    def hide(self):
        # hide the player temporarily
        self.hidden = True
        hide_timer = pygame.time.get_ticks()
        self.rect.center = (WIDTH / 2, HEIGHT + 200)

    def shoot(self):
        bullet = Bullet(self.rect.centerx, self.rect.top)
        all_sprites.add(bullet)
        bullets.add(bullet)
        shoot_sound.play()


class Mob(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image_orig = random.choice(meteor_img)
        self.image_orig.set_colorkey(BLACK)
        self.rect = self.image_orig.get_rect()
        self.image = self.image_orig.copy()
        self.image.set_colorkey(BLACK)
        self.radius = int(self.rect.width * .85 / 2)
        self.rect.x = random.randrange(WIDTH - self.rect.width)
        self.rect.y = random.randrange(-100, -40)
        self.speedy = random.randrange(1, 8)
        self.speedx = random.randrange(-3, 3)
        self.rot = 0
        self.rot_speed = random.randrange(-8, 8)
        self.last_update = pygame.time.get_ticks()

    def rotate(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > 50:
            self.last_update = now
            self.rot = (self.rot + self.rot_speed) % 360
            new_image = pygame.transform.rotate(self.image_orig, self.rot)
            old_center = self.rect.center
            self.image = new_image
            self.rect = self.image_orig.get_rect()
            self.rect.center = old_center

    def update(self, *args):
        self.rotate()
        self.rect.x += self.speedx
        self.rect.y += self.speedy
        if self.rect.top > HEIGHT + 10 or self.rect.left < -25 or self.rect.right > HEIGHT + 25:
            self.rect.x = random.randrange(WIDTH - self.rect.width)
            self.rect.y = random.randrange(-100, -40)
            self.speedy = random.randrange(1, 8)


class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(laser_img, (10, 20))
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.bottom = y
        self.rect.centerx = x
        self.speedy = -10

    def update(self, *args):
        self.rect.y += self.speedy
        # kill bullet if moves off the top of the screen
        if self.rect.bottom < 0:
            self.kill()


class Pow(pygame.sprite.Sprite):
    def __init__(self, center):
        self.type = random.choice(['shield', 'gun'])
        pygame.sprite.Sprite.__init__(self)
        self.image = power_up_img[self.type]
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.pos = random.randint(0, WIDTH - 20)
        self.rect.center = center
        self.speedy = 5

    def update(self, *args):
        self.rect.y += self.speedy
        # kill bullet if moves off the top of the screen
        if self.rect.top > HEIGHT:
            self.kill()


class Explosion(pygame.sprite.Sprite):
    def __init__(self, center, size):
        pygame.sprite.Sprite.__init__(self)
        self.size = size
        self.image = explosion_animations[self.size][0]
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.frame = 0
        self.last_update = pygame.time.get_ticks()
        self.frame_rate = 50

    def update(self, *args):
        now = pygame.time.get_ticks()
        if now - self.last_update > self.frame_rate:
            self.last_update = now
            self.frame += 1
            if self.frame == len(explosion_animations[self.size]):
                self.kill()
            else:
                center = self.rect.center
                self.image = explosion_animations[self.size][self.frame]
                self.rect = self.image.get_rect()
                self.rect.center = center


pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("My game")
clock = pygame.time.Clock()

# Game Graphics
background = pygame.image.load(path.join(img_dir, 'background.png')).convert()
background_rect = background.get_rect()
player_img = pygame.image.load(path.join(img_dir, 'player.png')).convert()
laser_img = pygame.image.load(path.join(img_dir, 'laser.png'))
player_mini_img = pygame.transform.scale(player_img, (30, 20))
player_mini_img.set_colorkey(BLACK)


#player_mini_img.set_colrkey(BLACK)
meteor_names = listdir(meteors)
meteor_img = []
for each_meteor in meteor_names:
    meteor_img.append(pygame.image.load(path.join(meteors, each_meteor)).convert())
explosion_animations = {}
explosion_animations['lg'] = []
explosion_animations['sm'] = []
explosion_animations['player'] = []

for name in explosion_list:
    img = pygame.image.load(path.join(explosion_dir, name)).convert()
    img.set_colorkey(BLACK)
    img_lg = pygame.transform.scale(img, (75, 75))
    explosion_animations['lg'].append(img_lg)
    img_sm = pygame.transform.scale(img, (32, 32))
    explosion_animations['sm'].append(img_sm)
for i in range(9):
    filename = 'sonicExplosion0{}.png'.format(i)
    images = pygame.image.load(path.join(player_explosion, filename)).convert()
    images.set_colorkey(BLACK)
    explosion_animations['player'].append(images)

power_up_img = {}
power_up_img['shield'] = pygame.image.load(path.join(power_up_dir, 'shield_gold.png')).convert()
power_up_img['gun'] = pygame.image.load(path.join(power_up_dir, 'bolt_gold.png')).convert()





# Game Sounds
shoot_sound = pygame.mixer.Sound(path.join(sound_dir, "Laser_Shoot4.wav"))
explosion_sounds = []
for snd in ['exp1.wav', 'exp2.wav']:
    explosion_sounds.append(pygame.mixer.Sound(path.join(sound_dir, snd)))
pygame.mixer.music.load(path.join(sound_dir, 'back_sound.mp3'))
player_die_sound = pygame.mixer.Sound(path.join(sound_dir, 'player_die.ogg'))
pygame.mixer.music.set_volume(0.4)

#  sprite Groups
all_sprites = pygame.sprite.Group()
mobs = pygame.sprite.Group()
bullets = pygame.sprite.Group()
power_up = pygame.sprite.Group()
for i in range(8):
    new_mob()
player = Player()
all_sprites.add(player)

pygame.mixer.music.play(loops=-1)
# Game loop

running = True

while running:
    clock.tick(fps)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                player.shoot()

    # Update
    all_sprites.update()

    # check to see if bullet hit the mob
    bullet_hit = pygame.sprite.groupcollide(mobs, bullets, True, True)
    for _hit in bullet_hit:
        score += (55 - _hit.radius)
        random.choice(explosion_sounds).play()
        explos = Explosion(_hit.rect.center, 'lg')
        all_sprites.add(explos)
        if random.random() > 0.9:
            Power = Pow(_hit.rect.center)
            all_sprites.add(Power)
            power_up.add(Power)


        new_mob()
    # check to see if player hit Power up
    pow_ = pygame.sprite.spritecollide(player, power_up, True)
    for check in pow_:
        if check.type == 'shield':
            player.shield += random.randrange(10, 30)
        if player.shield >= 100:
            player.shield = 100
        if check.type == 'gun':
            pass

    # check to see if mob hit player
    hits = pygame.sprite.spritecollide(player, mobs, True, pygame.sprite.collide_circle)
    for hit in hits:
        player.shield -= hit.radius * 2

        explos = Explosion(hit.rect.center, 'sm')
        all_sprites.add(explos)
        new_mob()
        if player.shield <= 0:
            player_die_sound.play()
            player_death = Explosion(player.rect.center, 'player')
            all_sprites.add(player_death)
            player.hide()
            player.lives -= 1
            player.shield = 100

    # if the player died
    if player.lives == 0:
        running = False
    # Draw / render
    screen.fill(BLACK)
    screen.blit(background, background_rect)
    all_sprites.draw(screen)

    draw_score(screen, str(score), 18, WIDTH/2, 10)
    health_bar(screen, 5, 5, player.shield)
    draw_lives(screen, WIDTH - 100, 5, player.lives, player_mini_img)
    # after drawing everything
    pygame.display.flip()

pygame.quit()



















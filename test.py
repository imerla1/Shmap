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
score = 0

# assets
img_dir = path.join(path.dirname(__file__), 'img')
meteors = path.join(path.dirname(__file__), 'Meteors')
sound_dir = path.join(path.dirname(__file__), 'sounds')


font_Name = pygame.font.match_font('arial')


def draw_score(surf, text, size, x, y):
    font = pygame.font.Font(font_Name, size)
    text_surface = font.render(text, True, RED)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    surf.blit(text_surface, text_rect)


def health_bar(surf, text, size, x, y):
    pass


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

    def update(self, *args):
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
meteor_names = listdir(meteors)
meteor_img = []
for each_meteor in meteor_names:
    meteor_img.append(pygame.image.load(path.join(meteors, each_meteor)).convert())
# Game Sounds
shoot_sound = pygame.mixer.Sound(path.join(sound_dir, "Laser_Shoot4.wav"))
explosion_sounds = []
for snd in ['exp1.wav', 'exp2.wav']:
    explosion_sounds.append(pygame.mixer.Sound(path.join(sound_dir, snd)))
pygame.mixer.music.load(path.join(sound_dir, 'back_sound.mp3'))
pygame.mixer.music.set_volume(0.4)

#  sprite Groups
all_sprites = pygame.sprite.Group()
mobs = pygame.sprite.Group()
bullets = pygame.sprite.Group()
for i in range(8):
    m = Mob()
    all_sprites.add(m)
    mobs.add(m)
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
        m = Mob()
        all_sprites.add(m)
        mobs.add(m)

    # check to see if mob hit player
    hits = pygame.sprite.spritecollide(player, mobs, True, pygame.sprite.collide_circle)
    for hit in hits:
        player.shield -= hit.radius * 2
        if player.shield <= 0:
            running = False
    # Draw / render
    screen.fill(BLACK)
    screen.blit(background, background_rect)
    all_sprites.draw(screen)

    draw_score(screen, str(score), 18, WIDTH/2, 10)
    # after drawing everything
    pygame.display.flip()

pygame.quit()


















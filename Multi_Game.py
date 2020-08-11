import pygame

pygame.init()

win = pygame.display.set_mode((1280, 720))

pygame.display.set_caption("First Game")

walkRight = [pygame.image.load('R1.png'), pygame.image.load('R2.png'), pygame.image.load('R3.png'),
             pygame.image.load('R4.png'), pygame.image.load('R5.png'), pygame.image.load('R6.png'),
             pygame.image.load('R7.png'), pygame.image.load('R8.png'), pygame.image.load('R9.png')]
walkLeft = [pygame.image.load('L1.png'), pygame.image.load('L2.png'), pygame.image.load('L3.png'),
            pygame.image.load('L4.png'), pygame.image.load('L5.png'), pygame.image.load('L6.png'),
            pygame.image.load('L7.png'), pygame.image.load('L8.png'), pygame.image.load('L9.png')]
bg = pygame.image.load('bg2.png')
char = pygame.image.load('standing.png')

clock = pygame.time.Clock()

bullet_mu = pygame.mixer.Sound('bullet.wav')
impact = pygame.mixer.Sound('hit.wav')
bgmusic = pygame.mixer.music.load('music.wav')
pygame.mixer.music.play(-1)


class player(object):
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.vel = 5
        self.isJump = False
        self.left = False
        self.right = False
        self.walkCount = 0
        self.jumpCount = 10
        self.standing = True
        self.hitbox = (self.x + 17, self.y + 11, 29, 52)
        self.health = 10
        self.score = 0
        self.visible = True

    def draw(self, win):
        if self.walkCount + 1 >= 27:
            self.walkCount = 0
        if self.health >= 1 and self.visible:
            if not self.standing:
                if self.left:
                    win.blit(walkLeft[self.walkCount // 3], (self.x, self.y))
                    self.walkCount += 1
                elif self.right:
                    win.blit(walkRight[self.walkCount // 3], (self.x, self.y))
                    self.walkCount += 1
            else:
                if self.right:
                    win.blit(walkRight[0], (self.x, self.y))
                else:
                    win.blit(walkLeft[0], (self.x, self.y))
            self.hitbox = (self.x + 17, self.y + 11, 29, 52)
            pygame.draw.rect(win, (255, 0, 0), (self.hitbox[0], self.hitbox[1] - 20, 50, 10))
            pygame.draw.rect(win, (0, 128, 0), (self.hitbox[0], self.hitbox[1] - 20, 50 - (5 * (10 - self.health)), 10))

    def hit(self):
        i = 0
        if self.visible:
            self.health -= 1
        else:
            self.visible = False
        while i < 100:
            # pygame.time.delay(10)
            i += 1
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    i = 101
                    pygame.quit()


class projectile(object):
    def __init__(self, x, y, radius, color, facing):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.facing = facing
        self.vel = 8 * facing

    def draw(self, win):
        pygame.draw.circle(win, self.color, (self.x, self.y), self.radius)


def redrawGameWindow():
    win.blit(bg, (0, 0))
    man.draw(win)
    man2.draw(win)
    # goblin.draw(win)
    text = font.render('Score 1 : ' + str(man.score), 1, (0, 0, 0))
    text1 = font.render('Score 2 : ' + str(man2.score), 1, (0, 0, 0))
    win.blit(text, (380, 10))
    win.blit(text1, (120, 10))
    for bullet in bullets:
        bullet.draw(win)




    for bullet in bullets2:
        bullet.draw(win)

    if man2.score == 10 or man.health <= 0 or man2.score == 10 or man2.health <= 0:
        font3 = pygame.font.SysFont('comicsans', 30)
        if man2.score == 10:
            text3 = font3.render('Player 2 won', 1, (0, 0, 0))
        elif man.score == 10:
            text3 = font3.render('Player 1 won', 1, (0, 0, 0))
        font2 = pygame.font.SysFont('comicsans', 50)
        text1 = font2.render('Game Over', 1, (255, 0, 0))
        text2 = font3.render('Press R to start again', 1, (0, 0, 0))
        pygame.draw.rect(win, (0, 128, 0), (620-text1.get_width()/2, 100, 240, 60))
        win.blit(text1, (640-text1.get_width()/2, 100))
        win.blit(text2, (640-text2.get_width()/2, 130))
        win.blit(text3, (640-text3.get_width()/2, 160))

    pygame.display.update()


# mainloop
font = pygame.font.SysFont('comicsans', 30, True)
man = player(1050, 580, 64, 64)
man2 = player(100, 580, 64, 64)
shootLoop = 0
shootLoop2 = 0
bullets = []
bullets2 = []
run = True
enter = True

while run:
    clock.tick(27)

    if shootLoop2 > 0:
        shootLoop2 += 1
    if shootLoop2 > 5:
        shootLoop2 = 0

    if shootLoop > 0:
        shootLoop += 1
    if shootLoop > 5:
        shootLoop = 0

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    for bullet in bullets:
        if bullet.y - bullet.radius < man2.hitbox[1] + man2.hitbox[3] and bullet.y + bullet.radius > man2.hitbox[1]:
            if bullet.x + bullet.radius > man2.hitbox[0] and bullet.x - bullet.radius < man2.hitbox[0] + man2.hitbox[2]:
                if man.score <= 9 and man.visible:
                    man.score += 1
                    man2.hit()
                    bullets.pop(bullets.index(bullet))

        if 1100 > bullet.x > 0:
            bullet.x += bullet.vel
        else:
            bullets.pop(bullets.index(bullet))

    for bullet in bullets2:
        if bullet.y - bullet.radius < man.hitbox[1] + man.hitbox[3] and bullet.y + bullet.radius > man.hitbox[1]:
            if bullet.x + bullet.radius > man.hitbox[0] and bullet.x - bullet.radius < man.hitbox[0] + man.hitbox[2]:
                if man2.score <= 9 and man2.visible:
                    man.hit()
                    man2.score += 1
                    bullets2.pop(bullets2.index(bullet))

        if 1100 > bullet.x > 0:
            bullet.x += bullet.vel
        else:
            bullets2.pop(bullets2.index(bullet))

    keys = pygame.key.get_pressed()

    if keys[pygame.K_SPACE] and shootLoop == 0:
        bullet_mu.play()
        if man.left:
            facing = -1
        else:
            facing = 1

        if len(bullets) < 5:
            bullets.append(
                projectile(round(man.x + man.width // 2), round(man.y + man.height // 2), 6, (212, 175, 55), facing))

        shootLoop = 1

    if keys[pygame.K_f] and shootLoop2 == 0:
        bullet_mu.play()
        if man2.left:
            facing = -1
        else:
            facing = 1

        if len(bullets2) < 5:
            bullets2.append(
                projectile(round(man2.x + man2.width // 2), round(man2.y + man2.height // 2), 6, (212, 175, 55),
                           facing))

        shootLoop2 = 1

    if keys[pygame.K_LEFT] and man.x > man.vel:
        man.x -= man.vel
        man.left = True
        man.right = False
        man.standing = False
    elif keys[pygame.K_RIGHT] and man.x < 1100 - man.width - man.vel:
        man.x += man.vel
        man.right = True
        man.left = False
        man.standing = False
    else:
        man.standing = True
        man.walkCount = 0

    if not man.isJump:
        if keys[pygame.K_UP]:
            man.isJump = True
            man.right = False
            man.left = False
            man.walkCount = 0
    else:
        if man.jumpCount >= -10:
            neg = 1
            if man.jumpCount < 0:
                neg = -1
            man.y -= (man.jumpCount ** 2) * 0.5 * neg
            man.jumpCount -= 1
        else:
            man.isJump = False
            man.jumpCount = 10

    if keys[pygame.K_a] and man2.x > man2.vel:
        man2.x -= man2.vel
        man2.left = True
        man2.right = False
        man2.standing = False
    elif keys[pygame.K_d] and man2.x < 1100 - man2.width - man2.vel:
        man2.x += man2.vel
        man2.right = True
        man2.left = False
        man2.standing = False
    else:
        man2.standing = True
        man2.walkCount = 0

    if not (man2.isJump):
        if keys[pygame.K_w]:
            man2.isJump = True
            man2.right = False
            man2.left = False
            man2.walkCount = 0
    else:
        if man2.jumpCount >= -10:
            neg = 1
            if man2.jumpCount < 0:
                neg = -1
            man2.y -= (man2.jumpCount ** 2) * 0.5 * neg
            man2.jumpCount -= 1
        else:
            man2.isJump = False
            man2.jumpCount = 10


    if keys[pygame.K_r]:
        man.score = 0
        man2.score = 0
        man2.visible = True
        man.visible = True
        man.health = 10
        man2.health = 10
        man.x = 1050
        man2.x = 20
    redrawGameWindow()

pygame.quit()

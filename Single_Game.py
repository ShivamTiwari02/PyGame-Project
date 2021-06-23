import pygame

pygame.init()

win = pygame.display.set_mode((500, 480))

pygame.display.set_caption("First Game")

walkRight = [pygame.image.load('./Pygame-Images/Game/R1.png'), pygame.image.load('./Pygame-Images/Game/R2.png'), pygame.image.load('./Pygame-Images/Game/R3.png'),
             pygame.image.load('./Pygame-Images/Game/R4.png'), pygame.image.load('./Pygame-Images/Game/R5.png'), pygame.image.load('./Pygame-Images/Game/R6.png'),
             pygame.image.load('./Pygame-Images/Game/R7.png'), pygame.image.load('./Pygame-Images/Game/R8.png'), pygame.image.load('./Pygame-Images/Game/R9.png')]
walkLeft = [pygame.image.load('./Pygame-Images/Game/L1.png'), pygame.image.load('./Pygame-Images/Game/L2.png'), pygame.image.load('./Pygame-Images/Game/L3.png'),
            pygame.image.load('./Pygame-Images/Game/L4.png'), pygame.image.load('./Pygame-Images/Game/L5.png'), pygame.image.load('./Pygame-Images/Game/L6.png'),
            pygame.image.load('./Pygame-Images/Game/L7.png'), pygame.image.load('./Pygame-Images/Game/L8.png'), pygame.image.load('./Pygame-Images/Game/L9.png')]
bg = pygame.image.load('./Pygame-Images/Game/bg.jpg')
char = pygame.image.load('./Pygame-Images/Game/standing.png')

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

    def draw(self, win):
        if self.walkCount + 1 >= 27:
            self.walkCount = 0
        if self.health >= 1:
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
            # pygame.draw.rect(win, (255, 0, 0), self.hitbox, 2)
            pygame.draw.rect(win, (255, 0, 0), (self.hitbox[0], self.hitbox[1] - 20, 50, 10))
            pygame.draw.rect(win, (0, 128, 0), (self.hitbox[0], self.hitbox[1] - 20, 50 - (5 * (10 - self.health)), 10))

    def hit(self):
        self.x = 60
        self.y = 410
        self.walkCount = 0
        font1 = pygame.font.SysFont('comicsans', 100)
        text = font1.render('-5', 1, (255, 0, 0))
        win.blit(text, (250 - (text.get_width() / 2), 200))
        pygame.display.update()
        i = 0
        self.health -= 3
        while i < 100:
            pygame.time.delay(10)
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


class enemy(object):
    walkRight = [pygame.image.load('R1E.png'), pygame.image.load('R2E.png'), pygame.image.load('R3E.png'),
                 pygame.image.load('R4E.png'), pygame.image.load('R5E.png'), pygame.image.load('R6E.png'),
                 pygame.image.load('R7E.png'), pygame.image.load('R8E.png'), pygame.image.load('R9E.png'),
                 pygame.image.load('R10E.png'), pygame.image.load('R11E.png')]
    walkLeft = [pygame.image.load('L1E.png'), pygame.image.load('L2E.png'), pygame.image.load('L3E.png'),
                pygame.image.load('L4E.png'), pygame.image.load('L5E.png'), pygame.image.load('L6E.png'),
                pygame.image.load('L7E.png'), pygame.image.load('L8E.png'), pygame.image.load('L9E.png'),
                pygame.image.load('L10E.png'), pygame.image.load('L11E.png')]

    def __init__(self, x, y, width, height, end):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.end = end
        self.path = [self.x, self.end]
        self.walkCount = 0
        self.vel = 7
        self.hitbox = (self.x + 17, self.y + 2, 31, 57)
        self.health = 10
        self.visible = True

    def draw(self, win):
        self.move()
        if self.visible:
            if self.walkCount + 1 >= 33:
                self.walkCount = 0

            if self.vel > 0:
                win.blit(self.walkRight[self.walkCount // 3], (self.x, self.y))
                self.walkCount += 1
            else:
                win.blit(self.walkLeft[self.walkCount // 3], (self.x, self.y))
                self.walkCount += 1
            self.hitbox = (self.x + 17, self.y + 2, 31, 57)
            pygame.draw.rect(win, (255, 0, 0), (self.hitbox[0], self.hitbox[1] - 20, 50, 10))
            pygame.draw.rect(win, (0, 128, 0), (self.hitbox[0], self.hitbox[1] - 20, 50 - (5 * (10 - self.health)), 10))

    def move(self):
        if self.vel > 0:
            if self.x + self.vel < self.path[1]:
                self.x += self.vel
            else:
                self.vel = self.vel * -1
                self.walkCount = 0
        else:
            if self.x - self.vel > self.path[0]:
                self.x += self.vel
            else:
                self.vel = self.vel * -1
                self.walkCount = 0

    def hit(self):
        global score
        if self.health > 1:
            self.health -= 1
        else:
            self.visible = False
        impact.play()
        score += 1
        print('hit')


def redrawGameWindow():
    win.blit(bg, (0, 0))
    man.draw(win)
    goblin.draw(win)
    text = font.render('Score : ' + str(score), 1, (0, 0, 0))
    win.blit(text, (380, 10))
    for bullet in bullets:
        bullet.draw(win)
    if score == 10 or man.health <= 0:
        font2 = pygame.font.SysFont('comicsans', 50)
        font3 = pygame.font.SysFont('comicsans', 20)
        text1 = font2.render('Game Over', 1, (255, 0, 0))
        text2 = font3.render('Press R to start again', 1, (0, 0, 0))
        pygame.draw.rect(win, (0, 128, 0), (165, 190, 200, 50))
        win.blit(text1, (175, 200))
        win.blit(text2, (185, 250))

    pygame.display.update()


# mainloop
font = pygame.font.SysFont('comicsans', 30, True)
man = player(400, 410, 64, 64)
goblin = enemy(50, 410, 64, 64, 450)
shootLoop = 0
bullets = []
run = True
score = 0
enter = True


while run:
    clock.tick(30)

    if goblin.hitbox[1] < goblin.hitbox[3] + goblin.hitbox[1] and man.hitbox[3] + man.hitbox[1] > goblin.hitbox[1]:
        if man.hitbox[0] + man.hitbox[2] > goblin.hitbox[0] and man.hitbox[0] < goblin.hitbox[0] + goblin.hitbox[2]:
            if goblin.visible:
                man.hit()


    if shootLoop > 0:
        shootLoop += 1
    if shootLoop > 5:
        shootLoop = 0

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    for bullet in bullets:
        if bullet.y - bullet.radius < goblin.hitbox[1] + goblin.hitbox[3] and bullet.y + bullet.radius > goblin.hitbox[1]:
            if bullet.x + bullet.radius > goblin.hitbox[0] and bullet.x - bullet.radius < goblin.hitbox[0] + goblin.hitbox[2]:
                if score <= 9 and goblin.visible:
                    goblin.hit()
                    bullets.pop(bullets.index(bullet))

        if 500 > bullet.x > 0:
            bullet.x += bullet.vel
        else:
            bullets.pop(bullets.index(bullet))

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

    if keys[pygame.K_LEFT] and man.x > man.vel:
        man.x -= man.vel
        man.left = True
        man.right = False
        man.standing = False
    elif keys[pygame.K_RIGHT] and man.x < 500 - man.width - man.vel:
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
    if keys[pygame.K_r]:
        score = 0
        goblin.visible = True
        man.health = 10
        goblin.health = 10
        man.x = 450
        goblin.x = 20
    redrawGameWindow()

pygame.quit()

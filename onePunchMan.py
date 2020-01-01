import pygame
import os

pygame.init()
screen_width = 500
screen_height = 480
screen = pygame.display.set_mode((screen_width, screen_height))
os.chdir('img')
pygame.display.set_caption('FIRST GAME')
walkRight = [pygame.image.load('R1.png'), pygame.image.load('R2.png'), pygame.image.load('R3.png'),
             pygame.image.load('R4.png'), pygame.image.load('R5.png'), pygame.image.load('R6.png'),
             pygame.image.load('R7.png'), pygame.image.load('R8.png'), pygame.image.load('R9.png')]
walkLeft = [pygame.image.load('L1.png'), pygame.image.load('L2.png'), pygame.image.load('L3.png'),
            pygame.image.load('L4.png'), pygame.image.load('L5.png'), pygame.image.load('L6.png'),
            pygame.image.load('L7.png'), pygame.image.load('L8.png'), pygame.image.load('L9.png')]
bg = pygame.image.load('bg.jpg')
char = pygame.image.load('standing.png')

clock = pygame.time.Clock()

score = 0


class player(object):
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.velocity = 5
        self.isJump = False
        self.jumpCount = 10
        self.left = False
        self.right = False
        self.walkCount = 0
        self.standing = True
        self.hitbox = (self.x + 17, self.y + 11, 29, 52) # x y width height

    def redrawGameWindow(self):

        # pygame.draw.rect(screen, (200, 23, 255), pygame.Rect(x, y, width, height)) # last one is rect
        if self.walkCount >= 27:
            self.walkCount = 0

        if not self.standing:
            if self.left:
                screen.blit(walkLeft[self.walkCount // 3], (self.x, self.y))
                self.walkCount += 1
            elif self.right:
                screen.blit(walkRight[self.walkCount // 3], (self.x, self.y))
                self.walkCount += 1
        else:    # he is standing
            if self.right:
                screen.blit(walkRight[0],(self.x, self.y))
            else:
                screen.blit(walkLeft[0],(self.x, self.y))
        self.hitbox = (self.x + 17, self.y + 11, 29, 52) # x y width height
        # pygame.draw.rect(screen,(255,0,0),self.hitbox, 2 )
        # pygame.draw.rect(screen,(0,0,255),(self.x,self.y,self.width,self.height),1)

    def hit(self):
        self.x = 60
        self.walkCount = 0
        font2 = pygame.font.SysFont('comicsans',100)
        text2 = font2.render('-5',1,(255,0,0))
        screen.blit(text2,(screen_width//2 - text2.get_width()//2, screen_height//2 - text2.get_height()))
        pygame.display.update()
        pygame.time.delay(1000)

class projectile(object):
    def __init__(self,x,y,radius,color,facing):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.facing = facing
        self.velocity = 8*facing

    def draw(self):
        pygame.draw.circle(screen,self.radius,(self.x, self.y),self.radius, 0)
        # 1 if you want an outline of a circle ie not filled in, but we need a filled circle

class enemies(object):
    walkRight = [pygame.image.load('R1E.png'), pygame.image.load('R2E.png'), pygame.image.load('R3E.png'),
                 pygame.image.load('R4E.png'), pygame.image.load('R5E.png'), pygame.image.load('R6E.png'),
                 pygame.image.load('R7E.png'), pygame.image.load('R8E.png'), pygame.image.load('R9E.png'),
                 pygame.image.load('R10E.png'), pygame.image.load('R11E.png')]
    walkLeft = [pygame.image.load('L1E.png'), pygame.image.load('L2E.png'), pygame.image.load('L3E.png'),
                pygame.image.load('L4E.png'), pygame.image.load('L5E.png'), pygame.image.load('L6E.png'),
                pygame.image.load('L7E.png'), pygame.image.load('L8E.png'), pygame.image.load('L9E.png'),
                pygame.image.load('L10E.png'), pygame.image.load('L11E.png')]
    def __init__(self,x,y,width,height,end):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.end = end
        self.velocity = 3
        self.path = [x, end]
        self.walkCount = 0
        self.hitbox = (self.x + 17, self.y + 2, 31, 57) # x y width height
        self.health = 10
        self.visible = True

    def draw(self):
        self.move()
        if self.visible:
            if self.walkCount >= 33:
                self.walkCount = 0
            if self.velocity>0:
                screen.blit(self.walkRight[self.walkCount//3], (self.x, self.y))
                self.walkCount += 1
            else:
                screen.blit(self.walkLeft[self.walkCount // 3], (self.x, self.y))
                self.walkCount += 1

            pygame.draw.rect(screen, (255,0,0),(self.hitbox[0],self.hitbox[1] - 20,50,10))
            pygame.draw.rect(screen, (0,128,0),(self.hitbox[0],self.hitbox[1] - 20,50 - (5 * (10 - self.health)),10))
            self.hitbox = (self.x + 17, self.y + 2, 31, 57) # x y width height
            # pygame.draw.rect(screen, (255,0,0),self.hitbox, 2)


    def move(self):
        if self.velocity >0:
            if self.x < self.path[1] - self.velocity:
                self.x += self.velocity
            else:
                self.velocity *= -1
                self.walkCount = 0
        else:
            if self.x > self.path[0] + self.velocity:
                self.x += self.velocity
            else:
                self.velocity *= -1
                self.walkCount = 0
    def hit(self):
        if self.health> 1:
            self.health -= 1
        else:
            self.visible = False
        print('hit')


# main loop
font1 = pygame.font.SysFont('comicsans',30,True,False)  # last two are bold and italic
man = player(300, 410, 64, 64)
goblin = enemies(100,410, 64, 64, 450)
bullets = []
#bullet cooldown time
shootloop = 0
run = True
while run:
    # no of frames you see per seconds
    # pygame.time.delay(50)
    clock.tick(27)

    # man gets hit
    if goblin.visible:
        if man.hitbox[1] < goblin.hitbox[1] + goblin.hitbox[3] and man.hitbox[1] + man.hitbox[3] > goblin.hitbox[1]:
            if man.hitbox[0] + man.hitbox[2] > goblin.hitbox[0] and man.hitbox[0] < goblin.hitbox[0] + goblin.hitbox[2]:
                man.hit()
                score -= 5

    if shootloop > 0:
        shootloop += 1
    if shootloop > 3:
        shootloop = 0
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    for bullet in bullets:
        # above the bottom of rectangle
        # below the top of the rectangle
        if bullet.y + bullet.radius < goblin.hitbox[1] + goblin.hitbox[3] and bullet.y - bullet.radius > goblin.hitbox[1]:
            if bullet.x + bullet.radius > goblin.hitbox[0] and bullet.x - bullet.radius < goblin.hitbox[0] + goblin.hitbox[2]:
                goblin.hit()
                score += 1
                #remove bullet from the list
                bullets.remove(bullet)
        if 0 < bullet.x < 500 :
            bullet.x +=  bullet.velocity
        else:
            #bullets.pop(bullets.index(bullet))
            bullets.remove(bullet)


    keys = pygame.key.get_pressed()

    if keys[pygame.K_SPACE] and shootloop == 0:
        if len(bullets) < 5:
            if man.left:
                facing = -1
            else:
                facing = 1

            bullets.append(projectile(round(man.x + man.width//2), round(man.y + man.height//2),6,(0,0,0),facing ))
            shootloop = 1

    if keys[pygame.K_LEFT] and man.x > man.velocity:
        man.x -= man.velocity
        man.left = True
        man.right = False
        man.standing = False
    elif keys[pygame.K_RIGHT] and man.x < screen_width - man.width - man.velocity:
        man.x += man.velocity
        man.left = False
        man.right = True
        man.standing = False
    else:
        man.standing = True
        man.walkCount = 0

    if not man.isJump:
        # if keys[pygame.K_UP] and y > velocity:
        #     y -= velocity
        # if keys[pygame.K_DOWN] and y < screen_width-height - velocity:
        #     y += velocity
        if keys[pygame.K_UP]:
            man.isJump = True
            man.walkCount = 0
    else:
        if man.jumpCount >= -10:
            neg = 1
            if man.jumpCount < 0:
                neg = -1
            man.y -= neg * man.jumpCount ** 2 / 2
            man.jumpCount -= 1

        else:
            man.isJump = False
            man.jumpCount = 10

    # drawings

    # screen.fill((0, 0, 0))
    screen.blit(bg, (0, 0))
    text = font1.render('Score: '+str(score),True,(0,0,0))
    screen.blit(text, (390, 10))
    man.redrawGameWindow()
    goblin.draw()
    for bullet in bullets:
        bullet.draw()
    pygame.display.update()
pygame.quit()

import math
import pygame
import os 
import random
import ctypes
from timeit import default_timer as timer

pygame.init()
pygame.font.init()

#Window Setup
WIDTH, HEIGHT = 750, 570
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Runner Sid")
backgroundMusic = pygame.mixer.Sound(os.path.join("assets", "bensound-adventure.mp3"))
backgroundMusic.set_volume(0.05)
backgroundMusic.play()

#Load Images
icon = pygame.image.load(os.path.join("assets", "iconsid.png"))
pygame.display.set_icon(icon)
background = pygame.image.load(os.path.join("assets", "background.jpg"))
background = pygame.transform.scale(pygame.image.load(os.path.join("assets", "background.jpg")), (WIDTH, HEIGHT))
cannon = pygame.image.load(os.path.join("assets", "cannon.png"))
cannonFlipped = pygame.image.load(os.path.join("assets", "cannonflip.png"))
stickman = pygame.image.load(os.path.join("assets", "Stickman.png"))
cannonball = pygame.image.load(os.path.join("assets", "cannonball.png"))
check = pygame.transform.scale(pygame.image.load(os.path.join("assets", "flag-42582_640.png")), (30, 20))

#Cannonball class
class CannonBalls:
    def __init__(self, x, y, img):
        self.x = x
        self.y = y
        self.img = img
        self.mask = pygame.mask.from_surface(self.img)

    def draw(self, window):
        window.blit(self.img, (self.x, self.y))

    def move_ball(self, vel, flipped):
        if flipped == True:
            self.x -= vel
        else:
            self.x += vel

    def off_screen(self, width, flipped):
        return not(self.x <= width and self.x >= 0)

    def collision(self, obj):
        return collide(self, obj)

#Cannons class
class Cannons:
    COOLDOWN = 0
    cannonball = pygame.image.load(os.path.join("assets", "cannonball.png"))

    def __init__(self, x, y, flipped):
        self.x = x
        self.y = y
        self.cannon_img = None
        self.cannons = []
        self.coolDown = 0
        self.flipped = flipped

        if self.flipped == True:
            self.cannon_img = cannonFlipped
        else:
            self.cannon_img = cannon

        self.mask = pygame.mask.from_surface(self.cannon_img)

    def draw(self, WIN):
        WIN.blit(self.cannon_img, (self.x, self.y))
        for ball in self.cannons:
            ball.draw(WIN)

    def cooldown(self):
        if self.coolDown >= self.COOLDOWN:
            self.coolDown = 0
        elif self.coolDown > 0:
            self.coolDown += 1

    def shoot(self):
        if self.coolDown == 0:
            cannonBall = CannonBalls(self.x, self.y, cannonball)
            self.cannons.append(cannonBall)
            self.coolDown = 1

    def moveCannons(self, vel, obj, flipped):
        for ball in self.cannons:
            ball.move_ball(vel, flipped)
            if ball.off_screen(WIDTH, flipped):
                self.cannons.remove(ball)
                self.coolDown = 0
                self.shoot()
            else:
                if ball.collision(obj):
                    if ball in self.cannons:
                        self.cannons.remove(ball)
                        obj.x = 0
                        obj.y = 520
                        self.coolDown = 0
    
#Main Character class
class Stickman:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.img = stickman
        self.mask = pygame.mask.from_surface(self.img)

    def draw(self, WIN):
        WIN.blit(self.img, (self.x, self.y))

#Snakes class
class Snake: 
    def __init__(self, x, y, image):
        self.x = x
        self.y = y
        self.image = image

    def draw(self, WIN):
        WIN.blit(self.image, (self.x, self.y))

#Collision Function
def collide(obj1, obj2):
    offset_x = obj2.x - obj1.x
    offset_y  = obj2.y - obj1.y
    return obj1.mask.overlap(obj2.mask, (offset_x, offset_y)) != None

#Cannon Boundary Function
def cannon_boundary(stickx, sticky, cannonx, cannony):
    distance = math.sqrt(math.pow(stickx-cannonx, 2) + math.pow(sticky-cannony, 2))
    if distance < 60:
        return True
    else:
        return False

#Snaker Boundary Function
def snake_boundary(stickx, sticky, snakex, snakey):
    distance = math.sqrt(math.pow(stickx-snakex, 2) + math.pow(sticky-snakey, 2))
    if distance < 30:
        return True
    else:
        return False

#Main Game Loop Function
def main(start):
    run = True
    FPS = 60
    main_font = pygame.font.SysFont("comicsans", 25)

    mainCharacter = Stickman(10, 500)
    playerVel = 2
    cannonball_Vel = 7

    cannon0 = Cannons(0, 395, False)
    cannon1 = Cannons(670, 120, True)
    cannon2 = Cannons(0, 200, False)
    cannon3 = Cannons(670, 280, True)
    cannon4 = Cannons(0, 50, False)
    cannon5 = Cannons(670, 465, True)
    cannons = [cannon0, cannon1, cannon2, cannon3, cannon4, cannon5]

    snake = pygame.transform.scale(pygame.image.load(os.path.join("assets", "snake-161424_640.png")), (40, 30))

    snake1 = Snake(450, 200, snake)
    snake2 = Snake(200, 25, snake)
    snake3 = Snake(366, 500, snake)
    snake4 = Snake(430, 87, snake)
    snake5 = Snake(150, 450, snake)
    snake6 = Snake(600, 300, snake)
    snake7 = Snake(550, 200, snake)
    snake8 = Snake(200, 300, snake)
    snake9 = Snake(600, 10, snake)
    snake10 = Snake(500, 500, snake)
    snake11 = Snake(366, 400, snake)
    snake12 = Snake(200, 100, snake)
    snake13 = Snake(150, 200, snake)
    snake14 = Snake(450, 300, snake)
    snake15 = Snake(340, 200, snake)
    snake16 = Snake(580, 100, snake)
    snakes = [snake1, snake2, snake3, snake4, snake5, snake6, snake7, snake8, snake9, snake10, snake11, snake12, snake13, snake14, snake15, snake16]

    clock = pygame.time.Clock()

    def redraw_window():
        WIN.blit(background, (0, 0))
        endTemp = timer()
        endTemp = round(endTemp - start, 2)
        time_label = main_font.render(f"Time: {endTemp}", 1, (255, 255, 255))
        WIN.blit(time_label, (10, 10))

        mainCharacter.draw(WIN)
        cannon0.draw(WIN)
        cannon1.draw(WIN)
        cannon2.draw(WIN)
        cannon3.draw(WIN)
        cannon4.draw(WIN)
        cannon5.draw(WIN)

        WIN.blit(check, (700, 10))

        for snake in snakes:
            snake.draw(WIN)

        pygame.display.update()

    while run:
        clock.tick(FPS)
        redraw_window()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP] and mainCharacter.y - playerVel > 0:
            mainCharacter.y -= playerVel
        if keys[pygame.K_DOWN] and mainCharacter.y + playerVel + 50 < HEIGHT:
            mainCharacter.y += playerVel
        if keys[pygame.K_RIGHT] and mainCharacter.x + playerVel + 50 < WIDTH:
            mainCharacter.x += playerVel
        if keys[pygame.K_LEFT] and mainCharacter.x - playerVel > 0:
            mainCharacter.x -= playerVel

        i = 0
        for cannon in cannons:
            restriction = cannon_boundary(mainCharacter.x, mainCharacter.y, cannon.x, cannon.y)

            if random.randrange(0, 2*10) == 1:
                cannon.shoot()

            if restriction == True:
                mainCharacter.x = 0
                mainCharacter.y = 520  

            if i % 2 == 0:
                cannon.moveCannons(cannonball_Vel, mainCharacter, False)
            else:
                cannon.moveCannons(cannonball_Vel, mainCharacter, True)
            
            i += 1

        i = 0

        for snake in snakes:
            if snake_boundary(mainCharacter.x, mainCharacter.y, snake.x, snake.y):
                mainCharacter.x = 0
                mainCharacter.y = 520

        if mainCharacter.y <= 40 and mainCharacter.x >= 690:
            if cannonball_Vel == 11:
                return round((timer() - start), 3)
            else:
                mainCharacter.x = 0
                mainCharacter.y = 520
                ctypes.windll.user32.MessageBoxW(0, "Congratulations. Round " + (str) (cannonball_Vel - 5) + " will now start", "ROUND OVER", 1)
                cannonball_Vel += 1

        if (mainCharacter.x >= 150) and (mainCharacter.x <= 190) and (mainCharacter.y >= 450) and (mainCharacter.y <= 420):
            mainCharacter.x = 0
            mainCharacter.y = 520


#Menu Function
def main_menu():
    title_font = pygame.font.SysFont("comicsans", 30)
    run = True
    while run:
        WIN.blit(background, (0,0))
        title_label = title_font.render("Press SPACE To Start Running. For Instructions, press h.", 1, (255,255,255))
        WIN.blit(title_label, (85, 285))
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE]:
            start = timer()
            time = main(start)
            if time != None:
                ctypes.windll.user32.MessageBoxW(0, "Congratulations! You did it! Sid took " + (str) (time) + " seconds to finish", "GAME OVER", 1)
        if keys[pygame.K_h]:
            ctypes.windll.user32.MessageBoxW(0, "To win, simply reach the chequered flag. Use the arrow keys to move Sid. Avoid snakes, cannons and the cannonballs fired. Your total time will be recorded. There are 5 rounds.", "Instructions", 1)
                

    pygame.quit()


main_menu()
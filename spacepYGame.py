import pygame
import random
import math

pygame.init()

# Creating a display
width = 600
height = 700
gameWindow = pygame.display.set_mode((width, height))
pygame.display.set_caption("Space Shooter")

# Colors
white = (255, 255, 255)
red = (255, 0, 0)

# Loading images
bg = pygame.image.load('bg.jpg')
bg = pygame.transform.scale(bg, (width, height)).convert_alpha()

# Game specific variables
# Exit and Over and FPS
exit_game = False
game_over = False
fps = 30

# Spaceship
spaceShip = pygame.image.load('spaceShip.png')
spaceShip = pygame.transform.scale(spaceShip, (70, 70)).convert_alpha()
spaceShip_x = 260
spaceShip_y = 620
spaceShip_vel = 0

# Aliens
aliens = []
aliens_x = []
aliens_y = []
alienX_vel = []
alienY_vel = []
numAliens = 6
for i in range(numAliens):
    aliens.append(pygame.image.load('alien.png'))
    aliens[i] = pygame.transform.scale(aliens[i], (70, 50)).convert_alpha()
    aliens_x.append(random.randint(0, width))
    aliens_y.append(100)
    alienX_vel.append(5)
    alienY_vel.append(5)

# Bullets
bullet = pygame.image.load('bullet.png')
bullet = pygame.transform.scale(bullet, (15, 15)).convert_alpha()
bullet_x = 0
bullet_y = 620
bulletX_vel = 0
bulletY_vel = 10
bullet_state = "ready"

score = 0

font = pygame.font.SysFont(None, 50)
clock = pygame.time.Clock()

def fire_bullet(x, y):
    global bullet_state
    bullet_state = "fire"
    gameWindow.blit(bullet, (x + 28, y - 20))

def ifCollission(alX, aly, blX, blY):
    distance = math.sqrt(math.pow(alX - blX, 2) + math.pow(aly - blY, 2))
    if distance < 27:
        return True
    else:
        return False


while (not exit_game):
    with open("highScore.txt", "r") as f:
        highScore = f.read()
    font = pygame.font.SysFont(None, 30)
    gameWindow.blit(bg, (0, 0))
    gameWindow.blit(spaceShip, (spaceShip_x, spaceShip_y))
    for event in pygame.event.get():
        # print(event)
        if event.type == pygame.QUIT:
            exit_game = True

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT:
                spaceShip_vel = 5

            if event.key == pygame.K_LEFT:
                spaceShip_vel = -5

            if event.key == pygame.K_SPACE:
                if bullet_state == "ready":
                    bullet_x = spaceShip_x
                    fire_bullet(bullet_x, bullet_y)

    if bullet_y <= 0:
        bullet_y = 620
        bullet_state = "ready"

    if bullet_state == "fire":
        fire_bullet(bullet_x, bullet_y)
        bullet_y -= bulletY_vel

    spaceShip_x += spaceShip_vel
    if spaceShip_x <= 0:
        spaceShip_vel = 0
    elif spaceShip_x > 520:
        spaceShip_vel = 0


    for i in range(numAliens):
        aliens_x[i] += alienX_vel[i]
        if aliens_x[i] <= 0:
            alienX_vel[i] = 5
            aliens_y[i] += 20
        elif abs(aliens_x[i] - width) < 10:
            alienX_vel[i] = -5
            aliens_y[i] += 20

        collision = ifCollission(aliens_x[i], aliens_y[i], bullet_x, bullet_y)
        if collision:
            bullet_y = 620
            bullet_state = "ready"
            score += 1
            if score > int(highScore):
                with open("highScore.txt", "w") as f:
                    f.write(str(score))
            aliens_x[i] = random.randint(0, width)
            aliens_y[i] = 100

        if aliens_y[i] > 150:
            for j in range(numAliens):
                aliens_y[i] = 2000
            gameWindow.fill(white)
            text = font.render("GAME OVER", True, red)
            # text2 = font.render("--- Press Space to play again ---", True, red)
            gameWindow.blit(text, (230, 200))
            # gameWindow.blit(text2, (150, 250))

        # print(aliens_y)

    for i in range(numAliens):
        gameWindow.blit(aliens[i], (aliens_x[i], aliens_y[i]))
        i += 2
    highScore_text = font.render(f"Highest Score : {highScore}", True, red)
    gameWindow.blit(highScore_text, (400, 20))
    scoreText = font.render(f"Score : {score}", True, red)
    gameWindow.blit(scoreText, (10, 20))
    pygame.display.update()
    clock.tick(fps)

pygame.quit()
quit()


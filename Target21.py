#Imports
import random
import sys
import time

import pygame
from pygame.locals import QUIT

#Initilizes pygame and clock
pygame.init()
clock = pygame.time.Clock()

#Creates Display
Display = pygame.display.set_mode((400, 400))
Display.fill((200,200,200))
pygame.display.set_caption("Target 21!")
ico = pygame.image.load("target.png")
pygame.display.set_icon(ico)


#Resets display
def displayReset():
    Display.fill((200,200,200))
    pygame.display.set_caption("Target 21!")
    pygame.display.set_icon(ico)

#Changes X and Y
def targetCoords():
    x = random.randint(20, 300)
    y = random.randint(20, 300)
    return x, y


#Creates a sprite for target
class clickSprite(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.image.load("targetSprite.png")
        self.image.set_colorkey((255, 255, 255))
        self.image = pygame.transform.scale(self.image, (60, 60))
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.direction = random.choice(["left", "right"])
        self.lastMove = pygame.time.get_ticks()

    def move(self):
        speed = 5
        if self.direction == "left":
            self.rect.x -= speed
            if self.rect.x < 10:
              self.direction = "right"
        elif self.direction == "right":
            self.rect.x += speed
            if self.rect.x > 330:
              self.direction = "left"

#Creates a sprite for bonus duck
class bonusSprite(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.image.load("duck.png")
        self.image.set_colorkey((255, 255, 255))
        self.image = pygame.transform.scale(self.image, (30, 30))
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.direction = random.choice(["up", "down"])

    def move(self):
      speed = 2
      if self.direction == "up":
          self.rect.y -= speed
          if self.rect.y < 10:
            self.direction = "down"
      elif self.direction == "down":
          self.rect.y += speed
          if self.rect.y > 330:
            self.direction = "up"
            
#Defines the sprites (Targets & Duck)
allSprites = pygame.sprite.Group()
bonusDuck = pygame.sprite.Group()
duck = bonusSprite(*targetCoords())
tar1 = clickSprite(*targetCoords())
tar2 = clickSprite(*targetCoords())
tar3 = clickSprite(*targetCoords())
allSprites.add(tar1, tar2, tar3)
bonusDuck.add(duck)


#Makes a border around the game
def drawBorder():
    pygame.draw.rect(Display, (0, 0, 0), (0, 0, 400, 400), 10)


#Creates title and introduction screen
def titleScreen():
    titleFont = pygame.font.SysFont(None, 50)
    instFont = pygame.font.SysFont(None, 20)

    titleText = titleFont.render("Target 21!", True, (0, 0, 0))
    inst1Text = instFont.render("Click the targets to gain 1-5 points", True, (0, 0, 0))
    inst2Text = instFont.render("Click the duck to gain 2 points", True, (0, 0, 0))
    inst3Text = instFont.render("Don't click the background or you lose a life", True, (0, 0, 0))
    inst4Text = instFont.render("Lose all lives or get over 21 points and you lose", True, (0, 0, 0))
    inst5Text = instFont.render("Collect 21 points to win!!", True, (0, 0, 0))
    inst6Text = instFont.render("Click to Play!", True, (0, 0, 0))

    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN or (
                    event.type == pygame.KEYDOWN
                    and event.key == pygame.K_SPACE):
                return
        Display.fill((200, 200, 200))
        titleTarget = pygame.image.load("target.png")
        titleTarget = pygame.transform.scale(titleTarget, (70, 70))
        titleTarget.set_colorkey((255, 255, 255))
        Display.blit(titleTarget, (300, 50))
        Display.blit(titleText, (100, 50))
        Display.blit(inst1Text, (50, 110))
        Display.blit(inst2Text, (50, 140))
        Display.blit(inst3Text, (50, 170))
        Display.blit(inst4Text, (50, 200))
        Display.blit(inst5Text, (50, 230))
        Display.blit(inst6Text, (150, 300))
        pygame.display.update()
        clock.tick(60)

#Creates a button at the end of the game that restarts
def restartScreen():
    restartFont = pygame.font.SysFont(None, 30)
    restartText = restartFont.render("Play Again?", True, (0, 0, 0))
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                pygame.time.delay(100)
                return True

        Display.fill((200, 200, 200))
        Display.blit(restartText, (100, 200))
        pygame.display.update()
        clock.tick(60)


#Main loop
lives = 3
counter = 0
end = False
titleScreenShown = False
titleScreen()
while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN and not end:
            if tar1.rect.collidepoint(event.pos):
                counter += random.randint(1, 5)
                print(counter)
                x, y = targetCoords()
                tar1.rect.topleft = (x, y)
            elif tar2.rect.collidepoint(event.pos):
                counter += random.randint(1, 5)
                print(counter)
                x, y = targetCoords()
                tar2.rect.topleft = (x, y)
            elif tar3.rect.collidepoint(event.pos):
                counter += random.randint(1, 5)
                print(counter)
                x, y = targetCoords()
                tar3.rect.topleft = (x, y)
            elif duck.rect.collidepoint(event.pos):
              counter += 21
              print(counter)
              x, y = targetCoords()
              duck.rect.topleft = (x, y)
            else:
                lives -= 1
                lives = max(lives, 0)
                print("lives =")
                print(lives)
            if lives == 0:
                end = True
                counter -= random.randint(1, 5)
                counter = max(0, counter)
            if counter >= 21:
                end = True

    #Updates game and draws sprites
    for target in allSprites:
      target.move()
    duck.move()
    displayReset()
    drawBorder()
    allSprites.update()
    allSprites.draw(Display)
    bonusDuck.update()
    bonusDuck.draw(Display)

    #Actively Shows the points
    font = pygame.font.Font(None, 30)
    counterText = font.render("Points: " + str(counter), True, (0, 0, 0))
    Display.blit(counterText, (10, 10))

    #Actively shows the lives
    livesText = font.render("Lives: " + str(lives), True, (0, 0, 0))
    Display.blit(livesText, (310, 10))

    #Determines is the player lost or won
    if end:
        if counter == 21:
            displayReset()
            win = font.render("You Win!", True, (0, 0, 0))
            Display.blit(win, (140, 200))
            titleTarget = pygame.image.load("target.png")
            titleTarget = pygame.transform.scale(titleTarget, (70, 70))
            titleTarget.set_colorkey((255, 255, 255))
            Display.blit(titleTarget, (150, 60))
            pygame.display.update()
            displayReset()
            time.sleep(2)
            restartScreen()
        else:
            displayReset()
            lose = font.render("You Lose!", True, (0, 0, 0))
            Display.blit(lose, (150, 200))
            titleTarget = pygame.image.load("targetSprite.png")
            titleTarget = pygame.transform.scale(titleTarget, (110, 110))
            titleTarget.set_colorkey((255, 255, 255))
            Display.blit(titleTarget, (150, 60))
            pygame.display.update()
            time.sleep(2)
            restartScreen()

        #Displays restart button
        pygame.display.update()
        if restartScreen():
          lives = 3
          counter = 0
          end = False
          titleScreenShown = False
          titleScreen()

    #Updates game and shows fps
    pygame.display.update()
    clock.tick(60)


import pygame
import pygame_widgets

class Bird:
    def __init__(self, path, game):
        # ? Creating and optimizing the image
        self.path = path
        self.img = pygame.image.load(self.path)
        self.image = pygame.transform.smoothscale(self.img, (70, 70))
        self.image.convert()

        # ? Defining the hitbox of the image
        self.imageRect = self.image.get_rect()
        self.x, self.y = game.screenWidth * 0.3, game.screenHeight//2
        self.imageRect.center = self.x, self.y
        
        # ? Miscellaneous things
        self.count = 0
        self.jumpAcc = 0
        self.yVel = 0
        self.game = game
        self.win = self.game.win
        

    def draw(self):
        self.imageRect.center = self.x, self.y
        self.win.blit(self.image, self.imageRect)

    def jump(self):
        self.count += 1
        print('JUMP ', self.count)
        # ? Changing the jump acceleration to 2 X the positive value of game gravity to give going up and down on the same rate
        self.jumpAcc = -30 * self.game.GRAVITY

    def move(self):
        #* Finding net acceleration
        if self.jumpAcc != 0:
            self.netAcc = self.jumpAcc
            self.yVel = 0
        else:
            self.netAcc = self.game.GRAVITY
        #* delta y = ut + 1/2at^2
        #* 1s/FPS = seconds passed every frame
        try:
            self.y += self.yVel * 1/self.game.clock.get_fps() + 0.5 * self.netAcc * (1/self.game.clock.get_fps())**2
        except ZeroDivisionError:
            pass
        #* Getting new y velocity
        try:
            self.yVel += self.netAcc * 1/self.game.clock.get_fps()
        except ZeroDivisionError:
            pass
        
        #? If jump acceleration != 0, then reseting its value to 0
        if self.jumpAcc != 0:
            self.jumpAcc = 0

    def checkLoss(self):
        if self.y < 0 or self.y > self.game.screenHeight:
            run = False
import pygame
import random

class Game:
    def __init__(self):
        self.screenWidth, self.screenHeight = 1280, 720
        self.win = pygame.display.set_mode(
            (self.screenWidth, self.screenHeight))
        pygame.display.set_caption('Flappy Bird')
        pygame.init()
        #? Gravity is positive because y axis is inverted in pygame
        self.GRAVITY = 1000
        self.bg = pygame.image.load(r'D:\More Python Projects\Games\Flappy Bird\Assets\bg.jpg')
        self.bg = pygame.transform.smoothscale(self.bg, (self.screenWidth, self.screenHeight))
        #self.bg.convert(self.win)
        self.clock = pygame.time.Clock()
        
        #!Defining the image and optimizing it and placing the tube
        
        self.img = pygame.image.load(r'D:\More Python Projects\Games\Flappy Bird\Assets\pipe.png')
        
        #@ Bottom Tube
        self.bottomTube = pygame.transform.smoothscale(self.img, (155, 800))
        #self.bottomTube.convert(self.win)
        
        #@ Upper Tube
        self.upperTube = pygame.transform.flip(self.bottomTube, False, True)
        #self.upperTube.convert(self.win)

    def mainLoop(self):
        start = False
        self.pipes = list()
        self.run = True
        while self.run:
            #? Setting FPS
            self.clock.tick(60)

            self.events = pygame.event.get()
            for event in self.events:
                # * If cross button is pressed, the window will close
                if event.type == pygame.QUIT:
                    self.run = False
                #! If the space or mouse is clicked on the screen, jump function will be launched
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        player.jump()
                        start = True         
                if event.type == pygame.MOUSEBUTTONDOWN:
                    player.jump()
                    start = True

            if start:
                #@ If the pipes list is empty then one pipe is created
                if self.pipes == []:
                    self.pipes.append(Pipe(flappyBirdGame, self.bottomTube, self.upperTube))
                #@ New objects will be appended when the previous ones are 200 pixels away from the right corner
                elif self.pipes[-1].upperRect.right < 0.7 * self.screenWidth:
                    self.pipes.append(Pipe(flappyBirdGame, self.bottomTube, self.upperTube))
            
                #? Removing the pipes out of screen
                if self.pipes[0].upperRect.right < 0:
                    self.pipes.pop(0)             
                
            #? Movement of the pipes
            for pipe in self.pipes:
                pipe.move()

            # ? Movement of the bird
            player.move()
            #? Checking for loss
            player.checkLoss()
            
            print(self.clock.get_fps())

            #todo Updating the window
            self.updateWin()

        pygame.quit()

    def updateWin(self):
        self.win.blit(self.bg, (0,0))
        player.draw()
        for pipe in self.pipes:
            pipe.draw()
        pygame.display.update()


class Bird:
    def __init__(self, path, game):
        # ? Creating and optimizing the image
        self.path = path
        self.img = pygame.image.load(self.path)
        self.image = pygame.transform.smoothscale(self.img, (70, 70))
        #self.image.convert()

        # ? Defining the hitbox of the image
        self.rect = self.image.get_rect()
        self.x, self.y = game.screenWidth * 0.3, game.screenHeight//2
        self.rect.center = self.x, self.y
        
        # ? Miscellaneous things
        self.jumpAcc = 0
        self.yVel = 0
        self.game = game
        self.win = self.game.win
        

    def draw(self):
        self.rect.center = self.x, self.y
        self.win.blit(self.image, self.rect)

    def jump(self):
        # ? Changing the jump acceleration to 2 X the positive value of game gravity to give going up and down on the same rate
        self.jumpAcc = -20 * self.game.GRAVITY

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
            displacement = self.yVel * 0.0166 + 0.5 * self.netAcc * (0.0166)**2
            if self.y + displacement  - 35 >= 0:
                self.y += displacement
        except ZeroDivisionError:
            pass
        #* Getting new y velocity
        try:
            #* v = u + at
            self.yVel += self.netAcc * 0.0166 
        except ZeroDivisionError:
            pass
        
        #? If jump acceleration != 0, then reseting its value to 0
        if self.jumpAcc != 0:
            self.jumpAcc = 0

    def checkLoss(self):
        if self.y >= self.game.screenHeight :
            self.game.run = False
            
class Pipe:
    
    def __init__(self, game, bottomTube, upperTube):
        
        #! Default basic attributes
        self.game = game
        self.win = self.game.win
        self.vel = -3
        
        self.bottomTube = bottomTube
        self.upperTube = upperTube
        
        #@ Choosing location for upper and bottom tubes
        self.bottomRect = self.bottomTube.get_rect()
        self.bottomRect.top = random.randint(200, self.game.screenHeight - 100)
        self.bottomRect.left = self.game.screenWidth
        
        self.upperRect = self.upperTube.get_rect()
        #* The bottom of the upper tube is 150 px over the bottom tube
        self.upperRect.bottom = self.bottomRect.top - 200
        self.upperRect.left = self.game.screenWidth        
        
    def draw(self):
        self.win.blit(self.upperTube, self.upperRect)
        self.win.blit(self.bottomTube, self.bottomRect)
        
    def move(self):
        self.bottomRect.right += self.vel
        self.upperRect.right += self.vel

flappyBirdGame = Game()
player = Bird(
    r'D:\More Python Projects\Games\Flappy Bird\Assets\bird.png', flappyBirdGame)

flappyBirdGame.mainLoop()

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
        self.score = 0    
        
        #?Start Screen
        self.clickToStart = textOnScreen('Click or press SPACE to start', 80, (255,255,255),
                                    self.screenWidth//2, self.screenHeight//2) 

        #!Defining the image and optimizing it and placing the tube
        
        self.img = pygame.image.load(r'D:\More Python Projects\Games\Flappy Bird\Assets\pipe.png')
        
        #@ Bottom Tube
        self.bottomTube = pygame.transform.smoothscale(self.img, (155, 800))
        #self.bottomTube.convert(self.win)
        
        #@ Upper Tube
        self.upperTube = pygame.transform.flip(self.bottomTube, False, True)
        #self.upperTube.convert(self.win)

    def mainLoop(self):
        self.start = False
        self.pipes = list()
        scoreAdded = False
        self.run = True
        self.loss = False
        self.score = 0
        
        player.x, player.y = self.screenWidth * 0.3, self.screenHeight//2
        
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
                        self.start = True         
                if event.type == pygame.MOUSEBUTTONDOWN:
                    player.jump()
                    self.start = True

            if self.start:
                #@ If the pipes list is empty then one pipe is created
                if self.pipes == []:
                    self.pipes.append(Pipe(flappyBirdGame, self.bottomTube, self.upperTube))
                #@ New objects will be appended when the previous ones are 200 pixels away from the right corner
                elif self.pipes[-1].upperRect.right < 0.7 * self.screenWidth:
                    self.pipes.append(Pipe(flappyBirdGame, self.bottomTube, self.upperTube))
            
                #? Removing the pipes out of screen
                if self.pipes[0].upperRect.right < 0:
                    self.pipes.pop(0)     
                    scoreAdded = False        
                
                # ? Movement of the bird
                player.move()
                
                #? Checking for collision with the pipes
                for pipe in self.pipes:
                    if pipe.upperRect.colliderect(player.rect) or pipe.bottomRect.colliderect(player.rect):
                        self.loss = True 
                        
                #@ Adding score
                #todo If the first object in pipes list is to the left of the bird, then add 1 point
                if self.pipes[0].upperRect.right < player.rect.left and not scoreAdded:
                    self.score += 1
                    print(self.score)
                    scoreAdded = True

            #? Movement of the pipes
            for pipe in self.pipes:
                pipe.move()

            #? Checking for loss
            player.checkLoss()
            
            if self.loss:
                self.lossText = textOnScreen('YOU LOST', 70, (255,255,255), 
                                     self.screenWidth//2, self.screenHeight//2 - 60)
                self.lossScoreText = textOnScreen('YOUR SCORE:' + str(self.score), 70, (255,255,255),
                                                  self.screenWidth//2, self.screenHeight//2 + 60)
            #print(self.clock.get_fps())

            #todo Updating the window
            self.updateWin()

        pygame.quit()

    def updateWin(self):
        self.win.blit(self.bg, (0,0))
        
        player.draw(hitboxVisibility = False)
        for pipe in self.pipes:
            pipe.draw(hitboxVisibility = False)
        scoreText.text = str(self.score)
        scoreText.draw(self.win)
        
        if not self.start:
            self.clickToStart.draw(self.win, center = True)
            
        if self.loss:
            self.lossText.draw(self.win, center = True)
            self.lossScoreText.draw(self.win, center = True)
        
        pygame.display.update()
        if self.loss:
            pygame.time.delay(3000)
            self.mainLoop()

class textOnScreen:

    def __init__(self, text, size, color, x, y, **kwargs):
        self.text = text
        self.size = size
        self.color = color
        self.x = x
        self.y = y
        self.font = kwargs.get('font', 'Comic Sans MS')
        self.myfont = pygame.font.SysFont(self.font, self.size)
        self.angle = 0

    def draw(self, win, center=False, rotate=False):
        textsurface = self.myfont.render(self.text, True, self.color)
        if rotate:
            textsurface = pygame.transform.rotate(textsurface, self.angle)
        if center:
            rect = textsurface.get_rect(center=(self.x, self.y))
            win.blit(textsurface, rect)
        else:
            win.blit(textsurface, (self.x, self.y))

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
        

    def draw(self, hitboxVisibility = False):
        self.rect.center = self.x, self.y
        self.win.blit(self.image, self.rect)
        if hitboxVisibility:
            pygame.draw.rect(self.win, (0,0,255),self.rect, 2)

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
            self.game.loss = True
            
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
        
    def draw(self, hitboxVisibility = False):
        self.win.blit(self.upperTube, self.upperRect)
        self.win.blit(self.bottomTube, self.bottomRect)
        if hitboxVisibility:
            pygame.draw.rect(self.win, (255,0,0), self.upperRect, 2)
            pygame.draw.rect(self.win, (255,0,0), self.bottomRect, 2)
            
    def move(self):
        self.bottomRect.right += self.vel
        self.upperRect.right += self.vel

if __name__ == '__main__':

    flappyBirdGame = Game()

    player = Bird(
        r'D:\More Python Projects\Games\Flappy Bird\Assets\bird.png', flappyBirdGame)
    scoreText = textOnScreen(str(flappyBirdGame.score), 40, (255,255,255), 20, 20)

    flappyBirdGame.mainLoop()

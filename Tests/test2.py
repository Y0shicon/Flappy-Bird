import pygame
import random

screenWidth, screenHeight = 1280, 720
win = pygame.display.set_mode(
    (screenWidth, screenHeight))
pygame.display.set_caption('Flappy Bird')
pygame.init()

clock = pygame.time.Clock()  

class Bird:
    def __init__(self, path, win):
        # ? Creating and optimizing the image
        self.path = path
        self.img = pygame.image.load(self.path)
        self.image = pygame.transform.smoothscale(self.img, (70, 70))
        #self.image.convert()

        # ? Defining the hitbox of the image
        self.rect = self.image.get_rect()
        self.x, self.y = screenWidth * 0.3, screenHeight//2
        self.rect.center = self.x, self.y
        
        # ? Miscellaneous things
        self.jumpAcc = 0
        self.yVel = 0
        self.win = win
        

    def draw(self):
        self.rect.center = self.x, self.y
        self.win.blit(self.image, self.rect)

    def jump(self):
        # ? Changing the jump acceleration to 2 X the positive value of game gravity to give going up and down on the same rate
        self.jumpAcc = -20 * GRAVITY

    def move(self):
        #* Finding net acceleration
        if self.jumpAcc != 0:
            self.netAcc = self.jumpAcc
            self.yVel = 0
        else:
            self.netAcc = GRAVITY
        #* delta y = ut + 1/2at^2
        #* 1s/FPS = seconds passed every frame
        try:
            displacement = self.yVel * 1/clock.get_fps() + 0.5 * self.netAcc * (1/clock.get_fps())**2
            if self.y + displacement  - 35 >= 0:
                self.y += displacement
        except ZeroDivisionError:
            pass
        #* Getting new y velocity
        try:
            #* v = u + at
            self.yVel += self.netAcc * 1/clock.get_fps() 
        except ZeroDivisionError:
            pass
        
        #? If jump acceleration != 0, then reseting its value to 0
        if self.jumpAcc != 0:
            self.jumpAcc = 0

    def checkLoss(self, run):
        if self.y >= screenHeight :
            return False
        return True
            
class Pipe:
    
    def __init__(self, win):
        
        #! Default basic attributes
        self.win = win
        self.vel = -3
        
        #!Defining the image and optimizing it and placing the tube
        
        self.path = r'D:\More Python Projects\Games\Flappy Bird\Assets\pipe.png'
        self.img = pygame.image.load(self.path)
        
        #@ Bottom Tube
        self.bottomTube = pygame.transform.smoothscale(self.img, (155, 800))
        #self.bottomTube.convert(self.win)
        
        #@ Upper Tube
        self.upperTube = pygame.transform.flip(self.bottomTube, False, True)
        #self.upperTube.convert(self.win)
        
        #@ Choosing location for upper and bottom tubes
        self.bottomRect = self.bottomTube.get_rect()
        self.bottomRect.top = random.randint(200, screenHeight - 100)
        self.bottomRect.left = screenWidth
        
        self.upperRect = self.upperTube.get_rect()
        #* The bottom of the upper tube is 150 px over the bottom tube
        self.upperRect.bottom = self.bottomRect.top - 200
        self.upperRect.left = screenWidth        
        
    def draw(self):
        self.win.blit(self.upperTube, self.upperRect)
        self.win.blit(self.bottomTube, self.bottomRect)
        
    def move(self):
        self.bottomRect.right += self.vel
        self.upperRect.right += self.vel



def updateWin():
        win.blit(bg, (0,0))
        player.draw()
        for pipe in pipes:
            pipe.draw()
        pygame.display.update()

player = Bird(
    r'D:\More Python Projects\Games\Flappy Bird\Assets\bird.png', win)
#? Gravity is positive because y axis is inverted in pygame
GRAVITY = 1000
bg = pygame.image.load(r'D:\More Python Projects\Games\Flappy Bird\Assets\bg.jpg')
bg = pygame.transform.smoothscale(bg, (screenWidth, screenHeight))
#bg.convert(win)

start = False
pipes = list()
run = True
while run:
    # ? Setting FPS
    clock.tick(60)

    events = pygame.event.get()
    for event in events:
        # * If cross button is pressed, the window will close
        if event.type == pygame.QUIT:
            run = False
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
        if pipes == []:
            pipes.append(Pipe(win))
        #@ New objects will be appended when the previous ones are 200 pixels away from the right corner
        elif pipes[-1].upperRect.right < 0.7 * screenWidth:
            pipes.append(Pipe(win))
    
        #? Removing the pipes out of screen
        if pipes[0].upperRect.right < 0:
            pipes.pop(0)  
            
        #? Checking for loss
        run = player.checkLoss(run)           
        
    #? Movement of the pipes
    for pipe in pipes:
        pipe.move()

    # ? Movement of the bird
    player.move()

    #todo Updating the window
    updateWin()

pygame.quit()

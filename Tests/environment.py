import pygame
import pygame_widgets


class Game:
    def __init__(self):
        self.screenWidth, self.screenHeight = 800, 600
        self.win = pygame.display.set_mode(
            (self.screenWidth, self.screenHeight))
        pygame.display.set_caption('Flappy Bird')
        pygame.init()
        #? Gravity is positive because y axis is inverted in pygame
        self.GRAVITY = 1000
        self.clock = pygame.time.Clock()

    def mainLoop(self):
        self.run = True
        while self.run:

            # ? Setting FPS
            self.clock.tick(60)

            self.events = pygame.event.get()
            for event in self.events:
                # * If cross button is pressed, the window will close
                if event.type == pygame.QUIT:
                    self.run = False

                #! If the space or mosue is clicked on the screen, jump function will be launched
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        player.jump()


                if event.type == pygame.MOUSEBUTTONDOWN:
                    player.jump()

            # ? Movement of the bird
            player.move()
            #? Checking for loss
            player.checkLoss()

            self.updateWin()

        pygame.quit()

    def updateWin(self):
        self.win.fill((255, 255, 255))
        player.draw()
        pygame.display.update()
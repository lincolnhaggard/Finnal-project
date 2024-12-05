import pygame
import sys
from bird import Bird
class Game:
    def __init__(self,screen,clock,menu):
        self.bird=Bird("img/bird.png")
        self.background=pygame.image.load("img/background.png").convert_alpha()
        self.background=pygame.transform.scale(self.background,(1000,1000))

        self.x_offset=0
        self.y_offset=0


        self.hgsmlr=True
        self.mainloop(screen,clock)
        


    def resizeall(self,screen):
        wdh=screen.get_width()
        hgt=screen.get_height()
        if wdh/2560>hgt/1400:
            self.y_offset=0
            self.x_offset=(wdh/2)-((hgt*2560/1400)/2)
            self.hgsmlr=True
            self.wdh=hgt*2560/1400
        elif wdh/2560<hgt/1400:
            self.x_offset=0
            self.y_offset=(hgt/2)-((wdh*1400/2560)/2)
            hgt=wdh*1400/2560
            self.hgsmlr=False
        else:
            self.x_offset=0
            self.y_offset=0
        
        self.background=pygame.transform.scale(self.background,(wdh,hgt))
        self.bird.resize(self.x_offset,self.y_offset,wdh,hgt)
    def renderall(self,screen):

        screen.blit(self.background,(self.x_offset-2.5,self.y_offset))#layer 1 background

        self.bird.render(screen)#layer 2 bird
        

    def mainloop(self,screen,clock):
        while True:
            for event in pygame.event.get():
                if event.type==pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type==pygame.MOUSEBUTTONUP:
                    self.bird.flap()
                if event.type==pygame.KEYDOWN:
                    if event.key==pygame.K_SPACE:
                        self.bird.flap()
            pygame.display.update()
            clock.tick(120.0)
            self.resizeall(screen)
            self.bird.update()
            self.renderall(screen)

import pygame
import sys
from bird import Bird
from pipe import Pipe
class Game:
    def __init__(self,screen,clock,menu):
        self.bird=Bird("img/bird.png")
        self.background=pygame.image.load("img/background.png").convert_alpha()
        self.background=pygame.transform.scale(self.background,(1000,1000))
        self.side_burn=pygame.image.load("img/side_burn.png").convert_alpha()
        self.side_burn=pygame.transform.scale(self.side_burn,(1000,1000))
        self.pipes=[]
        self.x_offset=0
        self.y_offset=0
        self.SPAWNPIPE = pygame.USEREVENT
        pygame.time.set_timer(self.SPAWNPIPE, int(2200.0*1.5))
        self.score=0
        self.font = pygame.font.SysFont(None,48)
        


        self.resizeall(screen)
        self.mainloop(screen,clock)
        


    def resizeall(self,screen):
        wdh=screen.get_width()
        hgt=screen.get_height()
        self.side_burn=pygame.image.load("img/side_burn.png").convert_alpha()
        if wdh/2560>hgt/1400:
            self.y_offset=0
            self.x_offset=(wdh/2)-((hgt*2560/1400)/2)
            wdh=hgt*2560/1400
            self.side_burn=pygame.transform.scale(self.side_burn,(self.x_offset+5,hgt))
        elif wdh/2560<hgt/1400:
            self.x_offset=0
            self.y_offset=(hgt/2)-((wdh*1400/2560)/2)
            hgt=wdh*1400/2560
            
            self.side_burn=pygame.transform.scale(self.side_burn,(wdh,self.y_offset+5))
        else:
            self.x_offset=0
            self.y_offset=0
        self.hgt=hgt
        self.wdh=wdh
        #theses can be in any order
        self.background=pygame.image.load("img/background.png").convert_alpha()
        self.background=pygame.transform.scale(self.background,(wdh,hgt))
        
        self.bird.resize(self.x_offset,self.y_offset,wdh,hgt)
        for pipe in self.pipes:
            pipe.resize(self.x_offset,self.y_offset,wdh,hgt)
    def renderall(self,screen):
        #the last one renders ontop, probably the bird
        screen.blit(self.background,(self.x_offset,self.y_offset))#layer 1 background
        for pipe in self.pipes:
            pipe.render(screen)#layer 2 pipe
        score_surface=self.font.render(str(int(self.score)),True,(255,255,255))
        score_rect= score_surface.get_rect(center=(202,75))
        screen.blit(score_surface,score_rect)#layer 3 score
        self.bird.render(screen)#layer 4 bird

        #sideburns, last layer for screen resizing
        screen.blit(self.side_burn, (0,0))
        if self.y_offset==0:
            screen.blit(self.side_burn,(self.wdh+self.x_offset,0))
        else:
            screen.blit(self.side_burn,(0,self.hgt+self.y_offset))

        
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
                if event.type==self.SPAWNPIPE:
                    self.pipes.append(Pipe("img/pipe.png",2400,600,True))
                    self.pipes.append(Pipe("img/pipe.png",2700,400,False))
                    self.pipes[-2].resize(self.x_offset,self.y_offset,self.wdh,self.hgt)
                    self.pipes[-1].resize(self.x_offset,self.y_offset,self.wdh,self.hgt)
                if event.type==pygame.VIDEORESIZE:
                    self.resizeall(screen)
            pygame.display.update()
            clock.tick(120.0)
            self.bird.update()
            
            for pipe in self.pipes:
                if pipe.returnscore():
                    self.score+=1
                if pipe.update():
                    self.pipes.remove(pipe)
                    del pipe
                
            self.renderall(screen)
            if self.bird.check_pipe_collide(self.pipes):
                break

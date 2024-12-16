import pygame
import sys
import random
import time
from bird import Bird
from pipe import Pipe
from mine import Mine
class Game:
    def __init__(self,screen,clock,menu):
        self.bird=Bird("img/bird.png")
        self.background=pygame.image.load("img/bgimgs/bg1/base.png").convert_alpha()
        self.background=pygame.transform.scale(self.background,(1000,1000))
        
        self.bglayer=pygame.image.load(f"img/bgimgs/bg1/object.png").convert_alpha()
        self.bglayer=pygame.transform.scale(self.bglayer,(1000,1000))
        self.darkness=pygame.image.load("img/darkness.png").convert_alpha()
        self.darkness=pygame.transform.scale(self.darkness,(1000,1000))
        self.darkdist=-2560
        self.bgoffset=100000
        self.bgoffsets=[]
        for i in range(10):
            self.bgoffsets.append(random.randint(25000,50000)/5000)

        self.side_burn=pygame.image.load("img/side_burn.png").convert_alpha()
        self.side_burn=pygame.transform.scale(self.side_burn,(1000,1000))
        self.pipes=[]
        self.mines=[]

        self.gap=menu.get_gap()
        self.speed=menu.get_speed()
        self.mode=menu.get_mode()

        self.x_offset=0
        self.y_offset=0
        self.SPAWNPIPE = pygame.USEREVENT
        pygame.time.set_timer(self.SPAWNPIPE, int(2200/self.speed))
        self.score=0
        self.font = pygame.font.SysFont(None,48)
        self.score_surface=self.font.render(str(int(self.score)),True,(255,255,255))
        self.score_rect= self.score_surface.get_rect(center=(2560/2,75))
        
        self.yflip=False
        self.xflip=False
        

        self.lastpipe=0

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

        self.background=pygame.image.load("img/bgimgs/bg1/base.png").convert_alpha()
        self.background=pygame.transform.scale(self.background,(wdh,hgt))

        self.darkness=pygame.image.load("img/darkness.png").convert_alpha()
        self.darkness=pygame.transform.scale(self.darkness,(wdh,hgt))

        self.bglayer=pygame.image.load(f"img/bgimgs/bg1/object.png").convert_alpha()
        self.bglayer=pygame.transform.scale(self.bglayer,(wdh/2560*500,hgt/1400*400))

        self.font = pygame.font.SysFont(None,int(150*(wdh/2560)))
        self.score_surface=self.font.render(str(int(self.score)),True,(255,255,255))
        self.bird.resize(self.x_offset,self.y_offset,wdh,hgt)
        for pipe in self.pipes:
            pipe.resize(self.x_offset,self.y_offset,wdh,hgt)
        for mine in self.mines:
            mine.resize(self.x_offset,self.y_offset,wdh,hgt)
        
        
    def renderall(self,screen):
        #the last one renders ontop, probably the bird
        screen.blit(self.background,(self.x_offset,self.y_offset))#layer 1 background
        for i in range(10):
            screen.blit(self.bglayer,(self.x_offset-((self.bgoffset*self.bgoffsets[i])%(2560+500))+2560,self.y_offset+(i*140)))
        for pipe in self.pipes:
            pipe.render(screen)#layer 2 pipe
        for mine in self.mines:
            mine.render(screen)
        screen.blit(self.score_surface,(self.wdh/2560*self.score_rect.x+self.x_offset,self.hgt/1400*self.score_rect.y+self.y_offset))#layer 3 score
        self.bird.render(screen)#layer 4 bird
        if self.mode=="dark":
            screen.blit(self.darkness,(self.x_offset+(self.darkdist*self.wdh/2560),self.y_offset))
            screen.blit(self.score_surface,(self.wdh/2560*self.score_rect.x+self.x_offset,self.hgt/1400*self.score_rect.y+self.y_offset))
        self.bird.render_eye(screen)


        #sideburns, last layer for screen resizing
        screen.blit(self.side_burn, (0,0))
        if self.y_offset==0:
            screen.blit(self.side_burn,(self.wdh+self.x_offset,0))
        else:
            screen.blit(self.side_burn,(0,self.hgt+self.y_offset))
        
        if self.xflip:
            screen.blit(pygame.transform.flip(screen, True, False), (0, 0))
        if self.yflip:
            screen.blit(pygame.transform.flip(screen,False,True), (0,0))

    def spawnpipe(self):
        dificulty=self.score*5
        
        minpipedist=200-dificulty#has to be less than 450
        if minpipedist<100:minpipedist=100
        height=random.randint(minpipedist,1400-self.gap-minpipedist)

        if dificulty>100:
            if abs(self.lastpipe-height)<=dificulty*2:
                height=1400-height
        self.lastpipe=height
        gap=self.gap-dificulty
        if gap<100:gap=100
        if self.mode=="reverse" and random.randint(1,2)==1:
            self.pipes.append(Pipe("img/pipe.png",2700,gap,False,True))
            self.pipes[-1].resize(self.x_offset,self.y_offset,self.wdh,self.hgt)
            return None
        if self.mode=="flying":
            mv=random.choice((-3,3))
            self.pipes.append(Pipe("img/pipe.png",2700,height,True,flying=mv))
            self.pipes.append(Pipe("img/pipe.png",2700,height+gap,False,flying=mv))
            self.pipes[-2].resize(self.x_offset,self.y_offset,self.wdh,self.hgt)
            self.pipes[-1].resize(self.x_offset,self.y_offset,self.wdh,self.hgt)
            return None
        self.pipes.append(Pipe("img/pipe.png",2700,height,True))
        self.pipes.append(Pipe("img/pipe.png",2700,height+gap,False))
        self.pipes[-2].resize(self.x_offset,self.y_offset,self.wdh,self.hgt)
        self.pipes[-1].resize(self.x_offset,self.y_offset,self.wdh,self.hgt)
        if self.mode=="bomb" and random.randint(1,2)==1:
            self.spawnmine(height,gap)

    def spawnmine(self,height,gap):
        for i in range(random.randint(1,3)):
            self.mines.append(Mine(2700+random.randint(300,1000),random.randint(0,int(height)+100)))
            self.mines[-1].resize(self.x_offset,self.y_offset,self.wdh,self.hgt)
        for i in range(random.randint(1,2)):
            self.mines.append(Mine(2700+random.randint(300,1000),random.randint(height+gap-100,1400)))
            self.mines[-1].resize(self.x_offset,self.y_offset,self.wdh,self.hgt)
        
    def mainloop(self,screen,clock):
        lastime=time.time()
        lastframe=time.time()
        while True:
            
            if time.time()-lastime>1.0/60:
                lastime=time.time()
                wave=False
                if self.mode=="wave":
                    wave=True
                for event in pygame.event.get():
                    if event.type==pygame.QUIT:
                        pygame.quit()
                        sys.exit()
                    if event.type==pygame.MOUSEBUTTONUP:
                        self.bird.flap(wave)
                    if event.type==pygame.KEYDOWN:
                        if event.key==pygame.K_SPACE:
                            self.bird.flap(wave)
                    if event.type==self.SPAWNPIPE:

                        self.spawnpipe()
                        
                        



                    if event.type==pygame.VIDEORESIZE:
                        self.resizeall(screen)

                
                self.bgoffset+=self.speed
                if self.darkdist<0:
                    self.darkdist+=self.speed
                else:
                    self.darkdist=0
                gravity=False
                if self.mode=="gravity":
                    gravity=True
                pong=False
                if self.mode=="pong":
                    pong=True
                self.bird.update(gravity=gravity,pong=pong,wave=wave)

                for pipe in self.pipes:
                    if pipe.returnscore():
                        self.score+=1
                        self.score_surface=self.font.render(str(int(self.score)),True,(255,255,255))
                        if self.mode=="flip":
                            if random.randint(1,2)==1:
                                if self.xflip:self.xflip=False
                                else:self.xflip=True
                            else:
                                if self.yflip:self.yflip=False
                                else:self.yflip=True
                    pipe.update(self.speed)
                        
                for pipe in self.pipes:
                    if pipe.check():
                        self.pipes.remove(pipe)
                        del pipe
                for mine in self.mines:
                    mine.update(self.speed)
                for mine in self.mines:
                    if mine.check():
                        self.mines.remove(mine)
                        del mine

                rvsd=False
                if self.mode=="reverse":
                    rvsd=True
                portal=False
                if self.mode=="portal":
                    portal=True
                self.renderall(screen)
                if self.bird.check_pipe_collide(self.pipes,rvsd,portal) or self.bird.check_mine_collide(self.mines):
                    break
            if time.time()-lastframe>1.0/60:
                pygame.display.update()
            clock.tick()
            
            

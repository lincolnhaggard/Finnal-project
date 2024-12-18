import pygame
import sys
import random
import time
from bird import Bird
from pipe import Pipe
from mine import Mine


class Game:


    def __init__(self,screen,clock,menu):
        """there are some variables not defined in the __init__ function
           they are instead defiened in the resize all function:
            background
            darkness
            bglayer
            side_burn
            x_offset
            y_offset
            wdh (resized width)
            hgt (resized height)
           """
        self.bird=Bird()
        
        self.darkdist=-2560 #the darknessed staring pos from the right side of the screen

        self.bgoffset=100000 #this is for the cloud background objects
        self.bgoffsets=[]#this controls how fast they move
        for i in range(10):
            self.bgoffsets.append(random.randint(25000,50000)/5000)
        self.pipes=[]
        self.mines=[]
        #retrives user inputed modes and gap and speed
        self.gap=menu.get_gap()
        self.speed=menu.get_speed()
        self.mode=menu.get_mode()

        self.SPAWNPIPE = pygame.USEREVENT
        pygame.time.set_timer(self.SPAWNPIPE, int(2200/self.speed))
        #the score rect needs to be defined here as it is not defined in resize all
        self.score=0
        self.font = pygame.font.SysFont(None,48)
        self.score_surface=self.font.render(str(int(self.score)),True,(255,255,255))
        self.score_rect= self.score_surface.get_rect(center=(2560/2,75))
        #if these are true flips the entire screen in the given direction
        self.yflip=False
        self.xflip=False
        #used to make pipes spawn farther apart with high enough score
        self.lastpipe=0
        self.resizeall(screen)
        self.mainloop(screen,clock)

    def resizeall(self,screen):
        #this code gets the size of the screen
        #it also makes sure that everything stays
        #in the right ratio, picking the smallest one
        wdh=screen.get_width()
        hgt=screen.get_height()
        #side_burns are to prevent bluring if the window size does not match 2560 by 1400
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
        #background
        self.background=pygame.image.load("img/bgimgs/bg1/base.png").convert_alpha()
        self.background=pygame.transform.scale(self.background,(wdh,hgt))
        #darkness
        self.darkness=pygame.image.load("img/darkness.png").convert_alpha()
        self.darkness=pygame.transform.scale(self.darkness,(wdh,hgt))
        #clouds
        self.bglayer=pygame.image.load(f"img/bgimgs/bg1/object.png").convert_alpha()
        self.bglayer=pygame.transform.scale(self.bglayer,(wdh/2560*500,hgt/1400*400))
        #score text
        self.font = pygame.font.SysFont(None,int(150*(wdh/2560)))
        self.score_surface=self.font.render(str(int(self.score)),True,(255,255,255))
        self.bird.resize(self.x_offset,self.y_offset,wdh,hgt)
        #pipes
        for pipe in self.pipes:
            pipe.resize(self.x_offset,self.y_offset,wdh,hgt)
        #mines
        for mine in self.mines:
            mine.resize(self.x_offset,self.y_offset,wdh,hgt)
        
        
    def renderall(self,screen):
        #the last one renders ontop, usually the side_burns
        screen.blit(self.background,(self.x_offset,self.y_offset))#layer 1/8 background
        for i in range(10):#layer 2/8 clouds
            screen.blit(self.bglayer,(self.x_offset-((self.bgoffset*self.bgoffsets[i])%(2560+500))+2560,self.y_offset+(i*140)))
        for mine in self.mines:#layer 3/8 mines
            mine.render(screen)
        for pipe in self.pipes:#layer 4/8 pipes
            pipe.render(screen)
        self.bird.render(screen)#layer 5/8 bird
        if self.mode=="dark":
            #layer 6/8 darkness (optional)
            screen.blit(self.darkness,(self.x_offset+(self.darkdist*self.wdh/2560),self.y_offset))
        #layer 7/8 score text so that it is over the darkness
        screen.blit(self.score_surface,(self.wdh/2560*self.score_rect.x+self.x_offset,self.hgt/1400*self.score_rect.y+self.y_offset))
        self.bird.render_eye(screen)#layer 8/8 birds eye
        #sideburns, last layer for screen resizing
        screen.blit(self.side_burn, (0,0))
        if self.y_offset==0:
            screen.blit(self.side_burn,(self.wdh+self.x_offset,0))
        else:
            screen.blit(self.side_burn,(0,self.hgt+self.y_offset))
        #flip the entire screen
        if self.xflip:
            screen.blit(pygame.transform.flip(screen, True, False), (0, 0))
        if self.yflip:
            screen.blit(pygame.transform.flip(screen,False,True), (0,0))

    def spawnpipe(self):
        dificulty=self.score*5
        #minpipedist is how far away a pipe has to be from the edges of the screen
        minpipedist=200-dificulty#has to be less than 450
        if minpipedist<100:minpipedist=100#makes the min 100
        #height is the distance from the top of the screen to
        #the bottom of the top pipe
        height=random.randint(minpipedist,1400-self.gap-minpipedist)
        if dificulty>100:
            #flips the pipe if it was too close the last pipe
            if abs(self.lastpipe-height)<=dificulty*2:
                height=1400-height
        self.lastpipe=height
        #gap is space inbetween the two pipes
        gap=self.gap-dificulty#shrinks the gap overtime
        if gap<100:gap=100#makes the min gap
        if self.mode=="reverse" and random.randint(1,2)==1: #two gaps one pipe
            self.pipes.append(Pipe("img/pipe.png",2700,gap,False,True))
            self.pipes[-1].resize(self.x_offset,self.y_offset,self.wdh,self.hgt)
        
        else:#one gap two pipes
            if self.mode=="flying": #moveing pipes
                mv=random.choice((-3,3))
            else:
                mv=0
            self.pipes.append(Pipe("img/pipe.png",2700,height,True,flying=mv))
            self.pipes.append(Pipe("img/pipe.png",2700,height+gap,False,flying=mv))
            self.pipes[-2].resize(self.x_offset,self.y_offset,self.wdh,self.hgt)
            self.pipes[-1].resize(self.x_offset,self.y_offset,self.wdh,self.hgt)
            #mines
            if self.mode=="bomb" and random.randint(1,2)==1:
                self.spawnmine(height,gap)

    def spawnmine(self,height,gap):
        #simpler version of the spawn pipe function
        for i in range(random.randint(1,3)):#spawns on top half of the screen
            self.mines.append(Mine(2700+random.randint(300,1000),random.randint(0,int(height)+100)))
            self.mines[-1].resize(self.x_offset,self.y_offset,self.wdh,self.hgt)
        for i in range(random.randint(1,2)):#spawns on bottom half of the screen
            self.mines.append(Mine(2700+random.randint(300,1000),random.randint(height+gap-100,1400)))
            self.mines[-1].resize(self.x_offset,self.y_offset,self.wdh,self.hgt)
        
    def mainloop(self,screen,clock):
        lastime=time.time()#last time the game was updated
        lastframe=time.time()#last time the game was rendered
        while True:
            if time.time()-lastime>1.0/60:#updates the game 60 times a second
                lastime=time.time()
                #modes for flapping the bird
                wave=False
                if self.mode=="wave":
                    wave=True
                for event in pygame.event.get():
                    if event.type==pygame.QUIT:#required
                        pygame.quit()
                        sys.exit()

                    #allows the user to press space or mouse1 to move the bird
                    if event.type==pygame.MOUSEBUTTONUP:
                        self.bird.flap(wave)
                    if event.type==pygame.KEYDOWN:
                        if event.key==pygame.K_SPACE:
                            self.bird.flap(wave)

                    if event.type==self.SPAWNPIPE:
                        self.spawnpipe()

                    if event.type==pygame.VIDEORESIZE:
                        self.resizeall(screen)
                    
                self.bgoffset+=self.speed#moves the background
                #moves the darkness
                if self.darkdist<0:
                    self.darkdist+=self.speed
                else:
                    self.darkdist=0
                #modes for moving the bird
                gravity=False
                if self.mode=="gravity":
                    gravity=True
                pong=False
                if self.mode=="pong":
                    pong=True
                self.bird.update(gravity=gravity,pong=pong,wave=wave)#moves the bird
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
                    pipe.update(self.speed)#moves pipe
                #move pipe and delete pipes have to be sperate to prevent the pipes from getting offset
                for pipe in self.pipes:
                    if pipe.check():
                        self.pipes.remove(pipe)
                        del pipe
                for mine in self.mines:
                    mine.update(self.speed)
                #the same applies for the mide (move and delete have to be sperate to prevent the mines from getting offset)
                for mine in self.mines:
                    if mine.check():
                        self.mines.remove(mine)
                        del mine

                #modes for checking collisions
                rvsd=False
                if self.mode=="reverse":
                    rvsd=True
                portal=False
                if self.mode=="portal":
                    portal=True
                if self.bird.check_pipe_collide(self.pipes,rvsd,portal) or self.bird.check_mine_collide(self.mines):
                    break
                self.renderall(screen)
                
            if time.time()-lastframe>1.0/60:#renders the game 60 times a second (in an attempt to prevent screen tearing)
                pygame.display.update()
            clock.tick()
            
            

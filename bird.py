import pygame

class Bird:
    def __init__(self):
        #the birds size is 153 by 102
        """there are some variables not defined in the __init__ function
           they are instead defiened in the resize function:
            bird_eye
            x_offset
            y_offset
            wdh (resized width)
            hgt (resized height)
           """
        #bird_rect does not get changed in resize
        self.bird=pygame.image.load("img/bird.png").convert_alpha()
        self.bird=pygame.transform.scale(self.bird,(153,102))
        self.bird_rect=self.bird.get_rect(center = (280,450))
        #vos is up and down, xvos is back and forth
        self.vos=-10
        self.xvos=3
    
    def render(self,screen):
        self.rotated_bird=pygame.transform.rotozoom(self.bird, -self.vos * 3, 1)#rotates bird acording to volosity
        screen.blit(self.rotated_bird, (self.bird_rect.x*self.wdh+self.x_offset,self.bird_rect.y*self.hgt+self.y_offset))
    
    def render_eye(self,screen):
        #seperate from render because it does not need to be rendered all the time
        screen.blit(pygame.transform.rotozoom(self.bird_eye, -self.vos * 3, 1), (self.bird_rect.x*self.wdh+self.x_offset,self.bird_rect.y*self.hgt+self.y_offset))
    
    def update(self,gravity,pong,wave):
        if not wave:#wave ignores gravity
            self.vos+=0.4
            if gravity:#gravity(moon mode) counteracts half of gravity
                self.vos-=0.2
        self.bird_rect.centery+=self.vos#updates the position of the bird
        if pong:#moves the bird back and forth
            self.bird_rect.x+=self.xvos
            if self.bird_rect.x<51*1.5 or self.bird_rect.x>1280-(34*1.5):
                self.xvos*=-1

    def flap(self,wave):
        if wave:#flips movement if wave mode
            self.vos*=-1
        else:#make sure to set vos when flapping and not add it
            self.vos=-10
    
    def resize(self,x_offset,y_offset,wdh,hgt):
        #This code makes sure the bird is rendered apropriatly to window size
        self.bird=pygame.image.load("img/bird.png").convert_alpha()
        self.bird=pygame.transform.scale(self.bird,(wdh/2560*153,hgt/1400*102))
        self.bird_eye=pygame.image.load("img/bird_eye.png").convert_alpha()
        self.bird_eye=pygame.transform.scale(self.bird_eye,(wdh/2560*153,hgt/1400*102))

        self.x_offset=x_offset
        self.y_offset=y_offset
        self.wdh=wdh/2560#saves wdh(width) and hgt(height) as ratios
        self.hgt=hgt/1400
    
    def check_pipe_collide(self,pipes,reversed=False,portal=False):
        collided=False
        for pipe in pipes:
            #checks collision with each part of the pipe
            if self.bird_rect.colliderect(pipe.pipe_rect) or self.bird_rect.colliderect(pipe.mid_rect) or (pipe.reversed and self.bird_rect.colliderect(pipe.bottom_rect)):
                collided=True
        #wraps around the screen if portal mode is active otherwise dies
        if portal:
            if self.bird_rect.bottom<-40:
                self.bird_rect.top=1390
            if self.bird_rect.top>1440:
                self.bird_rect.bottom=10
        elif self.bird_rect.top<-40 or self.bird_rect.bottom>1440:
            collided=True
        return collided
    
    def check_mine_collide(self,mines):
        #this is a seperate function from check_pipe_collide because it is not called in every run
        collided=False
        for mine in mines:
            if self.bird_rect.colliderect(mine.mine_rect):
                collided=True
        return collided
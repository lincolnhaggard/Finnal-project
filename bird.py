import pygame

class Bird:
    def __init__(self,bird_img):
        self.bird=pygame.image.load(bird_img).convert_alpha()
        self.bird_eye=pygame.image.load("img/bird_eye.png").convert_alpha()
        self.bird_img=bird_img
        self.bird_size=(51*3,34*3)
        self.bird=pygame.transform.scale(self.bird,self.bird_size)
        self.bird_eye=pygame.transform.scale(self.bird_eye,self.bird_size)
        
        self.bird_rect=self.bird.get_rect(center = (280,450))
        self.vos=-10
        self.xvos=3
    def render(self,screen):
        self.rotated_bird=self.rotate_bird()
        screen.blit(self.rotated_bird, (self.bird_rect.x*self.wdh+self.x_offset,self.bird_rect.y*self.hgt+self.y_offset))
    def render_eye(self,screen):
        screen.blit(pygame.transform.rotozoom(self.bird_eye, -self.vos * 3, 1), (self.bird_rect.x*self.wdh+self.x_offset,self.bird_rect.y*self.hgt+self.y_offset))
    def update(self,gravity,pong,wave):
        if not wave:
            
            self.vos+=0.4
            if gravity:
                self.vos-=0.2
        self.bird_rect.centery+=self.vos
        if pong:
            self.bird_rect.x+=self.xvos
            if self.bird_rect.x<51*1.5 or self.bird_rect.x>1280-(34*1.5):
                self.xvos*=-1
    def rotate_bird(self):
        new_bird=pygame.transform.rotozoom(self.bird, -self.vos * 3, 1)
        return new_bird
    def flap(self,wave):
        if wave:
            self.vos*=-1
        else:
            self.vos=-10
    def resize(self,x_offset,y_offset,wdh,hgt):
        self.x_offset=x_offset
        self.y_offset=y_offset
        self.bird=pygame.image.load(self.bird_img).convert_alpha()
        self.bird=pygame.transform.scale(self.bird,(wdh/2560*self.bird_size[0],hgt/1400*self.bird_size[1]))
        self.bird_eye=pygame.image.load("img/bird_eye.png").convert_alpha()
        self.bird_eye=pygame.transform.scale(self.bird_eye,(wdh/2560*self.bird_size[0],hgt/1400*self.bird_size[1]))
        self.wdh=wdh/2560
        self.hgt=hgt/1400
    def check_pipe_collide(self,pipes,reversed=False,portal=False):
        collided=False
        for pipe in pipes:
            if self.bird_rect.colliderect(pipe.pipe_rect) or self.bird_rect.colliderect(pipe.mid_rect) or (pipe.reversed and self.bird_rect.colliderect(pipe.bottom_rect)):
                collided=True
        if portal:
            if self.bird_rect.bottom<-40:
                self.bird_rect.top=1390
            if self.bird_rect.top>1440:
                self.bird_rect.bottom=10
        elif self.bird_rect.top<-40 or self.bird_rect.bottom>1440:
            collided=True
        return collided
    def check_mine_collide(self,mines):
        collided=False
        for mine in mines:
            if self.bird_rect.colliderect(mine.mine_rect):
                collided=True
        return collided
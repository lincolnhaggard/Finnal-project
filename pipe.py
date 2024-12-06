import pygame
class Pipe:
    def __init__(self,pipe_img,x,y):
        #add variable length
        self.pipe=pygame.image.load(pipe_img).convert_alpha()
        self.pipe_img=pipe_img
        self.pipe_size=(80*3,438*3)

        self.pipe_rect=self.pipe.get_rect(center=(x,y))
    def update(self):
        self.pipe_rect.centerx-=4
        if self.pipe_rect.centerx<-140:
            return True
        return False

    def render(self,screen):
        screen.blit(self.pipe, (self.pipe_rect.x*self.wdh+self.x_offset,self.pipe_rect.y*self.hgt+self.y_offset))

    def resize(self,x_offset,y_offset,wdh,hgt):
        self.x_offset=x_offset
        self.y_offset=y_offset
        self.pipe=pygame.image.load(self.pipe_img).convert_alpha()
        self.pipe=pygame.transform.scale(self.pipe,(wdh/2560*80*3,hgt/1400*438*3))
        self.wdh=wdh/2560
        self.hgt=hgt/1400
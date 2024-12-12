import pygame
class Pipe:
    def __init__(self,pipe_img,x,y,top):
        #add variable length
        self.pipe=pygame.image.load(pipe_img).convert_alpha()
        self.pipe_img=pipe_img
        self.pipe_size=(80*3,438*3)
        self.pipe=pygame.transform.scale(self.pipe,(80*3,438*3))
        self.pipe=pygame.transform.flip(self.pipe,False,True)
        self.pipe_rect=self.pipe.get_rect(x=x,y=y)
        if top:
            self.pipe_rect.y-=self.pipe_size[1]
        self.scored=False
        self.top=top
    def update(self,speed):
        self.pipe_rect.centerx-=8*speed
        
    def check(self):
        if self.pipe_rect.centerx<-140:
            return True
        return False

    def render(self,screen):
        screen.blit(self.pipe, (round(self.pipe_rect.x*self.wdh+self.x_offset,2),round(self.pipe_rect.y*self.hgt+self.y_offset,2)))

    def resize(self,x_offset,y_offset,wdh,hgt):
        self.x_offset=x_offset
        self.y_offset=y_offset
        self.pipe=pygame.image.load(self.pipe_img).convert_alpha()
        self.pipe=pygame.transform.scale(self.pipe,(wdh/2560*80*3,hgt/1400*438*3))
        if self.top:
            self.pipe=pygame.transform.flip(self.pipe,False,True)
        self.wdh=wdh/2560
        self.hgt=hgt/1400
    
    def returnscore(self):
        if not self.scored and not self.top:
            if self.pipe_rect.centerx<=280:
                self.scored=True
                return True
        return False
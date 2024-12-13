import pygame
class Pipe:
    def __init__(self,pipe_img,x,y,top):
        #add variable length
        self.top=pygame.image.load("img/pipe_top.png").convert_alpha()
        self.mid=pygame.image.load("img/pipe_mid.png").convert_alpha()
        self.pipe_img=pipe_img
        self.pipe_size=(80*3,438*3)
        self.top=pygame.transform.scale(self.top,(80*3,43*3))
        
        self.pipe_rect=self.top.get_rect(x=x,y=y)
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
        screen.blit(self.top, (round(self.pipe_rect.x*self.wdh+self.x_offset,2),round(self.pipe_rect.y*self.hgt+self.y_offset,2)))

    def resize(self,x_offset,y_offset,wdh,hgt):
        self.x_offset=x_offset
        self.y_offset=y_offset
        self.top=pygame.image.load("img/pipe_top.png").convert_alpha()
        self.top=pygame.transform.scale(self.top,(wdh/2560*80*3,hgt/1400*43*3))
        if self.top:
            self.top=pygame.transform.flip(self.top,False,True)
        self.wdh=wdh/2560
        self.hgt=hgt/1400
    
    def returnscore(self):
        if not self.scored and not self.top:
            if self.pipe_rect.centerx<=280:
                self.scored=True
                return True
        return False
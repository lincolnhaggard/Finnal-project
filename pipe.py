import pygame
class Pipe:
    def __init__(self,pipe_img,x,y,ontop,reversed=False):
        #add variable length
        self.top=pygame.image.load("img/pipe_top.png").convert_alpha()
        self.mid=pygame.image.load("img/pipe_mid.png").convert_alpha()
        self.pipe_img=pipe_img
        self.pipe_size=(80*3,43*3)
        self.top=pygame.transform.scale(self.top,(80*3,43*3))
        
        if reversed:
            gap=y
            self.bottom=pygame.image.load("img/pipe_top.png")
            self.bottom=pygame.transform.scale(self.bottom,(80*3,43*3))
            self.mid=pygame.transform.scale(self.mid,(80*3,1400-(gap*4)-50))
            self.mid_rect=self.mid.get_rect(x=x,y=700)
            self.mid_rect.centery=700
            self.pipe_rect=self.top.get_rect(x=x,y=y)
            self.pipe_rect.centery=self.mid_rect.top
            self.bottom_rect=self.bottom.get_rect(x=x,y=y)
            self.bottom_rect.centery=self.mid_rect.bottom
        else:
            self.pipe_rect=self.top.get_rect(x=x,y=y)
            if ontop:
                self.pipe_rect.y-=self.pipe_size[1]
            if ontop:
                self.mid=pygame.transform.scale(self.mid,(80*3,abs(self.pipe_rect.top+100)))
                self.mid_rect=self.mid.get_rect(x=x,y=-50)
            else:
                self.mid=pygame.transform.scale(self.mid,(80*3,1400-self.pipe_rect.bottom+100))
                self.mid_rect=self.mid.get_rect(x=x,y=self.pipe_rect.bottom-50)
        self.scored=False
        self.ontop=ontop
    def update(self,speed):
        self.pipe_rect.centerx-=8*speed
        self.mid_rect.centerx-=8*speed
        
    def check(self):
        if self.pipe_rect.centerx<-140:
            return True
        return False

    def render(self,screen):
        screen.blit(self.mid, (round(self.mid_rect.x*self.wdh+self.x_offset,2),round(self.mid_rect.y*self.hgt+self.y_offset,2)))
        screen.blit(self.top, (round(self.pipe_rect.x*self.wdh+self.x_offset,2),round(self.pipe_rect.y*self.hgt+self.y_offset,2)))
        

    def resize(self,x_offset,y_offset,wdh,hgt):
        self.x_offset=x_offset
        self.y_offset=y_offset
        self.top=pygame.image.load("img/pipe_top.png").convert_alpha()
        self.mid=pygame.image.load("img/pipe_mid.png").convert_alpha()
        self.top=pygame.transform.scale(self.top,(wdh/2560*80*3,hgt/1400*43*3))
        if self.ontop:
            self.mid=pygame.transform.scale(self.mid,(wdh/2560*80*3,hgt/1400*abs(self.pipe_rect.top+100)))
        else:
            self.mid=pygame.transform.scale(self.mid,(wdh/2560*80*3,hgt/1400*(1400-self.pipe_rect.bottom+100)))
        self.wdh=wdh/2560
        self.hgt=hgt/1400
    
    def returnscore(self):
        if not self.scored and not self.ontop:
            if self.pipe_rect.centerx<=280:
                self.scored=True
                return True
        return False
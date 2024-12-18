import pygame
import random
class Pipe:
    def __init__(self,pipe_img,x,y,ontop,reversed=False,flying=False):
        #pipe size is 240 by 129
        self.top=pygame.image.load("img/pipe_top.png").convert_alpha()
        self.mid=pygame.image.load("img/pipe_mid.png").convert_alpha()

        self.top=pygame.transform.scale(self.top,(240,129))
        self.reversed=reversed
        self.flying=flying
        
        if reversed:#makes the pipe double sided
            self.gap=y
            self.bottom=pygame.image.load("img/pipe_top.png")
            self.bottom=pygame.transform.scale(self.bottom,(240,129))
            self.mid=pygame.transform.scale(self.mid,(240,1400-(self.gap*2)-50))
            self.mid_rect=self.mid.get_rect(x=x,y=700)
            self.mid_rect.centery=700
            self.pipe_rect=self.top.get_rect(x=x,y=y)
            self.pipe_rect.centery=self.mid_rect.top
            self.bottom_rect=self.bottom.get_rect(x=x,y=0)
            self.bottom_rect.centery=1400-self.gap

        else:
            if self.flying!=False:#makes pipes move
                self.mv=flying
                self.offset=0

            self.pipe_rect=self.top.get_rect(x=x,y=y)
            if ontop:
                self.pipe_rect.y-=129
            if ontop:
                self.mid=pygame.transform.scale(self.mid,(240,abs(self.pipe_rect.top+100)))
                self.mid_rect=self.mid.get_rect(x=x,y=-50)
            else:
                self.mid=pygame.transform.scale(self.mid,(240,1400-self.pipe_rect.bottom+100))
                self.mid_rect=self.mid.get_rect(x=x,y=self.pipe_rect.bottom-50)

        self.scored=False#so that score is not counted more than once
        self.ontop=ontop#True if connected to the top side of the screen, False otherwise
    
    def update(self,speed):#moves the pipe
        self.pipe_rect.centerx-=8*speed
        self.mid_rect.centerx-=8*speed
        if self.reversed:
            self.bottom_rect.centerx-=8*speed
        if self.flying!=False:
            self.pipe_rect.y+=self.mv*speed
            if self.ontop:
                self.mid_rect.bottom=self.pipe_rect.top+50
            else:
                self.mid_rect.y=self.pipe_rect.bottom-50
            self.offset+=self.mv*speed
            if self.offset>200 or self.offset<-200:
                self.mv*=-1

    def check(self):#used to delete the pipe
        if self.pipe_rect.centerx<-140:
            return True
        return False

    def render(self,screen):
        screen.blit(self.mid, (round(self.mid_rect.x*self.wdh+self.x_offset,2),round(self.mid_rect.y*self.hgt+self.y_offset,2)))
        screen.blit(self.top, (round(self.pipe_rect.x*self.wdh+self.x_offset,2),round(self.pipe_rect.y*self.hgt+self.y_offset,2)))
        if self.reversed:
            screen.blit(self.bottom, (round(self.bottom_rect.x*self.wdh+self.x_offset,2),round(self.bottom_rect.y*self.hgt+self.y_offset,2)))
        

    def resize(self,x_offset,y_offset,wdh,hgt):
        #makes sure the pipe scales with window size
        self.top=pygame.image.load("img/pipe_top.png").convert_alpha()
        self.mid=pygame.image.load("img/pipe_mid.png").convert_alpha()
        self.top=pygame.transform.scale(self.top,(wdh/2560*240,hgt/1400*129))
        if self.reversed:#render the bottom if the pipe is reveres
            self.bottom=pygame.image.load("img/pipe_top.png").convert_alpha()
            self.bottom=pygame.transform.scale(self.bottom,(wdh/2560*240,hgt/1400*129))
            self.mid=pygame.transform.scale(self.mid,(wdh/2560*240,hgt/1400*(1400-(self.gap*2)-50)))
        elif self.flying!=False:#makes the pipe longer if flying
            if self.ontop:
                self.mid=pygame.transform.scale(self.mid,(wdh/2560*240,hgt/1400*abs(self.pipe_rect.top+300)))
                self.mid_rect.bottom=self.pipe_rect.top+50
            else:
                self.mid=pygame.transform.scale(self.mid,(wdh/2560*240,hgt/1400*(1400-self.pipe_rect.bottom+300)))
        else:#normal pipe rendering

            if self.ontop:
                self.mid=pygame.transform.scale(self.mid,(wdh/2560*240,hgt/1400*abs(self.pipe_rect.top+100)))
            else:
                self.mid=pygame.transform.scale(self.mid,(wdh/2560*240,hgt/1400*(1400-self.pipe_rect.bottom+100)))
        
        self.x_offset=x_offset
        self.y_offset=y_offset
        self.wdh=wdh/2560
        self.hgt=hgt/1400
    
    def returnscore(self):
        if not self.scored and not self.ontop:#only the bottom pipe scores
            if self.pipe_rect.centerx<=280:
                self.scored=True
                return True
        return False
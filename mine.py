import pygame
import random

class Mine:
    #simpler version of pipe
    def __init__(self,x,y):
        #mine size is 55.75 by 56.5
        """there are some variables not defined in the __init__ function
           they are instead defiened in the resize function:
            x_offset
            y_offset
            wdh (resized width)
            hgt (resized height)
           """

        self.mine=pygame.image.load("img/mine.png").convert_alpha()
        self.mine=pygame.transform.scale(self.mine, (57.75,56.5))
        self.mine_rect=self.mine.get_rect(center= (x,y))

        self.x=x
        self.y=y

    def resize(self,x_offset,y_offset,wdh,hgt):
        #makes sure the mine is rendered apropriatly
        self.x_offset=x_offset
        self.y_offset=y_offset

        self.mine=pygame.image.load("img/mine.png").convert_alpha()
        self.mine=pygame.transform.scale(self.mine,(wdh/2560*223/3,hgt/1400*226/3))

        self.wdh=wdh/2560#save wdh(width) and hgt(height) as ratios
        self.hgt=hgt/1400

    def render(self,screen):
        screen.blit(self.mine, (round(self.mine_rect.x*self.wdh+self.x_offset,2),round(self.mine_rect.y*self.hgt+self.y_offset,2)))
    
    def update(self,speed):
        self.mine_rect.x-=8*speed
    
    def check(self):#deletes when past the left side of the screen
        if self.mine_rect.centerx<-140:
            return True
        return False
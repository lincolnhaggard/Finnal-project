import pygame
import random
class Mine:
    def __init__(self,x,y):
        self.mine=pygame.image.load("img/mine.png").convert_alpha()
        self.mine=pygame.transform.scale(self.mine, (223/4,226/4))
        self.mine_rect=self.mine.get_rect(center= (x,y))
        self.x=x
        self.y=y
    def resize(self,x_offset,y_offset,wdh,hgt):
        self.x_offset=x_offset
        self.y_offset=y_offset
        self.mine=pygame.image.load("img/mine.png").convert_alpha()
        self.mine=pygame.transform.scale(self.mine,(wdh/2560*223/3,hgt/1400*226/3))
        self.wdh=wdh/2560
        self.hgt=hgt/1400
    def render(self,screen):
        screen.blit(self.mine, (round(self.mine_rect.x*self.wdh+self.x_offset,2),round(self.mine_rect.y*self.hgt+self.y_offset,2)))
    def update(self,speed):
        self.mine_rect.x-=8*speed
    def check(self):
        if self.mine_rect.centerx<-140:
            return True
        return False
import pygame

class Bird:
    def __init__(self,bird_img):
        self.bird=pygame.image.load(bird_img).convert_alpha()
        self.bird=pygame.transform.scale(self.bird,(51,34))
        self.bird_rect=self.bird.get_rect(center = (70,180))
        self.vos=0
        self.y=0
    def render(self,screen):
        screen.blit(self.rotated_bird, (self.bird_rect.x+self.x_offset,self.bird_rect.y+self.y_offset))
    def update(self):
        self.vos+=0.049
        self.bird_rect.centery+=self.vos
        self.rotated_bird=self.rotate_bird()
    def rotate_bird(self):
        new_bird=pygame.transform.rotozoom(self.bird, -self.vos * 3, 1)
        return new_bird
    def flap(self):
        self.vos=-2.5
    def resize(self,x_offset,y_offset,wdh,hgt):
        self.x_offset=x_offset
        self.y_offset=y_offset
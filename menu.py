import pygame
import sys
class Menu:
    def __init__(self,screen,clock):
        self.menu=pygame.image.load("img/menu.png").convert_alpha()
        self.menu=pygame.transform.scale(self.menu,(500,500))


        self.mainloop(screen,clock)
    def mainloop(self,screen,clock):
        exitmenu=False
        while not exitmenu:
            for event in pygame.event.get():
                if event.type==pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type==pygame.MOUSEBUTTONUP:
                    if self.menu.get_rect().collidepoint(pygame.mouse.get_pos()):
                        exitmenu=True
            screen.blit(self.menu,(250,250))
            pygame.display.update()
            clock.tick(120.0)
        
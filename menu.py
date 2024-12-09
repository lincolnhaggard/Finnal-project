import pygame
import sys
class Menu:
    def __init__(self,screen,clock,game=False):
        self.menu=pygame.image.load("img/menu.png").convert_alpha()
        self.menu=pygame.transform.scale(self.menu,(500,500))
        self.menu_rect=self.menu.get_rect(center=(2560/2,700))

        self.resizeall(screen)
        self.mainloop(screen,clock,game)
    def resizeall(self,screen):
        wdh=screen.get_width()
        hgt=screen.get_height()
        self.side_burn=pygame.image.load("img/side_burn.png").convert_alpha()
        if wdh/2560>hgt/1400:
            self.y_offset=0
            self.x_offset=(wdh/2)-((hgt*2560/1400)/2)
            wdh=hgt*2560/1400
            self.side_burn=pygame.transform.scale(self.side_burn,(self.x_offset+5,hgt))
        elif wdh/2560<hgt/1400:
            self.x_offset=0
            self.y_offset=(hgt/2)-((wdh*1400/2560)/2)
            hgt=wdh*1400/2560
            
            self.side_burn=pygame.transform.scale(self.side_burn,(wdh,self.y_offset+5))
        else:
            self.x_offset=0
            self.y_offset=0
        self.hgt=hgt
        self.wdh=wdh
        self.menu=pygame.image.load("img/menu.png").convert_alpha()
        self.menu=pygame.transform.scale(self.menu,(wdh/2560*500,hgt/1400*500))
        self.menu_rect=self.menu.get_rect(center=(2560/2,700))
    

    def renderall(self,screen):
        self.menu_rect.centerx=2560/2*(self.wdh/2560)+self.x_offset
        self.menu_rect.centery=1400/2*(self.hgt/1400)+self.y_offset
        screen.blit(self.menu, self.menu_rect)
    

    def mainloop(self,screen,clock,game):
        exitmenu=False
        while not exitmenu:
            for event in pygame.event.get():
                if event.type==pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type==pygame.MOUSEBUTTONUP:
                    if self.menu_rect.collidepoint(pygame.mouse.get_pos()):
                        exitmenu=True
                if event.type==pygame.VIDEORESIZE:
                    self.resizeall(screen)
                    if game!=False:
                        game.resizeall(screen)
            if game!=False:
                game.renderall(screen)
            self.renderall(screen)
            
            pygame.display.update()
            clock.tick(120.0)
        
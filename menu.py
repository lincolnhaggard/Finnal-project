import pygame
import sys
import math
class Menu:
    def __init__(self,screen,clock,game=False):
        self.menu=pygame.image.load("img/menu.png").convert_alpha()
        self.menu=pygame.transform.scale(self.menu,(500,500))
        self.play=pygame.image.load("img/play_button.png").convert_alpha()
        self.play=pygame.transform.scale(self.play,(400,200))
        self.menu_rect=self.menu.get_rect(center=(2560/2,700))
        self.play_rect=self.menu.get_rect(center=(2560/2,700))
        self.icons=[
            [0],
            [0],
            [0]
            ]
        self.iconsr=[
            [0],
            [0],
            [0]
        ]
        for i in range(3):
            self.icons[0].append(pygame.image.load(f"img/micons/icon{i+1}.png").convert_alpha())
            self.icons[0][-1]=pygame.transform.scale(self.icons[0][-1],(50,50))
            self.iconsr[0].append(self.icons[0][-1].get_rect(center=((2560/2+((i)*70)-100),(1400/2-200))))
        for i in range(3):
            self.icons[1].append(pygame.image.load(f"img/micons/icon1{i+1}.png").convert_alpha())
            self.icons[1][-1]=pygame.transform.scale(self.icons[1][-1],(50,50))
            self.iconsr[1].append(self.icons[1][-1].get_rect(center=((2560/2+((i)*70)-100),(1400/2-100))))
        for i in range(10):
            self.icons[2].append(pygame.image.load(f"img/micons/icon2{i+1}.png").convert_alpha())
            self.icons[2][-1]=pygame.transform.scale(self.icons[2][-1],(50,50))
            self.iconsr[2].append(self.icons[2][-1].get_rect(center=((2560/2+((i)*70)-100),(1400/2))))
        self.resizeall(screen)
        self.mainloop(screen,clock,game)

    def get_gap(self):
        if self.icons[0][0]==0:
            gap=400
        if self.icons[0][0]==1:
            gap=300
        if self.icons[0][0]==2:
            gap=500
        return gap
    def get_speed(self):
        if self.icons[1][0]==0:
            speed=1
        if self.icons[1][0]==1:
            speed=1.5
        if self.icons[1][0]==2:
            speed=0.75
        return speed
    def get_mode(self):
        if self.icons[2][0]==0:
            mode="normal"
        if self.icons[2][0]==1:
            mode="reverse"
        if self.icons[2][0]==2:
            mode="dark"
        if self.icons[2][0]==3:
            mode="flying"
        if self.icons[2][0]==4:
            mode="flip"
        if self.icons[2][0]==5:
            mode="gravity"
        if self.icons[2][0]==6:
            mode="pong"
        if self.icons[2][0]==7:
            mode="bomb"
        if self.icons[2][0]==8:
            mode="wave"
        if self.icons[2][0]==9:
            mode="portal"
        return mode
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
        self.menu=pygame.transform.scale(self.menu,(wdh/2560*400,hgt/1400*400))
        self.menucopy=pygame.image.load("img/menu.png").convert_alpha()
        self.menucopy=pygame.transform.scale(self.menucopy, (self.wdh/2560*400,self.hgt/1400*400))
        self.play=pygame.image.load("img/play_button.png").convert_alpha()
        self.play=pygame.transform.scale(self.play,(wdh/2560*390,hgt/1400*100))
        self.menu_rect=self.menu.get_rect(center=(2560/2,700))
        self.play_rect=self.play.get_rect(center=(2560/2,700+200))
        self.menu_rect.centerx=2560/2*(self.wdh/2560)+self.x_offset
        self.menu_rect.centery=(1400/2-60)*(self.hgt/1400)+self.y_offset
        self.play_rect.centerx=(2560/2)*(self.wdh/2560)+self.x_offset
        self.play_rect.centery=(1400/2+200)*(self.hgt/1400)+self.y_offset
        for w,i in enumerate(self.icons):
            for t,icon in enumerate(i):
                if t!=0:
                    if w==0:
                        i[t]=pygame.image.load(f"img/micons/icon{t}.png").convert_alpha()
                        i[t]=pygame.transform.scale(i[t],(wdh/2560*50,hgt/1400*50))
                        self.iconsr[w][t]=self.icons[w][t].get_rect(center=((2560/2+((t)*70)-100)*(self.wdh/2560)+self.x_offset,(1400/2-200)*(self.hgt/1400)+self.y_offset))
                    elif w==1:
                        i[t]=pygame.image.load(f"img/micons/icon1{t}.png").convert_alpha()
                        i[t]=pygame.transform.scale(i[t],(wdh/2560*70,hgt/1400*50))
                        self.iconsr[w][t]=self.icons[w][t].get_rect(center=((2560/2+((t)*70)-100)*(self.wdh/2560)+self.x_offset,(1400/2-100)*(self.hgt/1400)+self.y_offset))
                    elif w==2:
                        i[t]=pygame.image.load(f"img/micons/icon2{t}.png").convert_alpha()
                        i[t]=pygame.transform.scale(i[t],(wdh/2560*50,hgt/1400*50))
                        self.iconsr[w][t]=self.icons[w][t].get_rect(center=((2560/2+((t)*70)-100)*(self.wdh/2560)+self.x_offset,(1400/2)*(self.hgt/1400)+self.y_offset))
                    
    
    

    def renderall(self,screen):
        x=2560/2*(self.wdh/2560)+self.x_offset
        y=1400/2*(self.hgt/1400)+self.y_offset
        
        screen.blit(self.menu, self.menu_rect)
        

        self.menu.blit(self.menucopy, (0,0))
        screen.blit(self.play, self.play_rect)
        for z,i in enumerate(self.icons):
            for t,icon in enumerate(i):
                if t!=0:
                    #if self.iconsr[z][t].left>self.menu_rect.left and self.iconsr[z][t].right<self.menu_rect.right:
                        self.menu.blit(icon,(self.iconsr[z][t].x-self.menu_rect.x,self.iconsr[z][t].y-self.menu_rect.y))
    
    def animate(self):
        for w,i in enumerate(self.iconsr):
            if i[i[0]+1].centerx!=1280:
                distance=abs(1280-i[i[0]+1].centerx)
                if i[i[0]+1].centerx<1279:
                    for t,icon in enumerate(i):
                        if t!=0:
                            icon.centerx+=math.floor((distance)**0.7/5)+1
                            icon.centerx=round(icon.centerx,1)
                elif i[i[0]+1].centerx>1281:
                    for t,icon in enumerate(i):
                        if t!=0:
                            icon.centerx-=math.floor((distance)**0.7/5)+1
                            icon.centerx=round(icon.centerx,1)
    def mainloop(self,screen,clock,game):
        exitmenu=False
        while not exitmenu:
            clickedicon=False
            for event in pygame.event.get():
                if event.type==pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type==pygame.MOUSEBUTTONUP:
                    for w,i in enumerate(self.iconsr):
                        for t,icon in enumerate(i):
                            if t!=0:
                                if icon.collidepoint(pygame.mouse.get_pos()):
                                    i[0]=t-1
                                    self.icons[w][0]=t-1
                                    clickedicon=True
                    if self.play_rect.collidepoint(pygame.mouse.get_pos()) and not clickedicon:
                        exitmenu=True
                if event.type==pygame.VIDEORESIZE:
                    self.resizeall(screen)
                    if game!=False:
                        game.resizeall(screen)
            
            self.animate()
            
            if game!=False:
                game.renderall(screen)
            
            self.renderall(screen)
            
            pygame.display.update()
            clock.tick(120.0)
        
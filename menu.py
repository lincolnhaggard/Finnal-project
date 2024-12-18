import pygame
import sys
import math


class Menu:


    def __init__(self,screen,clock,game=False):
        """there are some variables not defined in the __init__ function
           they are instead defiened in the resize all function:
            menu
            menu_rect
            menucopy
            play
            play_rect
            side_burn
            x_offset
            y_offset
            wdh (resized width)
            hgt (resized height)
           """
        self.icons=[
                [0],
                [0]
                [0]
                ]
        self.iconsr=[
                [0],
                [0]
                [0]
                ]
        #icons and iconr have to be defined in __init__ so that the length of the list stays consistent
        
        for L in range(3):
            self.icons[0].append(pygame.image.load(f"img/micons/icon0{L+1}.png").convert_alpha())
            self.icons[0][-1]=pygame.transform.scale(self.icons[0][-1],(50,50))
            self.iconsr[0].append(self.icons[0][-1].get_rect(center=((2560/2+((L)*70)-100),(1400/2-200))))
        for L in range(3):
            self.icons[1].append(pygame.image.load(f"img/micons/icon1{i+1}.png").convert_alpha())
            self.icons[1][-1]=pygame.transform.scale(self.icons[1][-1],(50,50))
            self.iconsr[1].append(self.icons[1][-1].get_rect(center=((2560/2+((L)*70)-100),(1400/2-100))))
        for L in range(10):
            self.icons[2].append(pygame.image.load(f"img/micons/icon2{i+1}.png").convert_alpha())
            self.icons[2][-1]=pygame.transform.scale(self.icons[2][-1],(50,50))
            self.iconsr[2].append(self.icons[2][-1].get_rect(center=((2560/2+((L)*70)-100),(1400/2))))
        
        self.resizeall(screen)
        self.mainloop(screen,clock,game)

    def get_gap(self):
        if self.icons[0][0]==0:
            gap=400
        elif self.icons[0][0]==1:
            gap=300
        elif self.icons[0][0]==2:
            gap=500
        return gap
    
    def get_speed(self):
        if self.icons[1][0]==0:
            speed=1
        elif self.icons[1][0]==1:
            speed=1.5
        elif self.icons[1][0]==2:
            speed=0.75
        return speed
    
    def get_mode(self):
        if self.icons[2][0]==0:
            mode="normal"
        elif self.icons[2][0]==1:
            mode="reverse"
        elif self.icons[2][0]==2:
            mode="dark"
        elif self.icons[2][0]==3:
            mode="flying"
        elif self.icons[2][0]==4:
            mode="flip"
        elif self.icons[2][0]==5:
            mode="gravity"
        elif self.icons[2][0]==6:
            mode="pong"
        elif self.icons[2][0]==7:
            mode="bomb"
        elif self.icons[2][0]==8:
            mode="wave"
        elif self.icons[2][0]==9:
            mode="portal"
        return mode

    def resizeall(self,screen):
        #this code gets the size of the screen
        #it also makes sure that everything stays
        #in the right ratio, picking the smallest one
        wdh=screen.get_width()
        hgt=screen.get_height()

        #side_burns are to prevent bluring if the window size does not match 2560 by 1400
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

        #menu
        self.menu=pygame.image.load("img/menu.png").convert_alpha()
        self.menu=pygame.transform.scale(self.menu,(wdh/2560*400,hgt/1400*400))
        #menurect
        self.menu_rect=self.menu.get_rect(center=(2560/2,700))
        self.menu_rect.centerx=2560/2*(self.wdh/2560)+self.x_offset
        self.menu_rect.centery=(1400/2-60)*(self.hgt/1400)+self.y_offset

        #menucopy
        self.menucopy=pygame.image.load("img/menu.png").convert_alpha()
        self.menucopy=pygame.transform.scale(self.menucopy, (self.wdh/2560*400,self.hgt/1400*400))

        #play
        self.play=pygame.image.load("img/play_button.png").convert_alpha()
        self.play=pygame.transform.scale(self.play,(wdh/2560*390,hgt/1400*100))
        #play_rect
        self.play_rect=self.play.get_rect(center=(2560/2,700+200))
        self.play_rect.centerx=(2560/2)*(self.wdh/2560)+self.x_offset
        self.play_rect.centery=(1400/2+200)*(self.hgt/1400)+self.y_offset
        
        
        
        for w,i in enumerate(self.icons):
            for t,icon in enumerate(i):
                if t!=0:
                    i[t]=pygame.image.load(f"img/micons/icon{str(w)+str(t)}.png").convert_alpha()
                    if w==0:
                        i[t]=pygame.transform.scale(i[t],(wdh/2560*50,hgt/1400*50))
                    elif w==1:
                        i[t]=pygame.transform.scale(i[t],(wdh/2560*70,hgt/1400*50))
                    elif w==2:
                        i[t]=pygame.transform.scale(i[t],(wdh/2560*50,hgt/1400*50))
                    #The get_rect function needs to happend after the resize function
                    #so that the rectangle is the right size
                    self.iconsr[w][t]=self.icons[w][t].get_rect(center=((2560/2+((t)*70)-100)*(self.wdh/2560)+self.x_offset,(1400/2-200+(w*100))*(self.hgt/1400)+self.y_offset))

    def renderall(self,screen):
        screen.blit(self.menu, self.menu_rect)
        
        #menu copy is used to prevent the icons
        #from smearing on the menu
        self.menu.blit(self.menucopy, (0,0))

        screen.blit(self.play, self.play_rect)
        for z,i in enumerate(self.icons):
            for t,icon in enumerate(i):
                if t!=0:
                    #the icons are rendered on the menu so that 
                    #they do not render outside the menu
                    self.menu.blit(icon,(self.iconsr[z][t].x-self.menu_rect.x,self.iconsr[z][t].y-self.menu_rect.y))
    
    def animate(self):
        #this function moves all the icons in nice amounts
        for i in self.iconsr:
            #i[i[0]+1] is the icon that should be moved to the center
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
        exitmenu=False #exit menu is so that we can quit the menu
                       #inside the event loop
        while not exitmenu:
            clickedicon=False
            for event in pygame.event.get():

                if event.type==pygame.QUIT:#required
                    pygame.quit()
                    sys.exit()

                if event.type==pygame.MOUSEBUTTONUP:
                    #checks which if any icon was clicked
                    for w,i in enumerate(self.iconsr):
                        for t,icon in enumerate(i):
                            if t!=0:
                                if icon.collidepoint(pygame.mouse.get_pos()):
                                    i[0]=t-1
                                    self.icons[w][0]=t-1
                                    clickedicon=True
                    #quits the menu loop if the play button is pressed
                    if self.play_rect.collidepoint(pygame.mouse.get_pos()) and not clickedicon:
                        exitmenu=True
                
                if event.type==pygame.VIDEORESIZE:
                    self.resizeall(screen)
                    if game!=False:
                        game.resizeall(screen)
            #things that should happen every tick
            self.animate()
            
            if game!=False:#renders the previous game played if any
                game.renderall(screen)
            
            self.renderall(screen)
            
            pygame.display.update()
            clock.tick(120.0)
        
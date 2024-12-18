import pygame
import sys
from menu import Menu
from game import Game

pygame.init()
clock=pygame.time.Clock()   
screen=pygame.display.set_mode((2560, 1400), flags=pygame.RESIZABLE ,vsync=1)

menu=Menu(screen,clock) #the menu init function also starts it's mainloop
game=Game(screen,clock,menu) #the game init function also starts it's' mainloop

while True:
    menu.resizeall(screen) #don't do the menu init function otherwise the user's previous choices will be reset
    menu.mainloop(screen,clock,game)
    game.__init__(screen,clock,menu)
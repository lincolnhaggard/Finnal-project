import pygame
import sys
from menu import Menu
from game import Game
pygame.init()
clock=pygame.time.Clock()   
screen=pygame.display.set_mode((2560, 1400), pygame.RESIZABLE)
menu=Menu(screen,clock)
game=Game(screen,clock,menu)
while True:
    menu.mainloop(screen,clock,game)
    game.__init__(screen,clock,menu)
    game.mainloop(screen,clock) 
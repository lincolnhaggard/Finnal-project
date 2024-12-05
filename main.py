import pygame
import sys
from menu import Menu
from game import Game
clock=pygame.time.Clock()
pygame.init()
screen=pygame.display.set_mode((2560, 1400), pygame.RESIZABLE)
menu=Menu(screen,clock)
game=Game(screen,clock,menu)
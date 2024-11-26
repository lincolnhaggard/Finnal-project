import pygame
import sys
from menu import Menu
clock=pygame.time.Clock()
pygame.init()
screen=pygame.display.set_mode((1000, 1000))
menu=Menu(screen,clock)

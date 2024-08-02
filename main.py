#main.py
   
import sys
import os
import pygame

# Ajoutez le dossier 'src' au chemin de recherche des modules
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from game import Game

if __name__ == '__main__':
    pygame.init()
    game = Game()
    game.run()

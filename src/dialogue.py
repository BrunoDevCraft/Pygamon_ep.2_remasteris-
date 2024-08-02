#dialogs.py

import pygame
import os

class DialogBox:

    X_POSITION = 60
    Y_POSITION = 470

    def __init__(self):
        # Assurez-vous que les chemins des fichiers sont corrects
        base_path = os.path.dirname(os.path.abspath(__file__))  # Chemin du répertoire contenant ce script
        self.box_path = os.path.join(base_path, '..', 'dialogs', 'dialog_box.png')
        self.font_path = os.path.join(base_path, '..', 'dialogs', 'dialog_font.ttf')
        
        self.box = pygame.image.load(self.box_path)
        self.box = pygame.transform.scale(self.box, (700, 100))
        self.texts = []
        self.text_index = 0
        self.letter_index = 0
        self.font = pygame.font.Font(self.font_path, 18)
        self.reading = False
    
    def execute(self, dialog=[]):
        if self.reading:
            self.next_text()
        else:
            self.reading = True
            self.text_index = 0
            self.texts = dialog
            self.letter_index = 0  # Réinitialiser l'index des lettres

    def render(self, screen):
        if self.reading:
            self.letter_index += 1

            if self.letter_index > len(self.texts[self.text_index]):
                self.letter_index = len(self.texts[self.text_index])  # Assurez-vous que l'index ne dépasse pas la longueur du texte
            
            screen.blit(self.box, (self.X_POSITION, self.Y_POSITION))
            text = self.font.render(self.texts[self.text_index][0:self.letter_index], True, (0, 0, 0))
            screen.blit(text, (self.X_POSITION + 60, self.Y_POSITION + 30))

    def next_text(self):
        self.text_index += 1
        self.letter_index = 0  # Réinitialiser l'index des lettres pour le nouveau texte

        if self.text_index >= len(self.texts):
            self.reading = False  # Fermer la boîte de dialogue si tous les textes sont lus

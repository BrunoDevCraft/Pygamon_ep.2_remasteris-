import pygame
import os

class AnimateSprite(pygame.sprite.Sprite):
    def __init__(self, name):
        super().__init__()
        # Chemin relatif pour le dossier 'sprite'
        sprite_sheet_path = os.path.join(os.path.dirname(__file__), '..', 'sprite', f"{name}.png")
        self.sprite_sheet = self.load_image(sprite_sheet_path)
        self.animation_index = 0
        self.clock = 0
        self.images = {
            'down': self.get_images(0),
            'left': self.get_images(32),
            'right': self.get_images(64),
            'up': self.get_images(96)
        }
        self.speed = 2 

    def load_image(self, path):
        try:
            # Assurez-vous que le chemin est correct et l'image est chargée
            image = pygame.image.load(path).convert_alpha()
            return image
        except pygame.error as e:
            print(f"Impossible de charger l'image à {path}: {e}")
            raise SystemExit(e)

    def change_animation(self, name): 
        if name not in self.images:
            print(f"Animation {name} non trouvée.")
            return

        self.image = self.images[name][self.animation_index]
        self.image.set_colorkey((0, 0, 0))
        self.clock += self.speed * 8

        if self.clock >= 100:
            self.animation_index += 1  # Passer à l'image suivante

            if self.animation_index >= len(self.images[name]):
                self.animation_index = 0

            self.clock = 0

    def get_images(self, y):
        images = []

        for i in range(0, 3):
            x = i * 32
            image = self.get_image(x, y)
            images.append(image)
        
        return images

    def get_image(self, x, y):
        image = pygame.Surface([32, 32], pygame.SRCALPHA)  # Utilisation de SRCALPHA pour conserver la transparence
        image.blit(self.sprite_sheet, (0, 0), (x, y, 32, 32))
        return image

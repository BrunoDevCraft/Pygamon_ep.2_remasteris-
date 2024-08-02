from dataclasses import dataclass
import pygame
import pyscroll
import pytmx
import os
from player import NPC  # Assurez-vous que le fichier player.py est dans le dossier src

@dataclass
class Portal:
    from_world: str
    origin_point: str
    target_world: str
    teleport_point: str

@dataclass
class Map:
    name: str
    walls: list[pygame.Rect]
    group: pyscroll.PyscrollGroup
    tmx_data: pytmx.TiledMap
    portals: list[Portal]
    npcs: list[NPC]

class MapManager:
    def __init__(self, screen, player):
        self.maps = dict()
        self.screen = screen
        self.player = player
        self.current_map = "world"

        # Enregistrez les cartes avec leurs portails et NPCs
        self.register_map("world", portals=[
            Portal(from_world="world", origin_point="enter_house_1", target_world="house_1", teleport_point="point_entrée_house_1"), 
            Portal(from_world="world", origin_point="enter_house_2", target_world="house_2", teleport_point="point_entrée_house_2"),        
            Portal(from_world="world", origin_point="enter_dungeon", target_world="dungeon", teleport_point="spawn_dungeon")
        ], npcs=[
            NPC("paul", nb_points=4, dialog=["Hello, je m'appelle Paul", "@+"]), 
            NPC("robin", nb_points=2, dialog=["J'espère que tu vas bien!"])
        ])

        self.register_map("house_1", portals=[
            Portal(from_world="house_1", origin_point="exit_house_1", target_world="world", teleport_point="point_sortie_house_1"),
        ])
        self.register_map("house_2", portals=[
            Portal(from_world="house_2", origin_point="exit_house_2", target_world="world", teleport_point="point_sortie_house_2"),
        ])
        self.register_map("dungeon", portals=[
            Portal(from_world="dungeon", origin_point="exit_dungeon", target_world="world", teleport_point="spawn_exit_dungeon"),
        ], npcs=[
            NPC("boss", nb_points=2, dialog=["MWWAAAA", "je garde ces lieux"])
        ])
        
        self.teleport_npcs()  # Téléporter les NPCs avant de téléporter le joueur
        self.teleport_player("player")  # Téléporter le joueur au point d'entrée du donjon

    def check_npc_collisions(self, dialog_box):
        for sprite in self.get_group().sprites():
            if sprite.feet.colliderect(self.player.rect) and isinstance(sprite, NPC):
                dialog_box.execute(sprite.dialog)

    def check_collisions(self):
        for portal in self.get_map().portals:
            if portal.from_world == self.current_map:
                point = self.get_object(portal.origin_point)
                rect = pygame.Rect(point.x, point.y, point.width, point.height)

                if self.player.feet.colliderect(rect):
                    copy_portal = portal
                    self.current_map = portal.target_world
                    self.teleport_player(copy_portal.teleport_point)

        for sprite in self.get_group().sprites():
            if isinstance(sprite, NPC):
                if sprite.feet.colliderect(self.player.rect):
                    sprite.speed = 0
                else:
                    sprite.speed = 1

            if sprite.feet.collidelist(self.get_walls()) > -1:
                sprite.move_back()

    def teleport_player(self, name):
        point = self.get_object(name)
        self.player.position[0] = point.x
        self.player.position[1] = point.y
        self.player.save_location()

    def register_map(self, name, portals=[], npcs=[]):
        # Charger la carte tmx depuis le dossier 'map'
        tmx_path = os.path.join(os.path.dirname(__file__), '..', 'map', f"{name}.tmx")
        tmx_data = pytmx.util_pygame.load_pygame(tmx_path)
        map_data = pyscroll.data.TiledMapData(tmx_data)
        map_layer = pyscroll.orthographic.BufferedRenderer(map_data, self.screen.get_size())
        map_layer.zoom = 2

        # Définir une liste qui va stocker les murs
        walls = []

        for obj in tmx_data.objects:
            if obj.type == "collision":
                walls.append(pygame.Rect(obj.x, obj.y, obj.width, obj.height))

        # Dessiner un groupe de calque
        group = pyscroll.PyscrollGroup(map_layer=map_layer, default_layer=5)
        group.add(self.player)

        # Récupérer tous les NPCs pour les ajouter au groupe
        for npc in npcs:
            group.add(npc)

        # Enregistrer la nouvelle carte
        self.maps[name] = Map(name, walls, group, tmx_data, portals, npcs)

    def get_map(self): return self.maps[self.current_map]

    def get_group(self): return self.get_map().group

    def get_walls(self): return self.get_map().walls

    def get_object(self, name): return self.get_map().tmx_data.get_object_by_name(name)

    def teleport_npcs(self):
        for map_name in self.maps:
            map_data = self.maps[map_name]
            npcs = map_data.npcs

            for npc in npcs:
                npc.load_points(map_data.tmx_data)
                npc.teleport_spawn()

    def draw(self):
        self.get_group().draw(self.screen)
        self.get_group().center(self.player.rect.center)

    def update(self):
        self.get_group().update()
        self.check_collisions()

        for npc in self.get_map().npcs:
            npc.move()

import os
from random import randint

import pygame
from pygame.locals import *
import numpy as np

import networkx as nx
import openpyxl as opxl
import importlib, inspect

from TileType import *

TILE_W, TILE_H = 32, 32
named_tile = {"grass":0, "darkgrass":1, "dirt":2, "road":3}

MAP_WIDTH = 9
MAP_HEIGHT = 17

DISPLAY_WIDTH = 32 * MAP_WIDTH
DISPLAY_HEIGHT = 32 * MAP_HEIGHT
#pygame.display.set_mode((MAP_WIDTH, MAP_HEIGHT))

debug = True

class Map():
	"""Stores map info as a 2d numpy array, and renders tiles.
	Map is an array of ints, which correspond to the tile id

	members:
		scrolling:	toggle mouse smooth scrolling of map
		offset:	topleft for scrolling and world<->screen coordinate conversion.
	"""

	def __init__(self):
		self.width = MAP_WIDTH
		self.height = MAP_HEIGHT

		self.screen = pygame.display.set_mode((DISPLAY_WIDTH, DISPLAY_HEIGHT))
		self.scrolling = False
		self.load_tileset(os.path.join("art","32x32_DEMO.png"))

		self.spreadsheet_path = "C:\\StratGames\\FEclone\\FEclone Python Prototype\\TestMap.xlsx"

		self.map_spreadhseet = opxl.load_workbook(self.spreadsheet_path)
		self.terrain_sheet = self.map_spreadhseet["TerrainTypes"]
		self.texture_sheet = self.map_spreadhseet["TextureTypes"]

		self.map_graph = nx.grid_2d_graph(MAP_HEIGHT, MAP_WIDTH, periodic=False, create_using=None)    

		self.generate_map()

		self.reset()
		self.randomize()

	def generate_map(self):
		terrains = [class_tuple[0] for class_tuple in inspect.getmembers(importlib.import_module("TileType"), inspect.isclass)]

		nodes_iterator = iter(self.map_graph.nodes)

		for terrain_row, texture_row in zip(self.terrain_sheet.values, self.texture_sheet.values):
			for terrain, texture in zip(terrain_row, texture_row):
				current_node = next(nodes_iterator)
				print(texture)
				if terrain in terrains:
					
					if terrain == "Plains":
						self.map_graph.nodes[current_node]["Terrain"] = Plains()
						self.map_graph.nodes[current_node]["Texture"] = texture
					
					elif terrain == "Forest":
						self.map_graph.nodes[current_node]["Terrain"] = Forest()
						self.map_graph.nodes[current_node]["Texture"] = texture
					
					elif terrain == "Altar":
						self.map_graph.nodes[current_node]["Terrain"] = Altar()
						self.map_graph.nodes[current_node]["Texture"] = texture

					elif terrain == "Miasma":
						self.map_graph.nodes[current_node]["Terrain"] = Miasma()
						self.map_graph.nodes[current_node]["Texture"] = texture
					
					elif terrain == "Lava":
						self.map_graph.nodes[current_node]["Terrain"] = Lava()
						self.map_graph.nodes[current_node]["Texture"] = texture
					
				else:
					self.map_graph.nodes[current_node]["Terrain"] = texture
				
				print(self.map_graph.nodes[current_node]["Terrain"])
        
		print(self.map_graph.nodes(data=True))

	def reset(self, tiles_x=60, tiles_y=40):
		# clear map, and reset to defaults.
		"""
		default to fit for one screen size:
        self.tiles_x = self.game.width / TILE_W
        self.tiles_y = self.game.height / TILE_H
        """
        # or a fixed number
        #self.tiles_x =10
        #tiles_y = 10
		self.tiles_x, self.tiles_y = tiles_x, tiles_y

        # create empty array , filled with zero
		self.tiles = np.zeros((self.tiles_x, self.tiles_y), dtype=int)
        
		# if debug:
        # 	print("Map().reset(size={}, {})".format(tiles_x, tiles_y))

	def randomize(self):
		# give all tiles random values
		self.offset = (-200, 200)

		# completely random
		for y in range(self.tiles_y):
			for x in range(self.tiles_x):
				#print(len(named_tile.keys()))
				self.tiles[x,y] = randint(0, len(named_tile.keys()))

		# example of slicing, to add roads
		#self.tiles[1:] = named_tile["road"]
		#self.tiles[:2] = named_tile["road"]

		if debug: print("tiles = ", self.tiles)

	def scroll(self, rel):
		#scroll map using relative coordinates
		if not self.scrolling: return

		self.offset = (
				self.offset[0] + rel[0],
				self.offset[1] + rel[1] )

	def load_tileset(self, image="32x32_DEMO.png"):
		# load image
		self.tileset = pygame.image.load(image)
		self.rect = self.tileset.get_rect()

	def draw(self):
		# no optimization, just iterate to render tiles
		# You could start iterating at actual tiles on screen, instead.
		#print(self.tiles_x,self.tiles_y)

		for node in self.map_graph.nodes:

				#print(self.map_graph.nodes)
				#print("apple", tuple(map(int, self.map_graph.nodes[node]["Texture"].split(', '))))
				#print(self.map_graph.nodes[node]["Terrain"])
				x, y = tuple(map(int, self.map_graph.nodes[node]["Texture"].split(', ')))
				#print(cur)
				#print(node)
				dest = Rect(node[1] * TILE_W, node[0]  * TILE_H, TILE_W, TILE_H)
				
				background = Rect(9 * TILE_W, 10 * TILE_W, TILE_W, TILE_H)
				src = Rect(x * TILE_W, y * TILE_W, TILE_W, TILE_H)

				# screen to world coord
				if self.scrolling:
					dest.left += self.offset[0]
					dest.top += self.offset[1]

				self.screen.blit(self.tileset, dest, background)
				self.screen.blit(self.tileset, dest, src)
		
				BLACK = (0, 0, 0)

		for x in range(0, DISPLAY_WIDTH, 32):
			for y in range(0, DISPLAY_HEIGHT, 32):
				rect = pygame.Rect(x, y, TILE_W, TILE_W)
				pygame.draw.rect(self.screen, BLACK, rect, 1)
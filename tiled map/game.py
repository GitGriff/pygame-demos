from __future__ import print_function, division
import pygame
from pygame.locals import *
from map_tiled import Map

import os

class Cursor(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pygame.image.load(os.path.join('art', 'selection_icon.png'))
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y

    def move(self, dx=0, dy=0):
        self.x += dx
        self.y += dy

    def update(self):
        self.rect.x = self.x * 32
        self.rect.y = self.y * 32

class Game():
	""" main logic.
	
	properties:
		map:	map.Map()

	"""
	done = False
	
	def __init__(self, width=640, height=480):
		pygame.init()
		self.all_sprites = pygame.sprite.Group()
		self.width, self.height = width, height
		self.clock = pygame.time.Clock()
		self.screen = pygame.display.set_mode((self.width, self.height))
		self.player = Cursor(self, 1, 1)
		pygame.display.set_caption("demo: tiled map")

		self.map = Map()

	def update(self):
		# update portion of the game loop
		self.all_sprites.update()

	def main_loop(self):
		# main loop
		while not self.done:
			self.dt = self.clock.tick(20)
			self.handle_events()
			self.update()
			self.draw()
			#print(self.player.rect)

	def handle_events(self):
		# handle and copy events if needed
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				self.done = True

			# keydown
			elif event.type == KEYDOWN:
                
				if event.key == pygame.K_LEFT:
					self.player.move(dx=-1)
                
				if event.key == pygame.K_RIGHT:
					self.player.move(dx=1)
                
				if event.key == pygame.K_UP:
					self.player.move(dy=-1)
                
				if event.key == pygame.K_DOWN:
					self.player.move(dy=1)
				
				if event.key == K_ESCAPE:
					self.done = True
					
				elif event.key == K_s:
					self.map.scrolling = not self.map.scrolling

				elif event.key == K_SPACE:
					self.map.randomize()

			elif event.type == MOUSEMOTION:
				self.map.scroll(event.rel)

	def draw(self):
		# render
		#self.screen.fill(Color("gray20"))
		self.map.draw()
		self.all_sprites.draw(self.screen)
		pygame.display.flip()

if __name__ == "__main__":
	game = Game()
	game.main_loop()
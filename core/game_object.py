import pygame
from pygame.math import Vector2

class Game_object(pygame.sprite.Sprite):
	def __init__(self, game, image, x_scale, y_scale, initial_x=0, initial_y=0):
		self.init_images(image)
		if x_scale and y_scale:
			self.image = pygame.transform.scale(self.image, (x_scale, y_scale))
		self.image_rect = self.image.get_rect()
		self.cur_image = self.image
		self.scale = Vector2(x_scale, y_scale)
		self._game = game
		self.pos = Vector2(initial_x, initial_y)
		self.last_pos = Vector2(initial_x, initial_y)
		self._dead = False

	def set_scale(self, x_scale, y_scale):
		self.scale = Vector2(x_scale, y_scale)
		self.image = pygame.transform.scale(self.image, (x_scale, y_scale))
		self.image_rect = self.image.get_rect()
		
	def init_images(self, image):
		if isinstance(image, list):
			self.images = image
			self.image = self.images[0]
		else:
			self.image = image
			self.images = [image]
		self.last_animated_image_change = 0
		self.image_index = 0

	def back_up(self):
		self.last_pos = self.pos

	def get_pos(self):
		return self.pos
	
	def set_pos(self, new_initial_x, new_initial_y):
		self.pos = Vector2(new_initial_x, new_initial_y)
	
	def draw(self, serface, camera_offset = Vector2(0,0)):
		relative_pos = self.pos - camera_offset
		if self.is_inside_screen(relative_pos):
			serface.blit(self.image, (relative_pos[0], relative_pos[1]))
   
	def is_inside_screen(self, pos):
		return ((pos[0]<800) and (pos[1]<500)) and ((pos[0]+self.scale[0]>=0) and (pos[1]+self.scale[1]>=0))
		
	def get_rect(self, extra=(0,0)):
		return pygame.Rect(self.pos[0], self.pos[1], self.scale[0]+extra[0], self.scale[1]+extra[1])
	
	def update(self):
		pass

	def __del__(self):
		pass
import pygame
import sys,os
import random
from typing import Union
from helpers import  get_random_color, create_random_node_settings
from pygame.locals import *

class Node:
	def __init__(self, window_size :tuple, node_position: tuple, node_size: tuple, node_name: str="node", node_color : str="white") :
		"""
		Args:
			window_size(tuple): window size containing height and width
			node_position(tuple): node starting position
			node_size(tuple): node size
			node_name(str): node name
			node_color(str): node color
		"""
		self.window_size = window_size
		self.name = node_name
		self.position = node_position
		self.size = node_size
		self.color = node_color
		self.rect = pygame.Rect(self.position, self.size)
		if self.name =="center-node":
			self.position = ((self.window_size[0]//2) , (self.window_size[1]//2) )
			self.rect.center = self.position
		if self.name == "top-left":
			self.position = (self.size[0]//2,self.size[1]//2)
			self.rect.center = self.position
		if self.name == "top-mid":
			self.position = ((self.window_size[0]//2),(self.size[0]//2))
			self.rect.center = self.position
		if self.name == "top-right":
			self.position = ((self.window_size[0]) - (self.size[0]//2),(self.size[0]//2))
			self.rect.center = self.position
		if self.name == "right-mid":
			self.position = ((self.window_size[0]) - (self.size[0]//2) ,(self.window_size[1]//2))
			self.rect.center = self.position
		if self.name == "right-bottom":
			self.position = ((self.window_size[0]) - (self.size[0]//2) ,(self.window_size[1]) - (self.size[1]//2))
			self.rect.center = self.position
		if self.name == "bottom-mid":
			self.position = ((self.window_size[0]//2) ,(self.window_size[1]) - (self.size[1]//2))
			self.rect.center = self.position
		if self.name == "bottom-left":
			self.position = ((self.size[0]//2) ,(self.window_size[1]) - (self.size[1]//2))
			self.rect.center = self.position
		if self.name == "left-mid":
			self.position = ((self.size[0]//2) ,(self.window_size[1]//2))
			self.rect.center = self.position

	def speed(self, speed : dict):
		"""
		Set the node speed
		Args:
			speed(dict): a dictionary containing the speed values
		"""
		self.node_x_direction = speed["x_direction"]
		self.node_y_direction = speed["y_direction"]
		self.node_x_speed = speed["x_speed"]
		self.node_y_speed = speed["y_speed"]
		
	
	def update_node_position(self):
		"""
		Update the node position
		"""
		if self.rect.left <=0:
			self.node_x_direction = 1
		if self.rect.right > self.window_size[0]:
			self.node_x_direction = -1
		self.rect.x += self.node_x_speed * self.node_x_direction

		if self.rect.top <=0:
			self.node_y_direction = 1
		if self.rect.bottom > self.window_size[1]:
			self.node_y_direction = -1
		self.rect.y += self.node_y_speed * self.node_y_direction

		

	
		
		
class Manager:
	def __init__(self, general_settings: dict, display: pygame.display, nodes_settings: dict, speed_settings: dict) -> None:
		"""
		Args:
			general_settings(dict): the general settings
			display(pygame.display): the display to draw on
			nodes_settings(dict): the nodes settings
			speed_settings(dict): the nodes speed settings
		"""
		self.general_settings = general_settings
		self.display = display
		self.nodes_settings = nodes_settings
		self.speed_settings = speed_settings
		
		self.nodes = {"center-node" : [], "frame-nodes" : [[1] * 8,[]], "nodes" : []}

	def create_nodes(self):
		"""
		Create the nodes.
		"""
		#center node
		center_node = Node(window_size=self.general_settings["window-size"],node_name="center-node",
					 	node_size=self.nodes_settings["node-size"],node_position=(0,300),
						node_color=self.nodes_settings["center-node-color"])
		self.nodes["center-node"].append(center_node)
		#frame nodes
		top_left_node = Node(window_size=self.general_settings["window-size"], node_name="top-left",
					   		node_size=self.nodes_settings["node-size"],node_position=(0,0),
							node_color=self.nodes_settings["frame-node-color"]
					   		)
		self.nodes["frame-nodes"][1].append(top_left_node)

		top_mid_node = Node(window_size=self.general_settings["window-size"], node_name="top-mid",
					   		node_size=self.nodes_settings["node-size"],node_position=(0,0),
							node_color=self.nodes_settings["frame-node-color"]
					   		)
		self.nodes["frame-nodes"][1].append(top_mid_node)

		top_right_node = Node(window_size=self.general_settings["window-size"], node_name="top-right",
					   		node_size=self.nodes_settings["node-size"],node_position=(0,0),
							node_color=self.nodes_settings["frame-node-color"]
					   		)
		self.nodes["frame-nodes"][1].append(top_right_node)

		right_mid_node = Node(window_size=self.general_settings["window-size"], node_name="right-mid",
					   		node_size=self.nodes_settings["node-size"],node_position=(0,0),
							node_color=self.nodes_settings["frame-node-color"]
					   		)
		self.nodes["frame-nodes"][1].append(right_mid_node)


		right_bottom_node = Node(window_size=self.general_settings["window-size"], node_name="right-bottom",
					   		node_size=self.nodes_settings["node-size"],node_position=(0,0),
							node_color=self.nodes_settings["frame-node-color"]
					   		)
		self.nodes["frame-nodes"][1].append(right_bottom_node)

		bottom_mid_node = Node(window_size=self.general_settings["window-size"], node_name="bottom-mid",
					   		node_size=self.nodes_settings["node-size"],node_position=(0,0),
							node_color=self.nodes_settings["frame-node-color"]
					   		)
		self.nodes["frame-nodes"][1].append(bottom_mid_node)

		bottom_left_node = Node(window_size=self.general_settings["window-size"], node_name="bottom-left",
					   		node_size=self.nodes_settings["node-size"],node_position=(0,0),
							node_color=self.nodes_settings["frame-node-color"]
					   		)
		self.nodes["frame-nodes"][1].append(bottom_left_node)
		
		left_mid_node = Node(window_size=self.general_settings["window-size"], node_name="left-mid",
					   		node_size=self.nodes_settings["node-size"],node_position=(0,0),
							node_color=self.nodes_settings["frame-node-color"]
					   		)
		self.nodes["frame-nodes"][1].append(left_mid_node)
		#nodes
		for _ in range(self.nodes_settings["node-count"]):
			start_position = (random.randint(0,self.general_settings["window-size"][0]),random.randint(0,self.general_settings["window-size"][1]))
			new_node = Node(window_size=self.general_settings["window-size"],
					   		node_size=self.nodes_settings["node-size"],node_position=start_position,
							node_color=self.nodes_settings["node-color"]
					   		)
			self.nodes["nodes"].append(new_node)
		for node in self.nodes["nodes"]:
			node.speed(speed=self.speed_settings)
	
	def draw_center_node(self):
		"""Draw ceneter node"""
		if self.nodes["center-node"][0].color == "random1":
			self.nodes["center-node"][0].color = get_random_color()
			pygame.draw.ellipse(self.display,self.nodes["center-node"][0].color, self.nodes["center-node"][0])
		elif self.nodes["center-node"][0].color == "random2":
			pygame.draw.ellipse(self.display,get_random_color(), self.nodes["center-node"][0])
		elif self.nodes["center-node"][0].color == "none":
			...
		else:
			pygame.draw.ellipse(self.display,self.nodes["center-node"][0].color, self.nodes["center-node"][0])
	
	def draw_frame_nodes(self):
		"""
		Draw frame nodes.
		"""
		for i,frame_node in enumerate(self.nodes["frame-nodes"][1]):
			if frame_node.color == "random1":
				self.nodes["frame-nodes"][1][i].color = get_random_color()
				pygame.draw.ellipse(self.display, frame_node.color, frame_node)
			elif frame_node.color == "random2":
				pygame.draw.ellipse(self.display, get_random_color(), frame_node)
			elif frame_node.color == "none":
				...
			else:
				pygame.draw.ellipse(self.display, frame_node.color, frame_node)

	def draw_nodes(self):	
		"""
		Draw nodes.
		"""
		for i, node in enumerate(self.nodes["nodes"]):
			if node.color == "random1":
				self.nodes["nodes"][i].color = get_random_color()
				pygame.draw.ellipse(self.display, node.color, node)
			elif node.color == "random2":
				pygame.draw.ellipse(self.display, get_random_color(), node)
			elif node.color == "none":
				...
			else:
				pygame.draw.ellipse(self.display, node.color, node)

	def draw_center_edge(self):
		"""
		Draw ceneter edge for each node.
		"""
		for _, node in enumerate(self.nodes["nodes"]):
			if self.nodes_settings["center-edge-color"] == "random1":
				self.nodes_settings["center-edge-color"] = get_random_color()
				pygame.draw.line(self.display, self.nodes_settings["center-edge-color"], node.rect.center,
					  self.nodes["center-node"][0].rect.center, self.nodes_settings["center-edge-thickness"])
			elif self.nodes_settings["center-edge-color"] == "random2":
				pygame.draw.line(self.display, get_random_color(), node.rect.center,
					  self.nodes["center-node"][0].rect.center, self.nodes_settings["center-edge-thickness"])
			elif self.nodes_settings["center-edge-color"] == "none":
				...
			else:
				pygame.draw.line(self.display, self.nodes_settings["center-edge-color"],
					  node.rect.center, self.nodes["center-node"][0].rect.center, self.nodes_settings["center-edge-thickness"])
				
	def draw_frames_edges(self):
		"""
		Draw edges to frame nodes for the nodes.
		"""
		for i,frame_node in enumerate(self.nodes["frame-nodes"][1]):
			for node in self.nodes["nodes"]:
				if self.nodes_settings["frame-edge-color"] == "random1":
					self.nodes_settings["frame-edge-color"] = get_random_color()
					if self.nodes_settings["node-edges-frame"][i]:
						pygame.draw.line(self.display,self.nodes_settings["frame-edge-color"],node.rect.center, frame_node.rect.center, self.nodes_settings[ "node-frame-edges-thickness"][i])
				elif self.nodes_settings["frame-edge-color"] == "random2":
					if self.nodes_settings["node-edges-frame"][i]:
						pygame.draw.line(self.display,get_random_color(),node.rect.center, frame_node.rect.center, self.nodes_settings[ "node-frame-edges-thickness"][i])
				elif self.nodes_settings["frame-edge-color"] == "none":
					...
				else:
					if self.nodes_settings["node-edges-frame"][i]:
						pygame.draw.line(self.display,self.nodes_settings["frame-edge-color"],node.rect.center, frame_node.rect.center, self.nodes_settings[ "node-frame-edges-thickness"][i])

	def draw_nodes_adj(self):
		"""
		Draw edges between node (left and right).
		"""
		nodes = self.nodes["nodes"]
		nodes_count = len(nodes)
		for i, node in enumerate(nodes):
			if i + 1 == nodes_count:
				break
			if self.nodes_settings["node_edges_adj_color"] == "random1":
				self.nodes_settings["node_edges_adj_color"] = get_random_color()
				pygame.draw.line(self.display,self.nodes_settings["node_edges_adj_color"],
								node.rect.center, nodes[i+1].rect.center, self.nodes_settings["node-edge-node-thickness"])
			elif self.nodes_settings["node_edges_adj_color"] == "random2":
				pygame.draw.line(self.display,get_random_color(),
								node.rect.center, nodes[i+1].rect.center, self.nodes_settings["node-edge-node-thickness"])
			elif self.nodes_settings["node_edges_adj_color"] == "none":
				...
			else:
				pygame.draw.line(self.display,self.nodes_settings["node_edges_adj_color"],
								node.rect.center, nodes[i+1].rect.center, self.nodes_settings["node-edge-node-thickness"])
	
	def draw_nodes_all_edges(self):
		"""
		Draw all edges between nodes.
		"""
		nodes = self.nodes["nodes"]
		nodes_count = len(nodes)
		for i, node in enumerate(nodes):
			for j, other_node in enumerate(nodes):
				if other_node == node:
					continue
				if self.nodes_settings["node_edges_adj_color"] == "random1":
					self.nodes_settings["node_edges_adj_color"] = get_random_color()
					pygame.draw.line(self.display,self.nodes_settings["node_edges_adj_color"],
									node.rect.center, nodes[j].rect.center, self.nodes_settings["node-edge-node-thickness"])
					
				elif self.nodes_settings["node_edges_adj_color"] == "random2":
					pygame.draw.line(self.display,get_random_color(),
									node.rect.center, nodes[j].rect.center, self.nodes_settings["node-edge-node-thickness"])
				elif self.nodes_settings["node_edges_adj_color"] == "none":
					...
				else:
					pygame.draw.line(self.display,self.nodes_settings["node_edges_adj_color"],
								node.rect.center, nodes[j].rect.center, self.nodes_settings["node-edge-node-thickness"])
				
	def draw_by_order(self):
		"""
		Draw by the order under 'draw-order' in node settings.
		example: ["nodes","center-node", "frame-nodes", "node-edge-node", "center-edge", "frame-edge", "adj"]
		"""
		for to_draw in self.nodes_settings["draw-order"]:
			if to_draw == "nodes":
				self.draw_nodes()
			if to_draw == "center-node":
				self.draw_center_node()
			if to_draw == "frame-nodes":
				self.draw_frame_nodes()
			if to_draw == "center-edge":
				self.draw_center_edge()
			if to_draw == "frame-edge":
				self.draw_frames_edges()
			if to_draw == self.nodes_settings["node-edge-node"] :
				if to_draw == "adj":
					self.draw_nodes_adj()
				elif to_draw == "all":
					self.draw_nodes_all_edges()
				else:
					...
			
				

class ScreenSaver:
	def __init__(self, general_settings: dict, nodes_settings: dict, speed_settings: dict) -> None:
		self.general_settings = general_settings
		self.nodes_settings = nodes_settings
		self.speed_settings = speed_settings
		self.random_flag = False
		

	def init_pygame(self):
		"""
		This function init pygame and create the timers and music.
		"""
		pygame.init()
		self.display = pygame.display.set_mode(self.general_settings["window-size"])
		pygame.display.set_caption("Take a break")
		self.clock = pygame.time.Clock()
		pygame.time.set_timer(pygame.USEREVENT, self.general_settings["run_x_secs"])
		if os.path.exists(self.general_settings["music"]):
			self.music_queue = []
			self.music_counter = 0
			
			for filename in os.listdir(self.general_settings["music"]):
				if filename.endswith('.mp3'):

					self.music_queue.append(os.path.join(self.general_settings["music"], filename))
			pygame.mixer.music.set_endevent(pygame.USEREVENT + 1)
			pygame.mixer.music.load(self.music_queue[self.music_counter])
			self.music_counter +=1
			pygame.mixer.music.play()
		if self.general_settings["random"]:
			pygame.time.set_timer(pygame.USEREVENT+2, self.general_settings["random-change-time"])
		self.run_flag = True
		self.manager = Manager(general_settings=self.general_settings,
						nodes_settings=self.nodes_settings,speed_settings=self.speed_settings, display=self.display)
		self.manager.create_nodes()
	
	def on_event(self, event):
		"""
		This function handle events.
		"""

		if event.type == pygame.QUIT:
			self.run_flag = False
		if event.type == pygame.USEREVENT:
			self.run_flag = False
		if event.type == pygame.USEREVENT + 1:
			if self.music_counter == len(self.music_queue):
				self.music_counter = 0
			pygame.mixer.music.load(self.music_queue[self.music_counter])
			pygame.mixer.music.play()
			self.music_counter +=1
		if event.type == pygame.USEREVENT + 2:
			self.nodes_settings = create_random_node_settings()
			self.manager.nodes_settings = self.nodes_settings
			self.random_flag = True

		
	def on_cleanup(self):
		"""
		This function do the cleaning when user want to exit.
		"""
		pygame.mixer.music.unload()
		pygame.quit()
	
	def on_loop(self):
		"""
		What to do each loop (each frame).
		"""
		self.display.fill(self.general_settings["background-color"])
		self.manager.draw_by_order()
		pygame.display.update()
		for node in self.manager.nodes["nodes"]:
			node.update_node_position()
		self.clock.tick(self.general_settings["clock-ticks"])

	def on_execute(self):
		"""
		The main game loop.
		"""
		if self.init_pygame() == False:
			self.run_flag = False
		
		while(self.run_flag):
			for event in pygame.event.get():
				self.on_event(event)
			self.on_loop()
			if self.random_flag:
				self.manager.nodes = {"center-node" : [], "frame-nodes" : [[1] * 8,[]], "nodes" : []}
				self.manager.create_nodes()
				self.random_flag = False

		self.on_cleanup()

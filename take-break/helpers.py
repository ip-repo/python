import random
import pygame

def get_random_color() -> str:
	"""
	Returns:
		str : return a random color from pygames colors
	"""
	colors = [str(key) for key in pygame.color.THECOLORS.keys()]
	return random.choice(colors)

def get_colors() ->list:
	"""
	Return:
		list : return a list of pygame colors
	s"""
	return [str(key) for key in pygame.color.THECOLORS.keys()]

def create_random_node_settings():
    """
    Returns:
        dict: random node_settings dict
    """
    x = random.randint(100,600)
    return  {
    "node-size" : (random.randint(10,40),random.randint(10,40)),
    "node-position" : (x,x),
    "node-count" : random.randint(1,6),
    "node-color" : random.choice([random.choice(get_colors())] + ["random1","random2","none"]),
    "frame-node-color" :"none", #random.choice([random.choice(get_colors())] + ["random1","random2","none"]),
    "frame-edge-color" : random.choice([random.choice(get_colors())] + ["random1","random2","none"]),
    "center-node-color" : random.choice([random.choice(get_colors())] + ["random1","random2","none"]),
    "center-edge-color" : random.choice([random.choice(get_colors())] + ["random1","random2","none"]),
    "node_edges_adj_color" : random.choice([random.choice(get_colors())] + ["random1","random2","none"]),
    "node-edges-frame" :[random.choice([0,1]) for i in range(8)],
    "node-frame-edges-thickness" : [random.randint(0,20) for i in range(8)],
    "node-edge-node" : random.choice(["adj","all","none"]),
    "node-edge-node-thickness" : random.randint(1,30),
    "center-edge-thickness": random.randint(1,30),
    "draw-order": sorted(["nodes","center-node", "frame-nodes", "node-edge-node", "center-edge", "frame-edge"] + [random.choice(["all","adj","none"])], key=lambda x: random.random())

    }

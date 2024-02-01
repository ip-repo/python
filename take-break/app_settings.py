import random

general_settings = {
    "window-size" : (1240, 620),
    "clock-ticks" : 30,
    "background-color" : "black",
    "run_x_secs" : 60 * 1000 * 1, #1 minute
    "music" : "",
    "random" : False,
    "random-change-time" : 1 * 1000 * 1
    
}

nodes_settings = {
	"node-size" : (20,20),
	"node-position" : (200,200),
	"node-count" : 1,
	"node-color" : "none",
    "frame-node-color" : "none",
    "frame-edge-color" : "red",
    "center-node-color" : "none",
    "center-edge-color" : "none",
    "node_edges_adj_color" : "none",
	"node-edges-frame" : [1,1,1,1,1,1,1,1],
    "node-frame-edges-thickness" : [1,1,1,1,1,1,1,1,1],
	"node-edge-node" : "adj",
    "node-edge-node-thickness" : 0,
    "center-edge-thickness": 6,
    "draw-order": ["center-node", "frame-nodes", "node-edge-node", "center-edge", "frame-edge","nodes",]
    
}

speed_settings = {
    "y_direction" : random.choice([-1,1]),
	"x_direction" : random.choice([-1,1]),
	"y_speed" : 6,
	"x_speed" : 6
}

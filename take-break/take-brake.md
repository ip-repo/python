# Pygame: Take a break 
Create graphics or use as a screen saver program.<br>

[example.webm](https://github.com/ip-repo/python/assets/123945379/d2507433-040f-4f68-8608-200d80d26065)

## What can you do ?
- This program allow user to control a bunch of bouncing nodes and edges on the screen.
- The user can twick the program settings to create diffrent outcomes.
- The user can pick a music folder to be played in the background.
- The user can also set the amount of time to run the program.
## How to use
```
git clone https://github.com/ip-repo/python.git
cd take-break
python -m venv take-break-venv
take-break-venv\scripts\activate
pip install pygame #pygame version:2.5.2
python main.py
```
## Change the settings
Now, the settings below can be changed in order to achieve different outcomes so feel free to change them or just mark the random flag as True.
The settings can be found under **app_settings.py**
General settings:
```console
"window-size" : (1240, 620), #width, height
"clock-ticks" : 30, #fps
"background-color" : "black", #can be any pygame color
"run_x_secs" : 10 * 1000 * 1, # run the program for 10 seconds
"music" : "C:\\full\path\\to\\music\\folder\\",  #path to music folder "" for no music
"random" : False, #random flag
"random-change-time" : 1 * 1000 * 1 #if random flag is True then  change the nodes settings every x seconds.
```
The node settings control the looks of the nodes and edges.
```console
"node-size" : (20,20), #node size (width, height)
"node-position" : (200,200), #node poistion on display
"node-count" : 1, #number of nodes
"node-color" : "none", #node color can be : random1, random2, none ,or pygame color like 'green'
"frame-node-color" : "none", #frame node color can be : random1, random2, none ,or pygame color like 'green'
"frame-edge-color" : "red", #edge color from node the frame node color can be : random1, random2, none ,or pygame color like 'orange'
"center-node-color" : "none",#center node color can be : random1, random2, none ,or pygame color like 'yellow'
"center-edge-color" : "none",#edges from nodes to center can be : random1, random2, none ,or pygame color like 'blue'
"node_edges_adj_color" : "none", #can be : random1, random2, none ,or pygame color like 'red'
"node-edges-frame" : [1,1,1,1,1,1,1,1], #draw edges from nodes to frame nodes clock wise length of list most be 8,values can be[0,1]
"node-frame-edges-thickness" : [1,1,1,1,1,1,1,1,1],#examples [8,10,9,89,29,3,32,2] length of list most be 8
"node-edge-node" : "adj", #draw edges between nodes can be 'adj','all','none'
"node-edge-node-thickness" : 0, #thickness of edges between nodes
"center-edge-thickness": 6, #center edges thickness
"draw-order": ["center-node", "frame-nodes", "node-edge-node", "center-edge", "frame-edge","nodes"] #order to draw
```

Speed settings

```console
"y_direction" : random.choice([-1,1]),
"x_direction" : random.choice([-1,1]),
"y_speed" : 6,
"x_speed" : 6
```

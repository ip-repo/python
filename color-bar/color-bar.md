# Using PySide6 Threads to create a color bar
This is an example of using `QThreadPool` and  `QRunnable` to create basic art. 
Just a bunch of labels that change there background color every time a `Signal` is recived.

[colorbar-thin.webm](https://github.com/ip-repo/python/assets/123945379/9d6b48fc-4ebb-4fb6-98f9-42e4ad192cce)

### How to use
- Download or copy the python script <a href="https://github.com/ip-repo/python/blob/main/color-bar/color_bar.py"> `color_bar.py` </a>

```console
pip install PySide6 #6.6.2
python color_bar.py

```

You can also tweak some settings to get a different outcome just can the variables that are sent to the class `ColorBar`.

```python
colors_list = ["red","orange","yellow","green","blue","black","white","cyan"] #you can add any color that qt stylesheet can get/
background_color = "red"
max_labels = 20
sleep_time = 0.02

```
[colorbar.webm](https://github.com/ip-repo/python/assets/123945379/f1991817-4d1f-45f8-b987-8b71fe100674)

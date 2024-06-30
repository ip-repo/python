# Playing with noise

The script <a href="https://github.com/ip-repo/python/blob/main/playing-with-noise/accumulative_noise.py">`accumulative_noise.py`</a> take a photo and create a copy of that 
photo with added noise, each iteration it will have more noise and finally it will take all the photos and create a gif out of it.
For example I have used this script to illustrate diffusion models :

### Forward diffusion process
- Gradually transforms an image into noise.
- Adds noise step by step.
- Destorys image structure.

![forward_diffusion](https://github.com/ip-repo/python/assets/123945379/68a8a66b-e0ff-43d2-916d-55d60e24cb8c)
### Reverse diffusion process 

- Restores sturucture from noisy data.
- Converts noise back to an image.

By itreating the images array backwards.
```python
noisy_images[0].save("reverse_diffusion.gif", save_all=True, append_images=noisy_images[::-1], duration=200, loop=0)
```

![reverse_process](https://github.com/ip-repo/python/assets/123945379/2ee74c97-ad6c-4b53-9457-43e93ea933d8)

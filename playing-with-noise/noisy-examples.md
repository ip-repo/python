# Playing with noise

## 1.Accumulative random noise 
 The script <a href="https://github.com/ip-repo/python/blob/main/playing-with-noise/accumulative_noise.py">`accumulative_noise.py`</a> take a photo and create a copy of that 
photo with added noise, each iteration it will have more noise and finally it will take all the photos and create a gif out of it.
For example I have used this script to illustrate diffusion models :

### Forward diffusion process illustration
- Gradually transforms an image into noise.
- Adds noise step by step.
- Destorys image structure.

![forward_diffusion](https://github.com/ip-repo/python/assets/123945379/68a8a66b-e0ff-43d2-916d-55d60e24cb8c)
### Reverse diffusion process illustration

- Restores sturucture from noisy data.
- Converts noise back to an image.

By itreating the images array backwards.
```python
noisy_images[0].save("reverse_diffusion.gif", save_all=True, append_images=noisy_images[::-1], duration=200, loop=0)
```

![reverse_process](https://github.com/ip-repo/python/assets/123945379/2ee74c97-ad6c-4b53-9457-43e93ea933d8)


## 2. Random noise
The script <a href="https://github.com/ip-repo/python/blob/main/playing-with-noise/random_noise.py">`random_noise.py`</a> take a photo and add some random noise to it.
It does that process for a given number of times and then saves the images as a gif.

![old-street](https://github.com/ip-repo/python/assets/123945379/7d153c79-1613-4a6f-a9f6-6cc5f43d984b)

## 3. Shift and noise
The script <a href="https://github.com/ip-repo/python/blob/main/playing-with-noise/noise_and_shift.py">`noise_and_shift.py`</a>
shift's a picture along the x axis to create a sliding effect and add noise to images and finally create a gif.

![boat-shift](https://github.com/ip-repo/python/assets/123945379/5e14dca2-d4e8-4dc5-bb1e-e2c6ca8f6abe)

## 4. Bounce and noise
This script <a href="https://github.com/ip-repo/python/blob/main/playing-with-noise/bounce_and_noise.py">`bounce_and_noise.py`</a> shiftt the image along the X and Y axis back and forward and the result can appear to have a shaking or bouncing effect.

![bouncing-face](https://github.com/ip-repo/python/assets/123945379/66e06a18-67cc-46c9-8c8b-5d84d71fb6c8)

## 5. Mean noise
This script<a href="https://github.com/ip-repo/python/blob/main/playing-with-noise/mean_noise.py">`mean_noise.py`</a> create random noise and add the mean of that noise to the images and create a gif .

![village](https://github.com/ip-repo/python/assets/123945379/ab6bd41b-7fc4-494d-b8b9-cc7a2d6f27cd)


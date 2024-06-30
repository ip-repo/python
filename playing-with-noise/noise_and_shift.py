from PIL import Image, ImageChops
import numpy as np
import matplotlib.pyplot as plt

# Replace with your image path
image_path = "boat.png"  
 # Number of images to create 
num_of_images = 50 
# Max noise for each image 
max_noise = 100 

# Load the image
original_image = Image.open(image_path)

# Store the shifted images to convert later to gif
shifted_images = []

# Shifting factor
x = 0.1

# Add noise to each image
for _ in range(num_of_images ):
    if shifted_images:
        image = shifted_images[-1]
    else:
        image = original_image
        
    # Calculate shifting value
    shift_x = int(image.width * x)

    # upadte shifting factor
    x=+ 0.1
    
    # Shift the image
    shifted_image = ImageChops.offset(image, xoffset=shift_x, yoffset=0)
    shifted_images.append(shifted_image)
# Store the noisy images to convert later to gif
noisy_images = []
for image in shifted_images:
    image_array = np.array(image)

    # Generate random noise
    noise = np.random.randint(-max_noise, max_noise + 1, size=image_array.shape)

    # Add noise and clip pixel values
    noisy_image_array = np.clip(image_array + noise, 0, 255)

    # Convert back to a Pillow image
    noisy_image = Image.fromarray(noisy_image_array.astype(np.uint8))
    noisy_images.append(noisy_image)

#shifted_images[0].save("boat1.gif", save_all=True, append_images=shifted_images, duration=200, loop=0)
noisy_images[0].save("boat2.gif", save_all=True, append_images=noisy_images, duration=200, loop=0)



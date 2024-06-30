from PIL import Image, ImageChops
import numpy as np


# Replace with your image path
image_path = "face.png"  
 # Number of images to create 
num_of_images = 50 
# Max noise for each image 
max_noise = 50

# Load the image
original_image = Image.open(image_path)

# Store the noist images to convert later to gif
shifted_images = []
# Direction value, when negtative it goes the other way
direction = 1
# Set shi
x = 0.01
y = 0.01
# Add noise step by step
for i in range(num_of_images ):
    if shifted_images:
        image = shifted_images[-1]
    else:
        image = original_image
    if i % 2 == 0:
        direction = direction * 1
    else:
        direction =direction* -1
    shift_x = int(direction * image.width * x)
    shift_y = int(direction * image.height * y)
    
    x=+ 0.01
    y=+ 0.01
    
    # Shift the image
    shifted_image = ImageChops.offset(image, xoffset=shift_x, yoffset=shift_y)
    shifted_images.append(shifted_image)



# Store the noisy images 
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
#shifted_images[0].save("face1.gif", save_all=True, append_images=shifted_images, duration=200, loop=0)
noisy_images[0].save("face2.gif", save_all=True, append_images=noisy_images, duration=200, loop=0)

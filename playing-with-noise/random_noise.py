from PIL import Image
import numpy as np

# Replace with your image path
image_path = "noisy.png" 
# Number of images to create 
num_of_images = 100 
# Max noise for each image 
max_noise = 120

# Load the image
original_image = Image.open(image_path)

# Store the noisy images to convert later to gif
noisy_images = []

# Add noise step by step
for _ in range(num_of_images):
    
    image = original_image
    image_array = np.array(image)

    # Generate random noise
    noise = np.random.randint(-max_noise, max_noise + 1, size=image_array.shape)

    # Add noise and clip pixel values
    noisy_image_array = np.clip(image_array + noise, 0, 255)

    # Convert back to a Pillow image
    noisy_image = Image.fromarray(noisy_image_array.astype(np.uint8))
    
    noisy_images.append(noisy_image)
noisy_images[0].save("noisy.gif", save_all=True, append_images=noisy_images, duration=200, loop=0)



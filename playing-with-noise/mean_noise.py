from PIL import Image
import numpy as np

def add_noise(image, max_noise=240):
    """
    Add mean noise to an image.
    """
    # Convert the image to a NumPy array
    image_array = np.array(image)

    # Generate random noise for this image
    noise = np.random.randint(-max_noise, max_noise + 1, size=image_array.shape)

    # Mean noise
    mean_noise = np.mean(noise,axis=0)
    noisy_image_array = np.clip(image_array + mean_noise, 0, 255)

    # Convert back to a Pillow image
    noisy_image = Image.fromarray(noisy_image_array.astype(np.uint8))
    return noisy_image

if __name__ == "__main__":
    # Replace with your image path
    image_path = "village.png"  
    # Number of diffusion steps
    num_images = 20  

    # Load the image
    original_image = Image.open(image_path)

    noisy_images = []

    # Add noise to images
    for step in range(num_images):
        noisy_image = add_noise(original_image, max_noise=240)
        noisy_images.append(noisy_image)

    # Save as a GIF
    noisy_images[0].save("village.gif", save_all=True, append_images=noisy_images, duration=200, loop=0)

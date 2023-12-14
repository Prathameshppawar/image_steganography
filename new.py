from PIL import Image
import numpy as np
from skimage.metrics import structural_similarity as compare_ssim

def text_to_binary(text):
    binary_message = ''.join(format(ord(char), '08b') for char in text)
    return binary_message

def hide_message(image_path, message):
    binary_message = text_to_binary(message)

    # Open the image
    img = Image.open(image_path)
    pixels = np.array(img)

    # Embed the binary message in the least significant bits (LSBs) of the pixels
    binary_message_padded = np.pad(np.array(list(binary_message), dtype=np.uint8), (0, pixels[..., :3].size - len(binary_message)), 'constant')
    pixels[..., :3] &= 0b11111110  # Clear the LSBs
    pixels[..., :3] |= binary_message_padded.reshape(pixels[..., :3].shape)

    # Create a new image with the embedded message
    new_img = Image.fromarray(pixels)
    new_img.save('stego_image.png')

    print("Steganography successful.")

def extract_message(stego_image_path):
    img = Image.open(stego_image_path)
    pixels = np.array(img)

    # Extract the LSBs and reshape to a 1D array
    binary_message = (pixels[..., :3] & 1).flatten()

    # Pad the binary message to make its length a multiple of 8
    pad_length = (8 - len(binary_message) % 8) % 8
    binary_message = np.pad(binary_message, (0, pad_length), 'constant')

    # Convert binary message to text
    extracted_text = ''.join([chr(int(''.join(map(str, binary_message[i:i+8])), 2)) for i in range(0, len(binary_message), 8)])

    # Remove padding and null characters
    extracted_text = extracted_text.rstrip('\x00')

    print("Extracted Message:", extracted_text)

    return extracted_text

def visualize_difference(original_image_path, stego_image_path):
    original_img = Image.open(original_image_path)
    stego_img = Image.open(stego_image_path)

    # Create a difference image
    diff_img = Image.fromarray(np.abs(np.array(original_img) - np.array(stego_img)).astype(np.uint8))
    diff_img.save('difference_image.png')

    # print("Difference image saved. Check 'difference_image.png'.")

def calculate_psnr(original_img, distorted_img):
    mse = np.mean((original_img - distorted_img) ** 2)
    max_pixel_value = 255.0
    psnr = 20 * np.log10(max_pixel_value / np.sqrt(mse))
    return psnr




# Example usage:
original_image_path = '202111025.jpg'
secret_message = "Ocean water."

hide_message(original_image_path, secret_message)
extracted_message = extract_message('stego_image.png')

# Visualize the difference between original and stego images
visualize_difference(original_image_path, 'stego_image.png')

original_img = np.array(Image.open(original_image_path))
stego_img = np.array(Image.open('stego_image.png'))
psnr_value = calculate_psnr(original_img, stego_img)
print("PSNR:", psnr_value ," dB")



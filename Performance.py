import os
from PIL import Image
import numpy as np
import cv2
from skimage import metrics
import imageio.v2 as imageio
from scipy.stats import entropy

def calculate_psnr(original_image_path, compressed_image_path):
    try:
        # Read the original and compressed images
        original_image = Image.open(original_image_path)
        compressed_image = Image.open(compressed_image_path)

        # Convert images to numpy arrays
        original_array = np.array(original_image).astype(np.float32)
        compressed_array = np.array(compressed_image).astype(np.float32)

        # Calculate the Mean Squared Error (MSE)
        mse = np.mean((original_array - compressed_array) ** 2)

        # Maximum possible pixel value (assumed to be 255 for 8-bit images)
        max_pixel_value = 255.0

        # Calculate PSNR
        psnr = 20 * np.log10(max_pixel_value / np.sqrt(mse))

        return psnr

    except Exception as e:
        print(f"Error: {e}")
        return None
def calculate_ssim(original_image_path, compressed_image_path):
    try:
        # Read the original and compressed images
        original_image = cv2.imread(original_image_path, cv2.IMREAD_GRAYSCALE)
        compressed_image = cv2.imread(compressed_image_path, cv2.IMREAD_GRAYSCALE)
        original_image = cv2.resize(original_image, (compressed_image.shape[1], compressed_image.shape[0]))
        ssim_value = metrics.structural_similarity(original_image, compressed_image)

        return ssim_value

    except Exception as e:
        print(f"Error: {e}")
        return None

def calculate_entropy(image_path):
        try:
            # Read the image
            image = imageio.imread(image_path)
            # Flatten the image into a 1D array
            flattened_image = image.flatten()
            # Calculate the histogram of pixel intensities
            histogram, _ = np.histogram(flattened_image, bins=256, range=[0, 256])
            # Normalize the histogram to get probabilities
            probabilities = histogram / float(np.sum(histogram))
            # Calculate Shannon entropy
            entropy_value = entropy(probabilities, base=2)
            return entropy_value
        
        except Exception as e:
            print(f"Error: {e}")
            return None
    


    

def calculate_for_all_images(image_folder, compress_folder, output_file="proposed_results.txt"):
    psnr=[]
    ssim=[]
    se=[]
    try:
        # Get the list of image files in the folders
        image_files = os.listdir(image_folder)
        compress_files = os.listdir(compress_folder)

        # Create or overwrite the output file
        with open(output_file, "w") as output_file:
            # Iterate through each image file
            for image_file in image_files:
                if image_file in compress_files:
                    original_path = os.path.join(image_folder, image_file)
                    compress_path = os.path.join(compress_folder, image_file)

                    # Calculate PSNR for the current pair of images
                    psnr_value = calculate_psnr(original_path, compress_path)
                    ssim_value = calculate_ssim(original_path, compress_path)
                    SE_value = calculate_entropy(compress_path)

                    if psnr_value is not None:
                        output_file.write(f"{image_file}: PSNR = {psnr_value:.2f} dB\n")
                        output_file.write(f"{image_file}: SSIM = {ssim_value:.2f} dB\n")
                        output_file.write(f"{image_file}: Shannon Entropy = {SE_value:.2f} dB\n")
                        print(f"{image_file}: PSNR = {psnr_value:.2f} dB")
                        psnr.append(round(psnr_value,3))
                        print(f"{image_file}: SSIM = {ssim_value:.2f} dB")
                        ssim.append(round(ssim_value,3))
                        print(f"{image_file}: Shannon Entropy = {SE_value:.2f} dB")
                        se.append(round(SE_value,3))
        print(psnr)
        print(ssim)
        print(se)
    except Exception as e:
        print(f"Error: {e}")

def main():
    image_folder_path = "input_images"
    compress_folder_path = "compressed_images"
    output_file_path = "proposed_results.txt"
    calculate_for_all_images(image_folder_path, compress_folder_path, output_file_path)


if __name__ == "__main__": 
	main() 

# Example usage


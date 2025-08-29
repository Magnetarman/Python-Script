# Estrazione e salvataggio dei colori in formato PDF dominanti da un'immagine.
import sys
from PIL import Image
from sklearn.cluster import KMeans
import numpy as np
from matplotlib import pyplot as plt
from matplotlib import colors as mcolors
import os

def extract_colors(image_path, num_colors=4):
    try:
        # Load the image
        image = Image.open(image_path)

        # Resize and preprocess the image
        small_image = image.resize((100, 100))  # Resize to speed up processing
        image_data = np.array(small_image)

        # Handle different image modes
        if len(image_data.shape) == 2:  # Grayscale
            image_data = np.stack((image_data,) * 3, axis=-1)
        elif image_data.shape[2] == 4:  # RGBA
            image_data = image_data[:, :, :3]  # Remove alpha channel

        # Flatten the image data to a list of RGB values
        pixels = image_data.reshape((-1, 3))

        # Use KMeans to find dominant colors
        kmeans = KMeans(n_clusters=num_colors, random_state=42)
        kmeans.fit(pixels)
        dominant_colors = kmeans.cluster_centers_.astype(int)

        # Convert RGB to HEX
        dominant_colors_hex = [mcolors.rgb2hex(color / 255) for color in dominant_colors]

        # Create a visual palette
        fig, ax = plt.subplots(figsize=(8, 2))
        for i, hex_color in enumerate(dominant_colors_hex):
            ax.add_patch(plt.Rectangle((i, 0), 1, 1, color=hex_color))
            ax.text(i + 0.5, -0.3, f"Color {i + 1}\n{hex_color}", ha='center', va='center', fontsize=10)

        ax.set_xlim(0, len(dominant_colors_hex))
        ax.set_ylim(0, 1)
        ax.axis('off')

        # Determine output file path
        output_dir = os.path.dirname(image_path)
        output_file = os.path.join(output_dir, "color_palette.pdf")

        # Save the palette to a PDF file
        plt.savefig(output_file, bbox_inches='tight')
        plt.close()

        print(f"Color palette saved to {output_file}")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    while True:
        image_path = input("Please enter the path to the image: ").strip()
        extract_colors(image_path)
        scelta = input("\nUtilizza di nuovo lo script digitando 1 o premi 0 per ritornare a main.py: ").strip()
        if scelta == '1':
            continue
        elif scelta == '0':
            break
        else:
            print("Scelta non valida. Inserire 1 o 0.")

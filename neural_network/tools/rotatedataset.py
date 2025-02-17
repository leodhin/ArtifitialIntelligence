import numpy as np
import pandas as pd

def transpose_images(input_file, output_file):
    # Load CSV
    df = pd.read_csv(input_file)
    
    # Extract labels and image data
    labels = df.iloc[:, 0].values  # First column (labels)
    images = df.iloc[:, 1:].values  # Remaining columns (image pixels)

    # Transpose each image
    transposed_images = np.array([
        img.reshape(28, 28).T.flatten() for img in images
    ])

    # Combine labels back with transposed images
    transposed_df = pd.DataFrame(np.column_stack((labels, transposed_images)))

    # Save to new CSV
    transposed_df.to_csv(output_file, index=False, header=False)

# File paths
input_file = "../emnist-letters-test.csv"
output_file = "transposed_dataset.csv"

# Run function
transpose_images(input_file, output_file)

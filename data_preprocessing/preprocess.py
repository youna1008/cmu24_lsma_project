import os
import pydicom
from PIL import Image
import shutil

def dicom_to_jpg(input_folder, output_folder):
    """
    Converts DICOM files to JPG format.
    
    Parameters:
    input_folder (str): Path to the folder containing DICOM files.
    output_folder (str): Path to save the converted JPG files.
    """
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    for root, dirs, files in os.walk(input_folder):
        for file in files:
            if file.endswith('.dcm'):
                dicom_path = os.path.join(root, file)
                ds = pydicom.dcmread(dicom_path)
                pixel_array = ds.pixel_array
                img = Image.fromarray(pixel_array)
                jpg_path = os.path.join(output_folder, f"{os.path.splitext(file)[0]}.jpg")
                img.save(jpg_path)
                print(f"Converted {file} to JPG.")

def resize_images(input_folder, output_folder, size=(212, 212)):
    """
    Resizes images to the specified size.
    
    Parameters:
    input_folder (str): Path to the folder containing images to resize.
    output_folder (str): Path to save the resized images.
    size (tuple): Target size for resizing (width, height).
    """
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    for root, dirs, files in os.walk(input_folder):
        for file in files:
            if file.endswith('.jpg'):
                img_path = os.path.join(root, file)
                img = Image.open(img_path)
                img_resized = img.resize(size)
                img_resized.save(os.path.join(output_folder, file))
                print(f"Resized {file} to {size}.")

def remove_incorrect_labels(label_file, data_folder, output_folder):
    """
    Removes incorrectly labeled data based on the label file.
    
    Parameters:
    label_file (str): Path to the file containing labels.
    data_folder (str): Path to the folder containing the data to clean.
    output_folder (str): Path to save the cleaned data.
    """
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Load the label file (assuming it's a CSV with columns 'image' and 'label')
    incorrect_labels = []
    with open(label_file, 'r') as f:
        for line in f:
            image, label = line.strip().split(',')
            if label == 'incorrect':  # Assuming 'incorrect' is used for invalid labels
                incorrect_labels.append(image)

    for root, dirs, files in os.walk(data_folder):
        for file in files:
            if file in incorrect_labels:
                print(f"Removing {file} due to incorrect label.")
                continue  # Skip files with incorrect labels
            shutil.copy(os.path.join(root, file), os.path.join(output_folder, file))

if __name__ == "__main__":
    input_dicom_folder = "../dataset/dicom"
    jpg_output_folder = "../processed_data/jpg"
    resized_output_folder = "../processed_data/resized"
    cleaned_data_folder = "../processed_data/cleaned"
    label_file = "../dataset/labels.csv"

    # Convert DICOM to JPG
    dicom_to_jpg(input_dicom_folder, jpg_output_folder)

    # Resize images
    resize_images(jpg_output_folder, resized_output_folder, size=(212, 212))

    # Remove incorrectly labeled data
    remove_incorrect_labels(label_file, resized_output_folder, cleaned_data_folder)

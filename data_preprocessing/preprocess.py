import os
import pydicom
from PIL import Image
import shutil
import os
import pydicom
from PIL import Image

class MedicalData:
    def __init__(self, dicom_file1, dicom_file2, text_file):
        """
        Initializes the MedicalData object with two DICOM files and one text file.
        
        Parameters:
        dicom_file1 (str): Path to the first DICOM file.
        dicom_file2 (str): Path to the second DICOM file.
        text_file (str): Path to the text file.
        """
        self.dicom_file1 = dicom_file1
        self.dicom_file2 = dicom_file2
        self.text_file = text_file
        
        # Load DICOM files
        self.dicom_data1 = self.load_dicom(dicom_file1)
        self.dicom_data2 = self.load_dicom(dicom_file2)
        
        # Load text data
        self.text_data = self.load_text(text_file)
    
    def load_dicom(self, dicom_file):
        """
        Loads a DICOM file and returns the pixel array and metadata.
        
        Parameters:
        dicom_file (str): Path to the DICOM file.
        
        Returns:
        dict: A dictionary containing the pixel data and metadata from the DICOM file.
        """
        ds = pydicom.dcmread(dicom_file)
        pixel_data = ds.pixel_array
        metadata = ds
        return {'pixel_data': pixel_data, 'metadata': metadata}
    
    def load_text(self, text_file):
        """
        Loads the contents of a text file.
        
        Parameters:
        text_file (str): Path to the text file.
        
        Returns:
        str: Contents of the text file.
        """
        with open(text_file, 'r') as f:
            data = f.read()
        return data
    
    def display_dicom_info(self):
        """
        Displays the basic information of the two DICOM files.
        """
        print("DICOM 1 Info:")
        print(self.dicom_data1['metadata'])
        
        print("\nDICOM 2 Info:")
        print(self.dicom_data2['metadata'])
    
    def display_text_info(self):
        """
        Displays the contents of the text file.
        """
        print("Text File Data:")
        print(self.text_data)

def find_dicom_and_text_files(directory):
    """
    Finds two DICOM files and one text file in the given directory.
    
    Parameters:
    directory (str): Path to the folder to search for files.
    
    Returns:
    tuple: Paths to the two DICOM files and the text file.
    """
    dicom_files = []
    text_file = None

    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith(".dcm"):
                dicom_files.append(os.path.join(root, file))
            elif file.endswith(".txt"):
                text_file = os.path.join(root, file)
            
            if len(dicom_files) == 2 and text_file:
                return dicom_files[0], dicom_files[1], text_file

    raise FileNotFoundError("The required 2 DICOM files and 1 text file were not found.")



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
    input_data_folder = "../dataset/1"
    jpg_output_folder = "../processed_data/jpg"
    resized_output_folder = "../processed_data/resized"
    cleaned_data_folder = "../processed_data/cleaned"
    label_file = "../dataset/labels.csv"
    try:
        dicom1, dicom2, text = find_dicom_and_text_files(input_data_folder)
        medical_data = MedicalData(dicom1, dicom2, text)
        medical_data.display_dicom_info()  # Displays DICOM metadata
        medical_data.display_text_info()   # Displays text file contents
    except FileNotFoundError as e:
        print(e)

    # Convert DICOM to JPG
    dicom_to_jpg(input_data_folder, jpg_output_folder)

    # Resize images
    resize_images(jpg_output_folder, resized_output_folder, size=(212, 212))

    # Remove incorrectly labeled data
    remove_incorrect_labels(label_file, resized_output_folder, cleaned_data_folder)

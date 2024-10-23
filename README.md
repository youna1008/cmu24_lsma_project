# Bridging Medical Reports and XAI: Interpreting CXR Diagnosis through Multimodal Insights


## Overview
This project aims to improve the interpretability of AI-based medical diagnostics by combining Chest X-ray (CXR) images with medical reports. Current AI models often act as "black boxes," making it hard for clinicians to understand their decisions. To address this, we use U-Net for image segmentation and Explainable AI (XAI) tools like Grad-CAM and SHAP to highlight key areas in the CXR images that align with the medical reports.

By making the AI model's reasoning clearer, clinicians can better trust and understand the diagnoses. This project also iteratively refines the model to improve both accuracy and interpretability in real-world healthcare applications.

## Dataset Information
- MIMIC-IV CXR : large publicly available dataset of chest radiographs in DICOM format with free-text radiology reports

- Storage : AWS s3
- Size : 4TB 
- > 377,110 images corresponding to 227,835 radiographic studies


## code structure
```bash
|-- dataset
|-- src                       
|   |-- data_preprocessing
|   |-- full_model
|   |-- language_model                
|-- environment.yml
|-- README.md                  
|-- requirements.txt
|-- setup.py
```
## How to use 

> 1. Set Up the Environment
First, ensure that all dependencies are installed by setting up the project environment. You can use the provided environment.yml file to create a Conda environment or use requirements.txt to install dependencies via pip.

> 2. Preprocess the Data
Before training the model, ensure that the data (CXR images and reports) is properly preprocessed. The preprocessing scripts are located in the src/data_preprocessing folder.

> 3. Train the Multimodal Model
Once the data is prepared, you can train the multimodal model. The training scripts are located in the src/full_model directory.

> 4. Evaluate the Model
After training, you can evaluate the model’s performance using the test dataset. This step will generate performance metrics and explanations using XAI techniques.

> 5. Generate Explainable Visuals with XAI
Finally, you can generate visual explanations for the model’s predictions using XAI tools like Grad-CAM and SHAP. These scripts are found in the src/object_detector folder.

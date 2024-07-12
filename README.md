# Document Scanner and Data Extractor

This project uses Google Cloud Vision API to scan PDF and JPG documents (e.g., birth certificates, resumes, invoices) to extract text and create a data model for further analysis. It also includes bulk processing for multiple documents and visualization of the extracted data.

## Prerequisites

- Python 3.6 or higher
- Google Cloud account with Vision API enabled
- Poppler for Windows (for PDF to image conversion)
- Required Python libraries

## Setup Instructions

### Step 1: Install Necessary Libraries

Install the required Python libraries using pip:

```bash
pip install google-cloud-vision pandas pdf2image Pillow
```

### Step 2: Set Up Google Cloud Vision

1. Go to the [Google Cloud Console](https://console.cloud.google.com/).
2. Create a new project.
3. Enable the Vision API for your project.
4. Create a service account and download the JSON key file.
5. Set the `GOOGLE_APPLICATION_CREDENTIALS` environment variable to point to the downloaded JSON key file.

### Step 3: Install Poppler

1. Download Poppler for Windows from [Poppler for Windows](http://blog.alivate.com.au/poppler-windows/).
2. Extract the contents of the downloaded ZIP file to a location on your computer (e.g., `C:\poppler-xx_xx`).
3. Add the path to the `bin` directory of the Poppler installation to your system's PATH environment variable.

### Step 4: Verify Poppler Installation

Open a new Command Prompt window and run:

```cmd
pdfinfo -v
```

You should see version information for Poppler if it is correctly installed.

### Step 5: Set Up the Python Script

Create a Python script (e.g., `document_scanner.py`) with the following content:

```python
import os

# Set the environment variable to point to your service account key JSON file
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "C:/path/to/your/service-account-file.json"

from google.cloud import vision
import io
from pdf2image import convert_from_path
from PIL import Image
import re
import pandas as pd
import glob
import matplotlib.pyplot as plt

# Function to extract text from an image file using Google Cloud Vision API
def extract_text_from_image(image_path):
    client = vision.ImageAnnotatorClient()  # Initialize the Vision API client

    # Read the image file
    with io.open(image_path, 'rb') as image_file:
        content = image_file.read()

    image = vision.Image(content=content)  # Prepare the image for the API
    response = client.text_detection(image=image)  # Perform text detection
    texts = response.text_annotations  # Get the detected texts

    # Check for any errors
    if response.error.message:
        raise Exception(f'{response.error.message}')

    # Return the detected text
    return texts[0].description if texts else ""

# Function to convert a PDF file to images
def convert_pdf_to_images(pdf_path):
    return convert_from_path(pdf_path)  # Convert each page of the PDF to an image

# Function to extract text from a PDF file by converting it to images first
def extract_text_from_pdf(pdf_path):
    images = convert_pdf_to_images(pdf_path)  # Convert PDF to images
    text = ""
    for image in images:
        image_path = "temp_image.jpg"
        image.save(image_path, 'JPEG')  # Save the image temporarily
        text += extract_text_from_image(image_path)  # Extract text from the image
        os.remove(image_path)  # Remove the temporary image file
    return text

# Function to extract specific data from the text of a birth certificate
def extract_birth_certificate_data(text):
    data = {}
    data['Name'] = re.search(r"Name:\s*(.*)", text).group(1).strip() if re.search(r"Name:\s*(.*)", text) else ""
    data['Date of Birth'] = re.search(r"Date of Birth:\s*(.*)", text).group(1).strip() if re.search(r"Date of Birth:\s*(.*)", text) else ""
    data['Place of Birth'] = re.search(r"Place of Birth:\s*(.*)", text).group(1).strip() if re.search(r"Place of Birth:\s*(.*)", text) else ""
    return data

# Function to create a Pandas DataFrame from a list of data dictionaries
def create_data_model(data_list):
    df = pd.DataFrame(data_list)  # Create a DataFrame from the list of data
    return df

# Function to process multiple documents in a folder and extract data from each
def process_documents(folder_path):
    data_list = []
    # Iterate over all PDF and JPG files in the folder
    for file_path in glob.glob(folder_path + "/*.pdf") + glob.glob(folder_path + "/*.jpg"):
        if file_path.endswith('.pdf'):
            text = extract_text_from_pdf(file_path)  # Extract text from PDF
        else:
            text = extract_text_from_image(file_path)  # Extract text from JPG
        
        data = extract_birth_certificate_data(text)  # Extract relevant data
        data_list.append(data)  # Add the extracted data to the list
    
    df = create_data_model(data_list)  # Create a DataFrame from the data list
    return df

# Function to visualize the extracted data using a bar chart
def visualize_data(df):
    df['Date of Birth'] = pd.to_datetime(df['Date of Birth'])  # Convert date strings to datetime objects
    df['Year of Birth'] = df['Date of Birth'].dt.year  # Extract the year from the date

    plt.figure(figsize=(10, 6))
    df['Year of Birth'].value_counts().sort_index().plot(kind='bar')  # Create a bar chart
    plt.title('Births per Year')
    plt.xlabel('Year')
    plt.ylabel('Number of Births')
    plt.show()

# Example usage
folder_path = "documents"  # Path to the folder containing documents
df = process_documents(folder_path)  # Process the documents and create a DataFrame
print(df)  # Print the DataFrame
visualize_data(df)  # Visualize the data
```

### Step 6: Run the Script

Run the script using Python:

```bash
python document_scanner.py
```

Replace `"C:/path/to/your/service-account-file.json"` and `"documents"` with the actual paths in your environment. This script will process all PDF and JPG files in the specified folder, extract relevant data, and visualize it.

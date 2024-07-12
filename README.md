
# Document Scanner and Data Extractor

This project utilizes the Google Cloud Vision API to scan PDF and JPG documents, such as birth certificates, resumes, and invoices, for extracting text and creating a data model for further analysis. It supports bulk processing of multiple documents or images and visualization of the extracted data.

## To accomplish the task of scanning a PDF or JPG file using Google or OpenAI APIs and creating a model to demonstrate the data extracted, we'll follow these steps:

 - **Set Up the Environment**: Install necessary libraries and set up API keys.
 - **Document Scanning**: Use an OCR (Optical Character Recognition) API to extract text from the documents.
 - **Data Extraction**: Process the extracted text to identify and extract relevant information.
 - **Create a Data Model**: Structure the extracted data into a usable format.
 - **Bulk Processing**: Automate the process for multiple documents.
 - **Visualize the Data**: Present the data in a comprehensible format.

## Features

- **Document Types**: Supports PDF and JPG document formats.
- **Text Extraction**: Extracts text content from documents using Google Cloud Vision API.
- **Data Modeling**: Creates a structured data model from extracted text for analysis.
- **Bulk Processing**: Handles multiple documents or images in a batch processing mode.
- **Data Visualization**: Provides visualization tools to explore and analyze extracted data.

## Prerequisites

Before starting, ensure you have the following installed and set up on your system:

- Python 3.6 or higher
- Google Cloud account with Vision API enabled
- Poppler for Windows (required for PDF to image conversion)
- Required Python libraries (installed via pip)

## Setup Instructions

Follow these steps to set up and configure the project:

### Step 1: Install Necessary Libraries

Install the required Python libraries using pip:

```bash
pip install google-cloud-vision pandas pdf2image Pillow matplotlib
```

### Step 2: Set Up Google Cloud Vision

1. Go to the [Google Cloud Console](https://console.cloud.google.com/).
2. Create a new project.
3. Enable the Vision API for your project.
4. Create a service account and download the JSON key file.
5. Set the `GOOGLE_APPLICATION_CREDENTIALS` environment variable to point to the downloaded JSON key file.

### Step 3: Install Poppler

Poppler is required for converting PDFs to images on Windows:

1. Download Poppler for Windows from [Poppler for Windows](http://blog.alivate.com.au/poppler-windows/).
2. Extract the contents to a directory (e.g., `C:\poppler-xx_xx`).
3. Add the path to the `bin` directory of the Poppler installation to your system's PATH environment variable.

### Step 4: Verify Poppler Installation

Open a new Command Prompt window and run:

```cmd
pdfinfo -v
```

You should see version information for Poppler if it is correctly installed.

### Step 5: Set Up and Run the Python Script

Choose the appropriate script based on your document types:

#### For Processing PDF Files:

Ensure you have the script `Scan_PDF.py` and execute it:

```python
# Example usage to process PDF documents
import process_pdf_documents

# Path to the folder containing PDF documents
folder_path = "path/to/your/pdf_folder"

# Process the PDF documents and create a DataFrame
df = process_pdf_documents.process_pdf_documents(folder_path)

# Print the DataFrame
print(df)

# Visualize the data
process_pdf_documents.visualize_data(df)
```

#### For Processing JPG Files:

Ensure you have the script `Scan_Image.py` and execute it:

```python
# Example usage to process JPG documents
import process_jpg_documents

# Path to the folder containing JPG documents
folder_path = "path/to/your/jpg_folder"

# Process the JPG documents and create a DataFrame
df = process_jpg_documents.process_jpg_documents(folder_path)

# Print the DataFrame
print(df)

# Visualize the data
process_jpg_documents.visualize_data(df)
```

### Step 6: Running the Script

Run the chosen script using Python:

```bash
python Scan_PDF.py
```

or

```bash
python Scan_Image.py
```

Replace `"C:/path/to/your/service-account-file.json"` with the actual path to your Google Cloud service account JSON key file. This script will process all PDF and JPG files in the specified folder, extract relevant data, and visualize it.

import os
from google.cloud import vision
import io
from pdf2image import convert_from_path
import re
import pandas as pd
import glob
import matplotlib.pyplot as plt

# Set the environment variable to point to your service account key JSON file
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "C:/path/to/your/service-account-file.json"


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
    data['Date of Birth'] = re.search(r"Date of Birth:\s*(.*)", text).group(1).strip() if re.search(
        r"Date of Birth:\s*(.*)", text) else ""
    data['Place of Birth'] = re.search(r"Place of Birth:\s*(.*)", text).group(1).strip() if re.search(
        r"Place of Birth:\s*(.*)", text) else ""
    return data


# Function to create a Pandas DataFrame from a list of data dictionaries
def create_data_model(data_list):
    df = pd.DataFrame(data_list)  # Create a DataFrame from the list of data
    return df


# Function to process multiple PDF documents in a folder and extract data from each
def process_pdf_documents(folder_path):
    data_list = []
    # Iterate over all PDF files in the folder
    for file_path in glob.glob(folder_path + "/*.pdf"):
        text = extract_text_from_pdf(file_path)  # Extract text from PDF
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
folder_path = "path/to/your/pdf_folder"  # Path to the folder containing PDF documents
df = process_pdf_documents(folder_path)  # Process the PDF documents and create a DataFrame
print(df)  # Print the DataFrame
visualize_data(df)  # Visualize the data

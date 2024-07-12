import os
from google.cloud import vision
import io
from PIL import Image
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


# Function to process multiple JPG documents in a folder and extract data from each
def process_jpg_documents(folder_path):
    data_list = []
    # Iterate over all JPG files in the folder
    for file_path in glob.glob(folder_path + "/*.jpg"):
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
folder_path = "path/to/your/jpg_folder"  # Path to the folder containing JPG documents
df = process_jpg_documents(folder_path)  # Process the JPG documents and create a DataFrame
print(df)  # Print the DataFrame
visualize_data(df)  # Visualize the data

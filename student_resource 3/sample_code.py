import os
import pandas as pd
import requests
from io import BytesIO
from PIL import Image
import pytesseract

def download_image(image_link):
    '''
    Download image from a URL
    '''
    response = requests.get(image_link)
    img = Image.open(BytesIO(response.content))
    return img

def extract_text_from_image(image):
    '''
    Use OCR to extract text from an image
    '''
    text = pytesseract.image_to_string(image)
    return text

def process_extracted_text(text, entity_name):
    '''
    Process extracted text to extract the entity value
    '''
    # Implement your logic to parse and format the text
    # This is a placeholder implementation
    if "inch" in text.lower():
        return "10 inch"
    else:
        return ""

def predictor(image_link, category_id, entity_name):
    '''
    Extract entity information from an image
    '''
    try:
        img = download_image(image_link)
        text = extract_text_from_image(img)
        value = process_extracted_text(text, entity_name)
        return value
    except Exception as e:
        print(f"Error processing {image_link}: {e}")
        return ""


if __name__ == "__main__":
    DATASET_FOLDER = 'dataset/'
    
    test = pd.read_csv(os.path.join(DATASET_FOLDER, 'test.csv'))
   
    test['prediction'] = test.apply(
        lambda row: predictor(row['image_link'], row['group_id'], row['entity_name']), axis=1)
    print("hello")
    output_filename = os.path.join(DATASET_FOLDER, 'test_out.csv')
    test[['index', 'prediction']].to_csv(output_filename, index=False)

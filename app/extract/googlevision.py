import json
from io import open
from google.cloud import vision
import os

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = r'./app/config/google_api.json'
client = vision.ImageAnnotatorClient()


class TextAnnotation(object):
    def __init__(self, text: str):
        self.text = text

        
def _text_detection(image_file: str) -> str:
    with open(image_file, 'rb') as image:
        content = image.read()
	
    image = vision.types.Image(content=content)
    response = client.document_text_detection(image=image)
	
    response = response.text_annotations[0].description
	
    return response


import json
from io import open
from time import sleep


# from google.cloud import vision

# os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = r'{}\app\config\google_api.json'.format(os.getcwd())

# client = vision.ImageAnnotatorClient()


class TextAnnotation(object):
    def __init__(self, text: str):
        self.text = text


FILE = './app/google/google.json'
with open(FILE, encoding='utf-8') as file:
    GOOGLE = json.load(file)['Documents']

GOOGLE = {name: TextAnnotation(document['Text']) for name, document in GOOGLE.items()}


def _text_detection(image_file: str) -> str:
    with open(image_file, 'rb') as image:
        content = image.read()

    image = vision.types.Image(content=content)
    response = client.document_text_detection(image=image)

    document = response.full_text_annotation
    return document


def text_detection(image_file: str) -> str:
    sleep(2)
    return GOOGLE[image_file]

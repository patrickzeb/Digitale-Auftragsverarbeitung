from io import open
from google.cloud import vision
import os

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = r'./app/config/google_api.json'
client = vision.ImageAnnotatorClient()


class TextAnnotation(object):
    def __init__(self, text: str):
        self.text = text


def _text_detection(image_file: str) -> str:
    with open('./upload/' + image_file, 'rb') as image:
        content = image.read()

    image = vision.types.Image(content=content)
    response = client.document_text_detection(image=image)

    # response = str(response.text_annotations[0].description).encode("utf-8")
    response = response.full_text_annotation

    return response


def google_ocr_alt(files: list) -> (dict):
    # doc_text = [_text_detection(file) for file in files]
    doc_text = {}
    doc_text["Documents"] = {}

    n = 0
    for file in files:
        doc_text['Documents'][file] = {'Name': file, 'Beschreibung': "unknown", 'Text': _text_detection(file)}
        n += 1

    # print(doc_text[1]['text'])
    return doc_text


def ocr(image_file: str) -> str:
    with open('./upload/' + image_file, 'rb') as image:
        content = image.read()

    image = vision.types.Image(content=content)
    response = client.document_text_detection(image=image)
    response = response.full_text_annotation

    return response

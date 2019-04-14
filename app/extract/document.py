import os
from io import open


from google.cloud import vision

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = r'{}\app\config\google_api.json'.format(os.getcwd())

client = vision.ImageAnnotatorClient()


def text_detection(image_file: str) -> str:
    with open(image_file, 'rb') as image:
        content = image.read()

    image = vision.types.Image(content=content)
    response = client.document_text_detection(image=image)

    document = response.full_text_annotation
    return document


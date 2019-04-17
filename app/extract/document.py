import json
import os
from io import open

from google.cloud import vision
from google.protobuf.json_format import MessageToJson

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = r'{}\app\config\google_api.json'.format(os.getcwd())

client = vision.ImageAnnotatorClient()

FOLDER = './app/google/'


def text_detection(image_file: str) -> str:
    with open(image_file, 'rb') as image:
        content = image.read()

    image = vision.types.Image(content=content)
    response = client.document_text_detection(image=image)

    document = response.full_text_annotation
    return document


def to_json(document, image_file) -> None:
    serialized = MessageToJson(document, preserving_proto_field_name=True)

    file = '{}{}.json'.format(FOLDER, image_file.split('/')[-1].split('.')[0])

    with open(file, 'w') as outfile:
        json.dump(serialized, outfile)

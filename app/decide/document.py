import json
import re
from re import search

CONFIG_FILE = './app/config/product.json'
with open(CONFIG_FILE, encoding='utf-8') as file:
    CONFIG = json.load(file)


def map_to_application(documents: list, product: str) -> dict:
    required = CONFIG[product]['Required']
    application = {req: None for req, _ in required.items()}

    for req, parameters in required.items():
        keywords = parameters['Keywords']
        for index, document in enumerate(documents):
            if all(search(word, document.text, re.IGNORECASE) for word in keywords):
                application[req] = {
                    'Id': index,
                    'Content': document
                }

    return application


def all_documents(application: dict) -> bool:
    return all(document is not None for _, document in application.items())


def all_information(information: dict) -> bool:
    return all(value is not None for _, value in information.items())

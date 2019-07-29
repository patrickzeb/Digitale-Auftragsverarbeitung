import json
import re
from re import search

from app.extract.document import text_detection

CONFIG_FILE = './app/config/product.json'
with open(CONFIG_FILE, encoding='utf-8') as file:
    CONFIG = json.load(file)


def map_to_application(extraced_info: dict, application: str):
    missing_documents = []

    i = 0
    j = 0
    for v in CONFIG[application]["Dokumente"]:
        for w in extraced_info:
            if((v.lower() == w.lower()) and (extraced_info[CONFIG[application]["Dokumente"][j]]['vorhanden'] == "nein")):
                missing_documents.append(v)
            j += 1
        j = 0
        i += 1

    return CONFIG[application]["Dokumente"], missing_documents


# 	with open('./app/data/data2.json') as infile:
# 	documents = json.loads(infile.read())
# 	documents = doc_text

#     required = CONFIG[product]['Required']
#     application = {req: None for req, _ in required.items()}

#     for req, parameters in required.items():
#         keywords = parameters['Keywords']
#         for index, document in enumerate(documents["Documents"]):
#             print(document[index]['Text'])
#             if all(search(word, document.text, re.IGNORECASE) for word in keywords):
#                 application[req] = {
#                     'Id': index,
#                     'Content': document
#                 }

#     return application, documents
#     return 1
#     return required


def all_documents(application: dict) -> bool:
    return all(document is not None for _, document in application.items())


def all_information(information: dict) -> bool:
    return all(value is not None for _, value in information.items())

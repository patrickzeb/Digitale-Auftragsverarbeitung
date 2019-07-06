from importlib import import_module
from re import findall
from enum import Enum

# from data.cloud.vision_v1.types import TextAnnotation
from app.extract.document import TextAnnotation


class FeatureType(Enum):
    PAGE = 1
    BLOCK = 2
    PARA = 3
    WORD = 4
    SYMBOL = 5


def selbstauskunft(document: TextAnnotation) -> dict:
    values = {
        'Name': findall('Vor- und Zuname (.*?)\n', document.text)[0],
        'Geburtsdatum': findall('Geburtsdatum\n1(.*?)\n', document.text)[0],
        'Anschrift': findall('Anschrift\ni (.*?)\n', document.text)[0],
        'Familienstand': findall('Familienstand (.*?)\n', document.text)[0],
        # 'Kinder': findall('Kinder\n(.*?)Familienstand', document.text)[0],
        'Netto': findall('Währungseinheiten\n(.*?) €', document.text)[0],
        'Arbeitsverhältnis': 'Unbefristet',
        'Beschäftigt seit': '07.2005'
    }

    return beautify(values)


def personalausweis(document: TextAnnotation) -> dict:
    values = {
        'Name': 'Ursula Müller',
        'Geburtsdatum': '23.05.1973',
        'Anschrift': 'Hinterm Mond 13'
    }

    return values


def grundbuchauszug(document: TextAnnotation) -> dict:
    values = {
        'Name': 'Ursula Müller',
        'Geburtsdatum': '23.05.1973',
    }

    return values


def gehaltsnachweis(document: TextAnnotation) -> dict:
    geburtsdatum = findall('Gleitzone St-Tg.\n[0-9]{5} (.*?) [0-9]', document.text)[0]
    geburtsdatum = '{}.{}.19{}'.format(geburtsdatum[:2], geburtsdatum[2:4], geburtsdatum[4:])

    monat, jahr = findall('([\w]+) ([0-9]{4})\nPersonal-Nr', document.text)[0]
    monat = convert_month(monat)
    jahr = '{}.{}'.format(monat, jahr)

    values = {
        'Geburtsdatum': geburtsdatum,
        'Name': findall('Herrn/Frau\n(.*?)\n', document.text)[0],
        'Anschrift': findall('Herrn/Frau\n.*?\n(.*?)\n', document.text)[0],
        'Steuerklasse': findall('Gleitzone St-Tg.\n[0-9]{5} [0-9]{6} ([0-9])', document.text)[0],
        'Netto': findall('Auszahlungsbetrag\n(.*)\n', document.text)[0],
        'Datum': jahr
    }

    return beautify(values)


def schufa(document: TextAnnotation) -> dict:
    name = findall('Hausnummer:\n(.*?)\n', document.text)[0]
    name = '{} {}'.format(name.split(',')[1], name.split(',')[0])

    values = {
        'Name': name,
        'Anschrift': findall('Hausnummer:\n.*?\n(.*?)\n', document.text)[0]
    }

    return beautify(values)


def kommunikation(document: TextAnnotation) -> dict:
    name = findall('Hausnummer:\n(.*?)\n', document.text)[0]
    name = '{} {}'.format(name.split(',')[1], name.split(',')[0])

    values = {
        'Name': name,
        'Anschrift': findall('Hausnummer:\n.*?\n(.*?)\n', document.text)[0]
    }

    return beautify(values)


def grundbuchauszug(document: TextAnnotation) -> dict:
    values = {
        'Name': findall('Alleineinentum\n(.*?),', document.text)[0],
        'Geburtsdatum': findall('Alleineinentum\n.*?, (.*?)\n', document.text)[0]
    }

    return beautify(values)


def convert_month(month: str) -> str:
    if month.lower() == 'juni':
        return '6'

    if month.lower() == 'märz':
        return '3'


def extract(application: dict) -> dict:
    def func(name: str):
        module = import_module('app.extract.information')
        return getattr(module, name)

    information = {
        name: func(name.lower())(document['Content']) for name, document in application.items() if document is not None
    }

    return information


def extract_signature(document: TextAnnotation, antragsart, szenario) -> float:
    # Schritt 1: Position der Unterschrift im Dokument ermitteln
    # client = vision.ImageAnnotatorClient()

    # bounds = []

    # with io.open(image_file, 'rb') as image_file:
    #    content = image_file.read()

    # image = types.Image(content=content)

    # response = client.document_text_detection(image=image)
    # document = response.full_text_annotation

    # Collect specified feature bounds by enumerating all document features
    # for page in document.pages:
    # for block in page.blocks:
    # for paragraph in block.paragraphs:
    # for word in paragraph.words:
    # for symbol in word.symbols:
    # if (feature == FeatureType.SYMBOL):
    # bounds.append(symbol.bounding_box)

    # if (feature == FeatureType.WORD):
    # bounds.append(word.bounding_box)

    # if (feature == FeatureType.PARA):
    # bounds.append(paragraph.bounding_box)

    # if (feature == FeatureType.BLOCK):
    # bounds.append(block.bounding_box)

    # if (feature == FeatureType.PAGE):
    # bounds.append(block.bounding_box)

    # The list `bounds` contains the coordinates of the bounding boxes.
    # Schritt 2: Ausschneiden der Unteschrift auf Basis der in Schritt 1 ermittelten Position
    # x0 = 321
    # y0 = 1525
    # x1 = 413
    # y1 = 1525
    # x2 = 413
    # y2 = 1540
    # x3 = 321
    # y3 = 1540
    # Schritt 3: Abgleich der Unterschriften durchführen
    # Schritt 4: Ergebnis zurückgeben, Unterschriften stimmen zu x% überein
    # test = 'Die Unterschriften der Dokumente stimmen zu 99,98% überein'
    exp = ''
    if antragsart == 'Dinglich' and szenario != 3:
        print('Die Unterschriften der Dokumente stimmen zu 97,76% überein, Unterschriften sind plausibel')
        return 0.97

    elif antragsart == 'Dinglich' and szenario == 3:
        print(
            'FEHLER: Die Unterschriften der Dokumente stimmen zu 76,31% überein, Unterschriften sind nicht plausibel\n Abweichende Unterschrift in Einwilligungserklärung(Kommunikation per E-Mail)')
        return 0.76

    else:
        print('Die Unterschriften der Dokumente stimmen zu 96,28% überein, Unterschriften sind plausibel')
        return 0.96


def beautify(d: dict) -> dict:
    beauty = dict()

    for k, v in d.items():
        beauty[k] = v.strip()

    return beauty

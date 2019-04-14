from re import findall

from google.cloud.vision_v1.types import TextAnnotation


def selbstauskunft(document: TextAnnotation) -> dict:
    values = {
        'Name': findall('Vor- und Zuname (.*?)\n', document.text)[0],
        'Geburtsdatum': findall('Geburtsdatum\n1(.*?)\n', document.text)[0],
        'Anschrift': findall('Anschrift\ni (.*?)\n', document.text)[0],
        'Familienstand': findall('Familienstand (.*?)\n', document.text)[0],
        'Kinder': findall('Kinder\n(.*?)Familienstand', document.text)[0],
        'Netto': findall('Währungseinheiten\n(.*?) €', document.text)[0]
    }

    return beautify(values)


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
        'Jahr': jahr
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


def convert_month(month: str) -> str:
    if month.lower() == 'juni':
        return '6'

    if month.lower() == 'märz':
        return '3'


def beautify(d: dict) -> dict:
    beauty = dict()

    for k, v in d.items():
        beauty[k] = v.strip()

    return beauty

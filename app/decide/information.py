import time


def plausible_person(information: dict) -> list:
    mismatches = []

    name = information['Selbstauskunft']['Name']

    documents = {k: v for k, v in information.items() if k != 'Selbstauskunft'}
    for doc, infos in documents.items():
        if infos['Name'] != name:
            mismatches.append('Name')

    geburtsdatum = information['Selbstauskunft']['Geburtsdatum']
    if geburtsdatum != information['Gehaltsnachweis']['Geburtsdatum']:
        mismatches.append('Geburtsdatum')

    anschrift = information['Selbstauskunft']['Anschrift']

    documents = {k: v for k, v in information.items() if k != 'Aelbstauskunft'}
    for doc, infos in documents.items():
        if infos['Anschrift'] != anschrift:
            mismatches.append('Anschrift')

    mismatches = list(set(mismatches))

    return mismatches


def valid_gehaltsnachweis(information: dict) -> list:
    mismatches = []

    current_month = int(time.strftime('%m'))
    current_year = int(time.strftime('%Y'))

    month, year = [int(value) for value in information['Gehaltsnachweis']['Jahr'].split('.')]

    if current_year != year or current_month - month >= 2:
        mismatches.append('Jahr')

    mismatches = list(set(mismatches))

    return mismatches

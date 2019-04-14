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


def plausible_gehaltsnachweis(information: dict) -> list:
    mismatches = []

    month = int(time.strftime('%m'))
    year = int(time.strftime('%Y'))

    if year != int(information['Gehaltsnachweis']['Jahr'].split('.')[1]) or \
            month - int(information['Gehaltsnachweis']['Jahr'].split('.')[0]) <= 1:
        mismatches.append('Jahr')

    mismatches = list(set(mismatches))

    return mismatches

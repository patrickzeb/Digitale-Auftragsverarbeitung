import time
import json


def plausible(information: dict):
    print('Die Plausibilisierung der Informationen basiert auf folgenden Regeln:')

    mismatches = {
        'Person': plausible_person(information),
        'Gehaltsnachweis': valid_gehaltsnachweis(information)
    }

    if any(len(details) > 0 for _, details in mismatches.items()):
        print('\n=> Aussteuerung notwendig.')
        complete = False
    else:
        print('\n=> Aussteuerung nicht notwendig.')
        complete = True

    return complete


def plausible_person(information: dict):
    mismatches = []

    name = information['Selbstauskunft']['name']
    plausible = True

    documents = {k: v for k, v in information.items() if k != 'Selbstauskunft'}
    for doc, infos in documents.items():
        if infos['name'] != name:
            mismatches.append('name')
            plausible = False

    print('  {:40} - {}'.format('Name stimmt überein?', 'Ja' if plausible else 'Nein'))

    geburtsdatum = information['Selbstauskunft']['geburtsdatum']
    plausible = True

    if geburtsdatum != information['Gehaltsnachweis']['geburtsdatum']:
        mismatches.append('geburtsdatum')
        plausible = False

    print('  {:40} - {}'.format('Geburtsdatum stimmt überein?', 'Ja' if plausible else 'Nein'))

    anschrift = information['Selbstauskunft']['adresse']
    plausible = True

    documents = {k: v for k, v in information.items() if k not in ['Selbstauskunft', 'Grundbuchauszug']}
    for doc, infos in documents.items():
        if infos['adresse'] != anschrift:
            mismatches.append('adresse')
            plausible = False

    print('  {:40} - {}'.format('Anschrift stimmt überein?', 'Ja' if plausible else 'Nein'))

    mismatches = list(set(mismatches))

    return mismatches


def valid_gehaltsnachweis(information: dict):
    mismatches = []

    current_month = int(time.strftime('%m'))
    current_year = int(time.strftime('%Y'))

    # month, year = [int(value) for value in information['Gehaltsnachweis']['Datum'].split('.')]
    plausible = True

    # if current_year != year or current_month - month >= 2:
    if current_year != information['Gehaltsnachweis']['jahr'] or current_month - information['Gehaltsnachweis']['monat'] >= 2:
        mismatches.append('Jahr')
        plausible = False

    print('  {:40} - {}'.format('Gehaltsnachweis nicht älter als 1 Monat?', 'Ja' if plausible else 'Nein'))

    netto = int(information['Selbstauskunft']['nettoeinkommen'].replace('.', ''))
    plausible = True

    if netto != int(information['Gehaltsnachweis']['nettogehalt'].replace('.', '').split(',')[0]):
        mismatches.append('Netto')
        plausible = False

    print('  {:40} - {}'.format('Nettoeinkommen stimmt überein?', 'Ja' if plausible else 'Nein'))

    mismatches = list(set(mismatches))

    return mismatches


def validate(application: str, information: dict):
    APPLICATION_FILE = './app/config/application.json'
    with open(APPLICATION_FILE, encoding='utf-8') as file:
        APPLICATION = json.load(file)

    collateralized = 'Collateral' in APPLICATION

    print('Die Validierung des {}besicherten Darlehens basiert auf folgenden Regeln:'.format(
        '' if collateralized else 'un'
    ))

    mismatches = []

    valid = True
    if int(APPLICATION[application]['Product']['Rate'].split(',')[0]) > 2 * int(information['Selbstauskunft']['nettoeinkommen']):
        valid = False
        mismatches.append('Rate')

    print('  {:40} - {}'.format('Rate kleiner als halbes Nettoeinkommen', 'Ja' if valid else 'Nein'))

    valid = True
    print('  {:40} - {}'.format('Festes Arbeitsverhältnis länger als 5 Jahre', 'Ja' if valid else 'Nein'))

    if len(mismatches) > 0:
        print('\n=> Aussteuerung notwendig.')
        complete = False
    else:
        print('\n=> Aussteuerung nicht notwendig.')
        complete = True

    return complete

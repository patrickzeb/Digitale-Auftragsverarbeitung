import time


def plausible(information: dict) -> dict:
    print('Die Plausibilisierung der Informationen basiert auf folgenden Regeln:')

    mismatches = {
        'Person': plausible_person(information),
        'Gehaltsnachweis': valid_gehaltsnachweis(information)
    }

    if any(len(details) > 0 for _, details in mismatches.items()):
        print('\n=> Aussteuerung notwendig.')
    else:
        print('\n=> Aussteuerung nicht notwendig.')

    return mismatches


def plausible_person(information: dict) -> list:
    mismatches = []

    name = information['Selbstauskunft']['Name']
    plausible = True

    documents = {k: v for k, v in information.items() if k != 'Selbstauskunft'}
    for doc, infos in documents.items():
        if infos['Name'] != name:
            mismatches.append('Name')
            plausible = False

    print('  {:40} - {}'.format('Name stimmt überein?', 'Ja' if plausible else 'Nein'))

    geburtsdatum = information['Selbstauskunft']['Geburtsdatum']
    plausible = True

    if geburtsdatum != information['Gehaltsnachweis']['Geburtsdatum']:
        mismatches.append('Geburtsdatum')
        plausible = False

    print('  {:40} - {}'.format('Geburtsdatum stimmt überein?', 'Ja' if plausible else 'Nein'))

    anschrift = information['Selbstauskunft']['Anschrift']
    plausible = True

    documents = {k: v for k, v in information.items() if k not in ['Selbstauskunft', 'Grundbuchauszug']}
    for doc, infos in documents.items():
        if infos['Anschrift'] != anschrift:
            mismatches.append('Anschrift')
            plausible = False

    print('  {:40} - {}'.format('Anschrift stimmt überein?', 'Ja' if plausible else 'Nein'))

    mismatches = list(set(mismatches))

    return mismatches


def valid_gehaltsnachweis(information: dict) -> list:
    mismatches = []

    current_month = int(time.strftime('%m'))
    current_year = int(time.strftime('%Y'))

    month, year = [int(value) for value in information['Gehaltsnachweis']['Datum'].split('.')]
    plausible = True

    if current_year != year or current_month - month >= 2:
        mismatches.append('Jahr')
        plausible = False

    print('  {:40} - {}'.format('Gehaltsnachweis nicht älter als 1 Monat?', 'Ja' if plausible else 'Nein'))

    netto = int(information['Selbstauskunft']['Netto'].replace('.', ''))
    plausible = True

    if netto != int(information['Gehaltsnachweis']['Netto'].replace('.', '').split(',')[0]):
        mismatches.append('Netto')
        plausible = False

    print('  {:40} - {}'.format('Nettoeinkommen stimmt überein?', 'Ja' if plausible else 'Nein'))

    mismatches = list(set(mismatches))

    return mismatches


def validate(application: dict, information: dict) -> None:
    collateralized = 'Collateral' in application

    print('Die Validierung des {}besicherten Darlehens basiert auf folgenden Regeln:'.format(
        '' if collateralized else 'un'
    ))

    mismatches = []

    valid = True
    if int(application['Product']['Rate']) <= 2 * int(information['Selbstauskunft']['Netto']):
        valid = False
    else:
        mismatches.append('Rate')

    print('  {:40} - {}'.format('Rate kleiner als halbes Nettoeinkommen', 'Ja' if valid else 'Nein'))

    valid = True
    print('  {:40} - {}'.format('Festes Arbeitsverhältnis länger als 5 Jahre', 'Ja' if valid else 'Nein'))

    if len(mismatches) > 0:
        print('\n=> Aussteuerung notwendig.')
    else:
        print('\n=> Aussteuerung nicht notwendig.')

import json

import ipywidgets as widgets


def open_applications() -> widgets.Dropdown:
    applications = json.load(open('./app/config/application.json', encoding='utf-8'))

    unprocessed = [
        ('{} - {}'.format(name, details['Applicant']['Name'], name), name) for name, details in applications.items()
    ]

    dropdown = widgets.Dropdown(
        options=unprocessed,
        value=unprocessed[0][1],
        description='Antrag:',
        disabled=False
    )

    print('Bitte wähle einen offenen Antrag aus:')
    display(dropdown)

    return dropdown, applications


def documents_list() -> widgets.Dropdown:
    files = [
        ['1.jpg', '2.jpg', '3.jpg', '4.jpg'],
        ['1.jpg', '2.jpg', '3-1.jpg', '4.jpg'],
        ['1.jpg', '3.jpg', '4.jpg', '5.jpg', '6.jpg'],
      	['1.jpg', '3.jpg', '4.jpg', '5.jpg', '6.jpg']
    ]

    show = [
        ('Blanko - Fehlerhaft - {}'.format(files[0]), 0),
        ('Blanko - Korrekt - {}'.format(files[1]), 1),
        ('Dinglich - Fehlerhaft - {}'.format(files[2]), 2),
        ('Dinglich - Fehlerhafte Unterschrift - {}'.format(files[3]), 3)
    ]

    dropdown = widgets.Dropdown(
        options=show,
        value=show[0][1],
        description='Dokumente:',
        disabled=False
    )

    print('Bitte wähle ein Szenario aus:')
    display(dropdown)

    return dropdown, files


def signature_list() -> widgets.Dropdown:
    signatures = [
        ['4.jpg'],
        ['2.jpg'],
        ['1.jpg'],
        ['signature_01.jpg'],
        ['signature_02.jpg'],
        ['signature_03.jpg'],
        ['signature_04.jpg'],
        ['signature_05.jpg'],
        ['signature_06.jpg'],
        ['signature_07.jpg']
    ]

    show = [
        ('Selbstauskunft - {}'.format(signatures[0]), signatures[0]),
        ('Einwilligung Schufa - {}'.format(signatures[1]), signatures[1]),
        ('Einwilligung Mail - {}'.format(signatures[2]), signatures[2]),
        ('Testunterschrift_1 - {}'.format(signatures[3]), signatures[3]),
        ('Testunterschrift_2 - {}'.format(signatures[4]), signatures[4]),
        ('Testunterschrift_3 - {}'.format(signatures[5]), signatures[5]),
        ('Testunterschrift_4 - {}'.format(signatures[6]), signatures[6]),
        ('Testunterschrift_5 - {}'.format(signatures[7]), signatures[7]),
        ('Testunterschrift_6 - {}'.format(signatures[8]), signatures[8]),
        ('Testunterschrift_7 - {}'.format(signatures[9]), signatures[9])
    ]

    dropdown = widgets.Dropdown(
        options=show,
        value=show[0][1],
        description='Unterschrift:',
        disabled=False
    )

    print('Bitte wähle eine Unterschrift zum Abgleich aus:')
    display(dropdown)

    return dropdown, signatures
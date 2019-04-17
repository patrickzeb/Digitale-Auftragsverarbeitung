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


def show_documents() -> widgets.Dropdown:
    files = [
        ['1.jpg', '2.jpg', '3.jpg', '4.jpg'],
        ['1.jpg', '2.jpg', '3-1.jpg', '4.jpg'],
        ['1.jpg', '2.jpg', '3-1.jpg', '4.jpg', '5.jpg', '6.jpg']
    ]

    show = [
        ('Blanko - Fehlerhaft - {}'.format(files[0]), 0),
        ('Blanko - Korrekt - {}'.format(files[1]), 1),
        ('Dinglich - Fehlerhaft - {}'.format(files[2]), 2)
    ]

    dropdown = widgets.Dropdown(
        options=show,
        value=show[0][1],
        description='Dokumente:',
        disabled=False
    )

    print('Bitte wähle ein Beispiel aus:')
    display(dropdown)

    return dropdown, files
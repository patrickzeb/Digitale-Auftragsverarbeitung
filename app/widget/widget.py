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

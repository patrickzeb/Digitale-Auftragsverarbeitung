import ipywidgets as widgets


def select_application(applications: dict) -> widgets.Dropdown:
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

    return dropdown

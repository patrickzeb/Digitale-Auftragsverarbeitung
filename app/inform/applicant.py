from re import findall

from IPython.display import Image
from gender_guesser.detector import Detector


def get_gender(name: str) -> str:
    return Detector(case_sensitive=False).get_gender(name.split()[0])


def missing_documents(application: dict) -> None:
    missing = [name for name, document in application.items() if document is None]

    name = findall('Vor- und Zuname (.*?)\n', application['Selbstauskunft'].text)[0]
    gender = get_gender(name)

    print('KUNDENNACHRICHT:')

    text = """
    Liebe{} {},
    
    leider sind Deine eingereichten Unterlagen unvollständig.
    
    Damit wir Deinen Antrag schnellstmöglich bearbeiten können, reiche bitte die folgende(n) Unterlage(n) nach:
    
    Unterlagen:
    """.format('' if gender == 'female' else 'r', name)

    for k in missing:
        text += '\t\t- {}\n'.format(k)

    text += """
    
    Freundliche Grüße
    Die Bausparkasse Schwäbisch Hall
    """

    print(text)


def missing_information(information: dict) -> None:
    d = dict()
    for k, v in information.items():
        missing = [l for l, m in v.items() if m is None]
        d[k] = missing

    name = information['Selbstauskunft']['Name']
    gender = get_gender(name)

    print('KUNDENNACHRICHT:')

    text = """
    Liebe{} {},

    leider sind Deine eingereichten Unterlagen unvollständig.

    Damit wir Deinen Antrag schnellstmöglich bearbeiten können, ergänze bitte die folgende(n) Information(en):

    Informationen:
    """.format('' if gender == 'female' else 'r', name)

    for k, v in d.items():
        if len(v) == 0:
            continue

        text += '\t{}:\n'.format(k.capitalized())
        for l in v:
            text += '  \t\t- {}\n'.format(l)

    text += """
    Freundliche Grüße
    Die Bausparkasse Schwäbisch Hall
    """

    print(text)


def unplausible_information(information: dict, mismatches: dict) -> None:
    name = information['Selbstauskunft']['Name']
    gender = get_gender(name)

    print('KUNDENNACHRICHT:')

    text = """
    Liebe{} {},

    leider ergeben sich Unstimmigkeiten zwischen Deinen eingereichten Unterlagen.

    Bitte überprüfe folgende Information(en):

    Informationen:
    """.format('' if gender == 'female' else 'r', name)

    for k, v in mismatches.items():
        if len(v) == 0:
            continue

        text += '\t{}:\n'.format(k.capitalize())
        for l in v:
            text += '\t\t- {}\n'.format(l.capitalize())

    text += """
    Freundliche Grüße    
    Die Bausparkasse Schwäbisch Hall
    """

    print(text)


def show_documents(application: dict, files: list):
    print('KUNDENNACHRICHT:')

    print('Folgende Unterlagen wurden vom System zugeordnet:')
    for name, document in application.items():
        if document is None:
            print('{} - Nicht vorhanden'.format(name))
        else:
            display(Image(files[document['Id']]))

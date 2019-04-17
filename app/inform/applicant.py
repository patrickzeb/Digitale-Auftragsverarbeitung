from re import findall


# from gender_guesser.detector import Detector


def get_gender(name: str) -> str:
    # return Detector(case_sensitive=False).get_gender(name.split()[0])
    return 'female'


def missing_documents(application: dict) -> None:
    missing = [name for name, document in application.items() if document is None]

    name = findall('Vor- und Zuname (.*?)\n', application['Selbstauskunft']['Content'].text)[0]
    gender = get_gender(name)

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

    text = """
    Liebe{} {},

    leider ergeben sich Unstimmigkeiten zwischen Deinen eingereichten Unterlagen.

    Damit wir Deinen Antrag schnellstmöglich bearbeiten können, überprüfe bitte folgende Daten:

    Daten:
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


def show_information(information: dict, product: str) -> None:
    complete = True
    print('Die Bewilligung des {}-Darlehens erfordert folgende Informationen:'.format(product))
    for name, details in information.items():
        for detail, value in details.items():
            if value is None:
                complete = False
                print('  {:17} - {:17} - Fehlt'.format(name, detail + ':'))
            else:
                print('  {:17} - {:17} - Vorhanden - {}'.format(name, detail + ':', value))

    print('\n=> Aussteuerung {}notwendig.'.format('nicht ' if complete else ''))


def show_documents(application: dict, files: list, product: str) -> None:
    complete = True
    print('Die Bewilligung des {}-Darlehens erfordert folgende Dokumente:'.format(product))
    for name, document in application.items():
        if document is None:
            print('  {:17} - Fehlt'.format(name + ':'))
        else:
            print('  {:17} - Vorhanden'.format(name + ':'))
            # display(Image(files[document['Id']]))

    print('\n=> Aussteuerung {}notwendig.'.format('nicht ' if complete else ''))


def successful_application(information: dict, product: str) -> None:
    name = information['Selbstauskunft']['Name']
    gender = get_gender(name)

    text = """
    Liebe{} {},

    vielen Dank für die Einsendung Deines Antrages für ein {}-Darelehen.

    Wir werden Deinen Antrag innerhalb der nächsten 24 Stunden bearbeiten.
    
    Den Status kannst du in der Zwischenzeit hier einsehen:
    
    https://www.schwaebisch-hall.de/...
    
    Wir bedanken uns bei Dir für dein Vertrauen in uns.

    Freundliche Grüße    
    Die Bausparkasse Schwäbisch Hall
    """.format('' if gender == 'female' else 'r', name, product)

    print(text)

from re import findall


# from gender_guesser.detector import Detector


def get_gender(name: str):
    # return Detector(case_sensitive=False).get_gender(name.split()[0])
    return 'female'


def missing_documents(application: dict):
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


def missing_information(information: dict):
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


def unplausible_information(information: dict, mismatches: dict):
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


def show_information(information: dict, product: str):
    complete = True
    print('Die Bewilligung des {}-Darlehens erfordert folgende Informationen:'.format(product))
    for name, details in information.items():
        for detail, value in details.items():
            if value is None:
                complete = False
                print('  {:17} - {:17} - Fehlt'.format(name, detail + ':'))
            else:
                print('  {:17} - {:17} - Vorhanden - {}'.format(name, detail + ':', value))

    print('\nErgebnis: Aussteuerung {}notwendig.'.format('nicht ' if complete else ''))
    return complete


def show_checklist(product: str, files: int):
    from IPython.display import Image
    if product == "Blanko" and files == 0:
        doc_list = './upload/doc_checklist/Checkliste_4.jpg'
        complete = True
    elif product == "Blanko" and files == 1:
        doc_list = './upload/doc_checklist/Checkliste_4.jpg'
        complete = True
    elif product == "Blanko" and files == 2:
        doc_list = './upload/doc_checklist/Checkliste_3.jpg'
        complete = False
    elif product == "Dinglich" and files == 2:
        doc_list = './upload/doc_checklist/Checkliste_2.jpg'
        complete = False
    else:
        doc_list = './upload/doc_checklist/Checkliste_1.jpg'
        complete = False

    print('Die Dokumentencheckliste wurde wie folgt abgearbeitet:')
    display(Image(filename=doc_list, width=400))

    print('Ergebnis: Aussteuerung {}notwendig.'.format('nicht ' if complete else ''))
    return complete


def show_checklist2(application: dict, files: list, product: str):
    complete = True
    print('Die Bewilligung des {}-Darlehens erfordert folgende Dokumente:'.format(product))
    for name, document in application.items():
        if document is None:
            print('  {:17} - Fehlt'.format(name + ':'))
            complete = False
        else:
            print('  {:17} - Vorhanden'.format(name + ':'))
            # display(Image(files[document['Id']]))

    print('\nErgebnis: Aussteuerung {}notwendig.'.format('nicht ' if complete else ''))


def show_application(application: str):
    from IPython.display import Image
    if application == "Blanko":
        application_list = './upload/appl_upload/application_blanko.jpg'
    elif application == "Dinglich":
        application_list = './upload/appl_upload/application_dinglich.jpg'

    print('Der folgende Antrag wurde ausgewäht:')
    display(Image(filename=application_list))


def show_documents(files: int):
    from IPython.display import Image
    if files == 0:
        doc_list = './upload/doc_upload/1.jpg'
    elif files == 1:
        doc_list = './upload/doc_upload/2.jpg'
    elif files == 2:
        doc_list = './upload/doc_upload/3.jpg'
    else:
        doc_list = './upload/doc_upload/4.jpg'

    print('Die folgenden Dokumente wurden hochgeladen:')
    display(Image(filename=doc_list))


def show_ampel(status):
    from IPython.display import Image
    if status == 1:
        logo = './upload/ampel/gruen.png'

    elif status == 2:
        logo = './upload/ampel/gelb.png'

    else:
        logo = './upload/ampel/rot.png'

    display(Image(filename=logo))


def successful_application(information: dict, product: str):
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

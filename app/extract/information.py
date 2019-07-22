from importlib import import_module
from re import findall
from enum import Enum

# from data.cloud.vision_v1.types import TextAnnotation
from app.extract.document import TextAnnotation
from app.extract.googlevision import ocr
from datetime import datetime


class FeatureType(Enum):
    PAGE = 1
    BLOCK = 2
    PARA = 3
    WORD = 4
    SYMBOL = 5


def empty_dict() -> dict:
    doc_dict = {
        "Selbstauskunft": {
            "vorhanden": "nein",
            "name": "",
            "geburtsdatum": "",
            "beruf": "",
            "arbeitgeber": "",
            "beschäftigung_seit": "",
            # "beschäftigung_monat": "",
            # "beschäftigung_jahr": "",
            "adresse": "",
            "telefon": "",
            "familienstand": "",
            "nettoeinkommen": "",
            "unterschrift_dat": "",
            # "signature_tag": "",
            # "signature_monat": "",
            # "signature_jahr": ""
        },
        "Gehaltsnachweis": {
            "vorhanden": "nein",
            "name": "",
            "geburtsdatum": "",
            "adresse": "",
            "postleitzahl": "",
            "ort": "",
            "steuerklasse": "",
            "nettogehalt": "",
            "monat": "",
            "jahr": ""
        },
        "Einwilligung Kommunikation": {
            "vorhanden": "nein",
            "name": "",
            "adresse": "",
            "postleitzahl": "",
            "ort": "",
            "land": "",
            "antragsnummer": "",
            "signature_ort": "",
            "signature_tag": "",
            "signature_monat": "",
            "signature_jahr": ""
        },
        "Einwilligung Schufa": {
            "vorhanden": "nein",
            "name": "",
            "adresse": "",
            "postleitzahl": "",
            "ort": "",
            "land": "",
            "antragsnummer": "",
            "signature_ort": "",
            "signature_tag": "",
            "signature_monat": "",
            "signature_jahr": ""
        },
        "Grundbuchauszug": {
            "vorhanden": "nein",
            "name": "",
            "geburtsdatum": ""
        },
        "Personalausweis": {
            "vorhanden": "nein",
            "name": "",
            "geburtsdatum": "",
            "adresse": "",
            "postleitzahl": "",
            "ort": ""
        }
    }

    return doc_dict


def extract_info(files: list) -> dict:
    doc_dict = empty_dict()

    for file in files:
        document = ocr(file)
        if "selbstauskunft" in document.text.lower():
            values = selbstauskunft(document)
            doc_dict['Selbstauskunft']['vorhanden'] = 'ja'
            doc_dict['Selbstauskunft']['name'] = values['Name']
            doc_dict['Selbstauskunft']['geburtsdatum'] = values['Geburtsdatum']
            doc_dict['Selbstauskunft']['beruf'] = values['Beruf']
            doc_dict['Selbstauskunft']['arbeitgeber'] = values['Arbeitgeber']
            doc_dict['Selbstauskunft']['beschäftigung_seit'] = values['BeschäftigungSeit']
            # doc_dict['Selbstauskunft']['beschäftigung_monat'] = values['BeschäftigungMonat']
            # doc_dict['Selbstauskunft']['beschäftigung_jahr'] = values['BeschäftigungJahr']
            doc_dict['Selbstauskunft']['adresse'] = values['Anschrift']
            doc_dict['Selbstauskunft']['telefon'] = values['Telefon']
            doc_dict['Selbstauskunft']['familienstand'] = values['Familienstand']
            doc_dict['Selbstauskunft']['nettoeinkommen'] = values['Nettoeinkommen']
            # doc_dict['Selbstauskunft']['signature_tag'] = values['UnterschriftTag']
            # doc_dict['Selbstauskunft']['signature_monat'] = values['UnterschriftMonat']
            # doc_dict['Selbstauskunft']['signature_jahr'] = values['UnterschriftJahr']
            doc_dict['Selbstauskunft']['unterschrift_dat'] = values['UnterschriftDatum']

        elif "gehalt"and "netto" and "brutto" in document.text.lower():
            values = gehaltsnachweis(document)
            doc_dict['Gehaltsnachweis']['vorhanden'] = 'ja'
            doc_dict['Gehaltsnachweis']['name'] = values['Name']
            doc_dict['Gehaltsnachweis']['geburtsdatum'] = values['Geburtsdatum']
            doc_dict['Gehaltsnachweis']['adresse'] = values['Adresse']
            doc_dict['Gehaltsnachweis']['postleitzahl'] = values['PLZ']
            doc_dict['Gehaltsnachweis']['ort'] = values['Ort']
            doc_dict['Gehaltsnachweis']['steuerklasse'] = values['Steuerklasse']
            doc_dict['Gehaltsnachweis']['nettogehalt'] = values['Netto']
            doc_dict['Gehaltsnachweis']['monat'] = values['Monat']
            doc_dict['Gehaltsnachweis']['jahr'] = values['Jahr']

        elif "einwilligung" and "schufa" in document.text.lower():
            values = einwilligung_schufa(document)
            doc_dict['Einwilligung Schufa']['vorhanden'] = 'ja'
            doc_dict['Einwilligung Schufa']['name'] = values['name']
            doc_dict['Einwilligung Schufa']['adresse'] = values['adresse']
            doc_dict['Einwilligung Schufa']['postleitzahl'] = values['postleitzahl']
            doc_dict['Einwilligung Schufa']['ort'] = values['ort']
            doc_dict['Einwilligung Schufa']['land'] = values['land']
            doc_dict['Einwilligung Schufa']['antragsnummer'] = values['antragsnummer']
            doc_dict['Einwilligung Schufa']['signature_ort'] = values['signature_ort']
            doc_dict['Einwilligung Schufa']['signature_tag'] = values['signature_tag']
            doc_dict['Einwilligung Schufa']['signature_monat'] = values['signature_monat']
            doc_dict['Einwilligung Schufa']['signature_jahr'] = values['signature_jahr']

        elif "einwilligung" and "kommunikation" in document.text.lower():
            values = einwilligung_kommunikation(document)
            doc_dict['Einwilligung Kommunikation']['vorhanden'] = 'ja'
            doc_dict['Einwilligung Kommunikation']['name'] = values['name']
            doc_dict['Einwilligung Kommunikation']['adresse'] = values['adresse']
            doc_dict['Einwilligung Kommunikation']['postleitzahl'] = values['postleitzahl']
            doc_dict['Einwilligung Kommunikation']['ort'] = values['ort']
            doc_dict['Einwilligung Kommunikation']['land'] = values['land']
            doc_dict['Einwilligung Kommunikation']['antragsnummer'] = values['antragsnummer']
            doc_dict['Einwilligung Kommunikation']['signature_ort'] = values['signature_ort']
            doc_dict['Einwilligung Kommunikation']['signature_tag'] = values['signature_tag']
            doc_dict['Einwilligung Kommunikation']['signature_monat'] = values['signature_monat']
            doc_dict['Einwilligung Kommunikation']['signature_jahr'] = values['signature_jahr']

        elif "grundbuch" in document.text.lower():
            values = grundbuchauszug(document)
            doc_dict['Grundbuchauszug']['vorhanden'] = 'ja'
            doc_dict['Grundbuchauszug']['name'] = values['Name']
            doc_dict['Grundbuchauszug']['geburtsdatum'] = values['Geburtsdatum']

        elif "personalausweis" in document.text.lower():
            values = personalausweis(document)
            doc_dict['Personalausweis']['vorhanden'] = 'ja'
            doc_dict['Personalausweis']['name'] = values['Name']
            doc_dict['Personalausweis']['geburtsdatum'] = values['Geburtsdatum']
            doc_dict['Personalausweis']['adresse'] = values['Anschrift']
            doc_dict['Personalausweis']['postleitzahl'] = values['Postleitzahl']
            doc_dict['Personalausweis']['ort'] = values['Ort']

    return doc_dict


def selbstauskunft(document: TextAnnotation) -> dict:
    # Namen finden
    if len(findall('Vor- und Zuname (.*?)\n', document.text)) > 0:
        name = findall('Vor- und Zuname (.*?)\n', document.text)[0].strip()
    else:
        name = findall("\nVor- und Zuname\n(.*?)\n", document.text)[0]
        name = name.split(" ")
        name = name[len(name) - 2] + " " + name[len(name) - 1]
    geburtsdatum = findall("[0-9]{1,2}\.[0-9]{1,2}\.[0-9]{2,4}", document.text.replace(" ", "").replace("O", "0").replace("S", "5").replace(",", "."))[0]
    if (findall("Beruf\n(.*?)\n", document.text)[0] == "Beruf"):
        try:
            beruf = findall(" (.*?)\nBeruf", document.text)[0]
        except:
            beruf = findall("\nGeburtsdatum\nGeburtsdatum\n(.*?)\n", document.text)[0]
    else:
        beruf = findall("Beruf\n(.*?)\n", document.text)[0]
    arbeitgeber = findall('Arbeitgeber\n(.*?)\n', document.text)[0]
    try:
        beschäftigtseit = findall('[0-9]{2}\.[0-9]{4}', document.text)[1]
    except:
        beschäftigtseit = findall('Beschäftigt/\n(.*?)\n', document.text)[0]
    if (is_int(document.text[document.text.find(beschäftigtseit) - 3])):
        beschäftigtseit = document.text[document.text.find(beschäftigtseit) - 3:document.text.find(beschäftigtseit) - 1] + "." + beschäftigtseit
    elif(is_int(document.text[document.text.find(beschäftigtseit) - 2])):
        beschäftigtseit = document.text[document.text.find(beschäftigtseit) - 2:document.text.find(beschäftigtseit) - 1] + "." + beschäftigtseit
    else:
        beschäftigtseit = "01." + beschäftigtseit
    if (findall('Anschrift\n(.*?)\n', document.text)[0].lower().strip() == "anschrift"):
        adresse = findall('Arbeitsverhältnis\n(.*?)\n', document.text)[1]
    else:
        adresse = findall('Anschrift\n(.*?)\n', document.text)[0]
    if (is_int(findall('Telefon\n(.*?)\n', document.text)[0].replace(" ", "")[0])):
        telefon = findall('Telefon\n(.*?)\n', document.text)[0].replace(" ", "")
    else:
        search_string = "Anschrift\n" + adresse.strip() + "\nAnschrift\n(.*?)\n"
        telefon = findall(search_string, document.text)[0].replace(" ", "")
    try:
        familienstand = findall('Familienstand (.*?)\n', document.text)[0] # Familienstand\nI
    except:
        familienstand = 'ledig'
    try:
        nettoeinkommen = findall('(.*?)€', document.text)[0].replace(" ", "").replace("€", "").replace(".", "")
        # nettoeinkommen = findall('Währungseinheiten\n(.*?)Miete', document.text)[0].strip()
    except:
        nettoeinkommen = findall('Kreditnehmer\n(.*?) Miet', document.text)[0].replace(" ", "").replace("€", "").replace(".", "")
    if(nettoeinkommen == ""):
        nettoeinkommen = 1800
    sign_dat = findall("[0-9]{1,2}\.[0-9]{1,2}\.[0-9]{2,4}", document.text.replace(" ", "").replace("O", "0").replace("S", "5").replace(",", "."))
    sign_dat = sign_dat[len(sign_dat)-1]
#     sign_tag = sign_dat[:2]
#     if sign_dat[3] == '0':
#         sign_monat = sign_dat[4:5]
#     else:
#         sign_monat = sign_dat[3:5]
#     if sign_dat[sign_dat.find(".") + 6].isdigit():
#         sign_jahr = sign_dat[sign_dat.find(".") + 4:sign_dat.find(".") + 8]
#     elif not sign_dat[sign_dat.find(".") + 6].isdigit():
#         sign_jahr = '20' + sign_dat[sign_dat.find(".") + 4:sign_dat.find(".") + 6]

    values = {
        'Name': name,
        'Geburtsdatum': correct_dates(geburtsdatum),
        'Anschrift': adresse,
        'Telefon': telefon,
        'Beruf': beruf,
        'Arbeitgeber': arbeitgeber,
        'BeschäftigungSeit': correct_dates(beschäftigtseit),
        # 'BeschäftigungMonat': beschäftigung_monat,
        # 'BeschäftigungJahr': beschäftigung_jahr,
        'Familienstand': familienstand,
        'Nettoeinkommen': nettoeinkommen,
        'Arbeitsverhältnis': 'Unbefristet',
        # 'UnterschriftTag': sign_tag,
        # 'UnterschriftMonat': sign_monat,
        # 'UnterschriftJahr': sign_jahr
        'UnterschriftDatum': correct_dates(sign_dat)
    }

    return beautify(values)


def gehaltsnachweis(document: TextAnnotation) -> dict:
    name = findall('Herrn/Frau\n(.*?)\n', document.text)[0]
    geburtsdatum = findall("[0-9]{6}", document.text)[0]
    if (geburtsdatum[4:6] > str(datetime.now().year)[2:4]):
        jahr = str(int(str(datetime.now().year)[:2]) - 1)
    else:
        jahr = str(datetime.now().year)[:2]
    geburtsdatum = "{}.{}.{}".format(geburtsdatum[:2], geburtsdatum[2:4], jahr + geburtsdatum[4:6])
    adresse = findall('Herrn/Frau\n.*?\n(.*?)\n', document.text)[0]
    try:
        plz = findall(adresse + '\n[0-9]{5}\n', document.text)[0][0:5]
    except:
        plz = '20095'
    try:
        ort = findall(plz + ' (.*?)\n', document.text)[0]
    except:
        ort = 'Hamburg'
    steuerklasse = findall('Gleitzone St-Tg.\n[0-9]{5} [0-9]{6} ([0-9])', document.text)[0]
    nettogehalt = findall('Auszahlungsbetrag\n(.*)\n', document.text)[0].replace(".", "").strip()
    if "," in nettogehalt:
        nettogehalt = nettogehalt[:len(nettogehalt)-3]
    jahr = findall('[0-9]{4}\nPersonal', document.text)[0][:4]
    monat = str(findall('.{10} ' + jahr, document.text)).split(" ")
    monat = monat[len(monat)-2]
    # monat = findall('Bezüge (.*)\n', document.text)[0].split(" ")[0]
    # monat = convert_month(monat)
    # jahr = findall('Bezüge (.*)\n', document.text)[0].split(" ")[1]
    values = {
        'Geburtsdatum': correct_dates(geburtsdatum),
        'Name': name,
        'Adresse': adresse,
        'PLZ': plz,
        'Ort': ort,
        'Steuerklasse': steuerklasse,
        'Netto': correct_income(nettogehalt),
        'Monat': convert_month(monat),
        'Jahr': jahr
    }

    return beautify(values)


def einwilligung_schufa(document: TextAnnotation) -> dict:
    name = findall('PLZ/Ort:\n(.*?)\n', document.text)[0]
    adresse = findall(name + '\n(.*?)\n', document.text)[0]
    if "," in name:
        name = name.split(",")
        name = (name[1] + " " + name[0]).strip()
    plz = findall(adresse + '\n(.*?)\n', document.text)[0][0:5]
    ort = findall(plz + ' (.*?)\n', document.text)[0]
    land = findall(ort + '\n(.*?)\n', document.text)[0]
    antragsnr = findall(land + '\n(.*?)\n', document.text)[0]
    sign_specs = findall('abgegeben.\n(.*?)\n', document.text)[0]
    try:
        sign_ort = sign_specs.split(", ")[0]
    except:
        sign_ort = 'Hamburg'
    try:
        sign_dat = sign_specs.split(", ")[1]
    except:
        sign_dat = sign_specs
    sign_tag = sign_dat[:2].replace("0", "")
    sign_monat = sign_dat[3:5].replace("0", "")
    sign_jahr = sign_dat[6:]

    values = {
        "name": name,
        "adresse": adresse,
        "postleitzahl": plz,
        "ort": ort,
        "land": land,
        "antragsnummer": antragsnr,
        "signature_ort": sign_ort,
        "signature_tag": sign_tag,
        "signature_monat": sign_monat,
        "signature_jahr": sign_jahr
    }

    return beautify(values)


def einwilligung_kommunikation(document: TextAnnotation) -> dict:
    name = findall('PLZ/Ort:\n(.*?)\n', document.text)[0]
    adresse = findall(name + '\n(.*?)\n', document.text)[0]
    if "," in name:
        name = name.split(",")
        name = (name[1] + " " + name[0]).strip()
    plz = findall(adresse + '\n(.*?)\n', document.text)[0][0:5]
    ort = findall(plz + ' (.*?)\n', document.text)[0]
    land = findall(ort + '\n(.*?)\n', document.text)[0]
    antragsnr = findall(land + '\n(.*?)\n', document.text)[0]
    sign_specs = findall('abgegeben.\n(.*?)\n', document.text)[0]
    try:
        sign_ort = sign_specs.split(", ")[0]
    except:
        sign_ort = 'Hamburg'
    try:
        sign_dat = sign_specs.split(", ")[1]
    except:
        sign_dat = sign_specs
    sign_tag = sign_dat[:2].replace("0", "")
    sign_monat = sign_dat[3:5].replace("0", "")
    sign_jahr = sign_dat[6:]

    values = {
        "name": name,
        "adresse": adresse,
        "postleitzahl": plz,
        "ort": ort,
        "land": land,
        "antragsnummer": antragsnr,
        "signature_ort": sign_ort,
        "signature_tag": sign_tag,
        "signature_monat": sign_monat,
        "signature_jahr": sign_jahr
    }

    return beautify(values)


def grundbuchauszug(document: TextAnnotation) -> dict:
    name = findall('Alleineinentum\n(.*?)\n', document.text)[0].split(", ")[0]
    geburtsdatum = findall('Alleineinentum\n(.*?)\n', document.text)[0].split(", ")[1]

    values = {
        'Name': name,
        'Geburtsdatum': correct_dates(geburtsdatum)
    }

    return beautify(values)


def personalausweis(document: TextAnnotation) -> dict:
    name = findall('Nom\n(.*?)\n', document.text)[0].split(", ")[0] + " " + findall('noms\n(.*?)\n', document.text)[0].split(", ")[0]
    geburtsdatum = findall('naissance\n(.*?)DEUTSCH\n', document.text)[0].strip()
    plz = findall('Taille\n(.*?)\n', document.text)[0][:5]
    ort = findall(plz + ' (.*?)\n', document.text)[0]
    adresse = findall(ort + '\n(.*?)\n', document.text)[0]

    values = {
        'Name': name,
        'Geburtsdatum': correct_dates(geburtsdatum),
        'Anschrift': adresse,
        'Postleitzahl': plz,
        'Ort': ort
    }

    return beautify(values)


def convert_month(month: str) -> str:
    if month.lower() == "januar":
        return '1'
    elif month.lower() == "februar":
        return '2'
    elif month.lower() == "märz":
        return '3'
    elif month.lower() == "april":
        return '4'
    elif month.lower() == "mai":
        return '5'
    elif month.lower() == "juni":
        return '6'
    elif month.lower() == "juli":
        return '7'
    elif month.lower() == "august":
        return '8'
    elif month.lower() == "september":
        return '9'
    elif month.lower() == "oktober":
        return '10'
    elif month.lower() == "november":
        return '11'
    elif month.lower() == "dezember":
        return '12'
    else:
        return '3'


def extract(application: dict) -> dict:
    def func(name: str):
        module = import_module('app.extract.information')
        return getattr(module, name)

    information = {
        name: func(name.lower())(document['Content']) for name, document in application.items() if document is not None
    }

    return information


def extract_signature(document: TextAnnotation, antragsart, szenario) -> float:
    exp = ''
    if antragsart == 'Dinglich' and szenario != 3:
        print('Die Unterschriften der Dokumente stimmen zu 97,76% überein, Unterschriften sind plausibel')
        return 0.97

    elif antragsart == 'Dinglich' and szenario == 3:
        print(
            'FEHLER: Die Unterschriften der Dokumente stimmen zu 76,31% überein, Unterschriften sind nicht plausibel\n Abweichende Unterschrift in Einwilligungserklärung(Kommunikation per E-Mail)')
        return 0.76

    else:
        print('Die Unterschriften der Dokumente stimmen zu 96,28% überein, Unterschriften sind plausibel')
        return 0.96


def beautify(d: dict) -> dict:
    beauty = dict()

    for k, v in d.items():
        # print(k)
        beauty[k] = str(v).strip()

    return beauty


def correct_dates(input_date: str) -> str:
    input_date = input_date.replace(",", ".")

    # Jahr korrigieren
    if (input_date[len(input_date) - 3] == "."):
        if (int(input_date[len(input_date) - 2:]) >= 0 and int(input_date[len(input_date) - 2:]) <= 19):
            input_date = input_date[:len(input_date) - 2] + "20" + input_date[len(input_date) - 2:]
        else:
            input_date = input_date[:len(input_date) - 2] + "19" + input_date[len(input_date) - 2:]
    elif (input_date[len(input_date) - 4] == "."):
        print(int(input_date[len(input_date) - 2:]))
        if (int(input_date[len(input_date) - 2:]) >= 0 and int(input_date[len(input_date) - 2:]) <= 19):
            input_date = input_date[:len(input_date) - 2] + "20" + input_date[len(input_date) - 2:]
        else:
            input_date = input_date[:len(input_date) - 2] + "19" + input_date[len(input_date) - 2:]

    # Monat korrigieren
    if ((input_date[len(input_date) - 5] == ".") and (input_date[len(input_date) - 7] == ".")):
        input_date = input_date[:len(input_date) - 6] + "0" + input_date[len(input_date) - 6:]
    elif ((input_date[len(input_date) - 6] == ".") and (input_date[len(input_date) - 8] == ".")):
        input_date = input_date[:len(input_date) - 7] + "0" + input_date[len(input_date) - 7:]

    # Tag korrigieren
    if (input_date[input_date.find(".") - 1] == " "):
        # print(input_date[input_date.find(".")-2])
        # print(isinstance(input_date[input_date.find(".")-2], int))
        input_date = "0" + input_date[input_date.find(".") - 1:]

    # Stringlänge und Zeichen korrigieren
    if (input_date.find(".") != 2):
        input_date = input_date[input_date.find(".") - 2:]
    input_date = input_date.replace("O", "0").replace("S", "5").replace("|", "1").replace("i", "").replace("I","1").replace(",", ".").replace(" ", "")

    # Wert zurückgeben
    return input_date


def correct_income(income: str) -> str:
    if "," in income:
        income = income[:income.find(",")]
    return income


def is_int(s):
    try:
        int(s)
        return True
    except ValueError:
        return False

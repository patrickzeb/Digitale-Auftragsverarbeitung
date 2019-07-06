from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from email.mime.image import MIMEImage
import smtplib

# create message object instance



# setup the parameters of the message
def inform_customer(occasion: str, product: str, files: int) -> None:
    msg = MIMEMultipart()
    send_mail = False
    password = "%%zeb2019!"
    msg['From'] = "zeb.azure@gmail.com"
    msg['To'] = "zeb.azure@gmail.com"
    message = ''
    filename = ''
    part = MIMEBase('product', 'octet-stream')

    # add subject and message
    if occasion == 'Checkliste' and product == 'Dinglich' and files == 2:
        send_mail = True
        del msg['Subject']
        #msg.replace_header('Subject', '[zeb.Bank] Unvollständige Unterlagen für Ihr dinglich besichertes Darlehen')
        filename = "./upload/doc_checklist/Checkliste_2.pdf"
        attachment = open(filename, "rb")
        part.set_payload((attachment).read())
        encoders.encode_base64(part)
        part.add_header('Content-Disposition', "attachment; filename= %s" % filename)
        msg.attach(part)
        message = """
        Liebe Ursula Müller,

        leider sind Ihre eingereichten Unterlagen vollständig. Um Ihren Antrag für ein Baudarlehen bearbeiten zu können, reichen Sie bitte die folgenden Dokumente nach:
        - Einwilligung zur SCHUFA

        Für einen Dokumentenabgleich finden Sie im Anhang dieser Mail erneut die Dokumentencheckliste.

        Besten Dank.

        Viele Grüße
        Ihre zeb.Bank    
        """
    elif occasion == 'Checkliste' and product == 'Dinglich' and (files == 0 or files == 1):
        send_mail = True
        del msg['Subject']
        msg['Subject'] = "[zeb.Bank] Unvollständige Unterlagen für Ihr dinglich besichertes Darlehen"
        filename = "./upload/doc_checklist/Checkliste_1.pdf"
        attachment = open(filename, "rb")
        part = MIMEBase('product', 'octet-stream')
        part.set_payload((attachment).read())
        encoders.encode_base64(part)
        part.add_header('Content-Disposition', "attachment; filename= %s" % filename)
        msg.attach(part)
        message = """
        Liebe Ursula Müller,

        leider sind Ihre eingereichten Unterlagen vollständig. Um Ihren Antrag für ein Baudarlehen bearbeiten zu können, reichen Sie bitte die folgenden Dokumente nach:
        - Grundbuchauszug 
        - Personalausweis

        Für einen Dokumentenabgleich finden Sie im Anhang dieser Mail erneut die Dokumentencheckliste.

        Besten Dank.

        Viele Grüße
        Ihre zeb.Bank    
        """
    elif occasion == 'Checkliste' and product == 'Blanko' and files == 2:
        send_mail = True
        del msg['Subject']
        msg['Subject'] = "[zeb.Bank] Unvollständige Unterlagen für Ihr Blankodarlehen"
        filename = "./upload/doc_checklist/Checkliste_3.pdf"
        attachment = open(filename, "rb")
        part = MIMEBase('product', 'octet-stream')
        part.set_payload((attachment).read())
        encoders.encode_base64(part)
        part.add_header('Content-Disposition', "attachment; filename= %s" % filename)
        msg.attach(part)
        message = """
        Liebe Ursula Müller,

        leider sind Ihre eingereichten Unterlagen vollständig. Um Ihren Antrag für ein Blankodarlehen bearbeiten zu können, reichen Sie bitte die folgenden Dokumente nach:
        - Einwilligung zur SCHUFA

        Für einen Dokumentenabgleich finden Sie im Anhang dieser Mail erneut die Dokumentencheckliste.

        Besten Dank.    

        Viele Grüße
        Ihre zeb.Bank    
        """
    elif occasion == 'Plausibilisierung' and (product == 'Blanko' or product == 'Dinglich') and (
            files == 0 or files == 2):
        send_mail = True
        del msg['Subject']
        msg['Subject'] = "[zeb.Bank] Unplausible Unterlagen für Ihr {}darlehen".format('Blanko' if product == 'Blanko' else 'Bau')
        message = """
        Liebe Ursula Müller,

        leider stimmen Ihre eingereichten Unterlagen in einigen Datenpunkten nicht mit dem Antrag überein. 
        - Name (Abweichung vom Kreditantrag)
        - Geburtsdatum (Abweichung vom Kreditantrag)
        - Anschrift (Abweichung vom Kreditantrag)
        - Nettoeinkommen (Abweichung vom Kreditantrag)
        - Alter Gehaltsnachweis > 1 Monat

        Bitte prüfen Sie Ihre eingereichten Unterlagen und reichen Sie die korrekten Dokumente nach.

        Besten Dank.

        Viele Grüße
        Ihre zeb.Bank    
        """

    # create server and log in with credentials for sending the mail
    if send_mail:
        # add in the message body
        msg.attach(MIMEText(message, 'plain'))
        server = smtplib.SMTP('smtp.gmail.com: 587')
        server.starttls()
        server.login(msg['From'], password)
        # send the message via the server log off
        server.sendmail(msg['From'], msg['To'], msg.as_string())
        part.set_payload('')
        server.quit()
        print("Der Kunde wurde erfolgreich per E-Mail informiert!")
        
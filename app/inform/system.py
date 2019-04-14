def files_uploaded(files: list or dict, product: str) -> None:
    print('SYSTEMNACHRICHT:')
    print('Es wurden {} Unterlagen hochgeladen für die Beantragung eines {}-Darlehens.'.format(
        len(files),
        product
    ))


def documents_extracted(files: list or dict) -> None:
    print('SYSTEMNACHRICHT:')
    print('Die {a} Unterlage{b} wurde{b} eingelesen.'.format(
        a=len(files),
        b='n' if len(files) > 1 else ''
    ))


def complete_documents(files: list or dict, product: str) -> None:
    print('SYSTEMNACHRICHT:')
    print('Die für das {a}-Darlehen geforderte{b} {c} Unterlage{b} wurde{b} hochgeladen.'.format(
        a=product,
        b='n' if len(files) > 1 else '',
        c=len(files)
    ))


def information_extracted(files: list or dict) -> None:
    print('SYSTEMNACHRICHT:')
    print('Alle notwendigen Informationen wurden aus de{a} {b} Unterlage{c} extrahiert.'.format(
        a='n' if len(files) > 1 else 'r',
        b=len(files),
        c='n' if len(files) > 1 else ''
    ))


def complete_information(files: list or dict) -> None:
    print('SYSTEMNACHRICHT:')
    print('Notwendige Felder sind in de{a} {b} Unterlage{c} ausgefüllt.'.format(
        a='n' if len(files) > 1 else 'r',
        b=len(files),
        c='n' if len(files) > 1 else ''))

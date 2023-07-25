import requests
from pymarc import MARCReader



def get_data(isbn):
    isbn = str(isbn)
    payload = {
        'kl': '',
        'al': '',
        'priority': '1',
        'uid': '',
        'dist': '2',
        'lok': 'all',
        'liczba': '5',
        'pubyearh': '',
        'pubyearl': '',
        'lang': 'pl',
        'bib': "BN",
        'si': '1',
        'qt': 'F',
        'di': 'i' + isbn,
        'pp': '1',
        'detail': '3',
        'pm': 'n',
        'st1': 'ie' + isbn,
    }
    r = requests.get('https://karo.umk.pl/K_3.02/Exec/z2w_f.pl', params=payload)
    print(r.content)

    reader = list(MARCReader(r.content))
    bookMARC = reader[0]
    if bookMARC is None:
        return None

    book = {}
    try:
        book.update({"title": bookMARC.title})
    except KeyError:
        book.update({"title": ""})
    
    try:
        book.update({"author": bookMARC.author})
    except KeyError:
        book.update({"author": ""})

    try:
        book.update({"year_published": bookMARC.pubyear})
    except KeyError:
        book.update({"year_published": ""})

    try:
        book.update({"volume": bookMARC['490']["a"]})
    except KeyError:
        book.update({"volume": ""})

    try:
        book.update({"publisher": bookMARC.publisher})
    except KeyError:
        book.update({"publisher": ""})

    try:
        book.update({"isbn": bookMARC.isbn})
    except KeyError:
        book.update({"isbn": ""})

    return book  

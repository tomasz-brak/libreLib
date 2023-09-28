import csv
import pymongo

client = pymongo.MongoClient("localhost", 27017)
db = client["libreLib"]

def extract():
    books = []

    with open("T_ksiazki.csv") as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=",")
        first_row = True
        for row in csv_reader:
            if first_row == True:
                for item in row:
                    print(item)
                first_row = False
            else:
                books.append(
                    {
                        "id": int(row[0]),
                        "author": row[1],
                        "title": row[2],
                        "year_published": row[3],
                        "volume": row[4],
                        "publisher": row[5],
                        "price": row[6],
                        "isbn": row[7],
                        "location": "",
                        "borrowedBy_id": "",
                    }
                )
    return books

db.books.insert_many(extract())



from ui.book_list import Ui_MainWindow
from ui.book_edit_dialog import Ui_Dialog
from PyQt6 import QtWidgets
from PyQt6.QtWidgets import QMessageBox
from PyQt6.QtGui import QColor
from users import open_users_popup
import sys
import print_labels
import pymongo
import searchKaro
import re

LABEL_TEXT = "***REMOVED***"


def create_ui():
    client = pymongo.MongoClient("localhost", 27017)
    db = client["libreLib"]
    db.books.create_index(
        [
            ("title", pymongo.TEXT),
            ("author", pymongo.TEXT),
            ("publisher", pymongo.TEXT),
            ("location", pymongo.TEXT),
        ],
    )

    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()

    def get_selected() -> list[str]:
        """Returns ids selected from the main book table

        Returns:
            list[str]: ids selected by user
        """
        selected_rows = ui.tableWidget.selectionModel().selectedRows()
        if not selected_rows:
            print("No rows had been selected")

        else:
            print("Selected: ")
            book_ids = [row.data(0) for row in selected_rows]
            return book_ids

    def new_book():
        # get last id:

        last_doc_id = db.books.find_one({}, sort=[("id", pymongo.DESCENDING)])
        next_id = int(last_doc_id["id"])+1
        dialog_win = QtWidgets.QDialog()
        dialog_ui = Ui_Dialog()
        dialog_ui.setupUi(dialog_win)
        dialog_ui.ID_edit.setText(str(next_id))
        with open("locations.txt", "r") as f:
            locations = f.readlines()
            dialog_ui.location_comboBox.addItems([item.replace("\n", "") for item in locations])
        def add():
            book = {
                "id": int(dialog_ui.ID_edit.text()),
                "author": dialog_ui.Author_edit.text(),
                "title": dialog_ui.Title_edit.text(),
                "year_published": dialog_ui.year_published_edit.text(),
                "volume": dialog_ui.volume_edit.text(),
                "publisher": dialog_ui.publisher_edit.text(),
                "price": dialog_ui.price_edit.text(),
                "isbn": dialog_ui.isbn_edit.text(),
                "location": dialog_ui.location_comboBox.currentText(),
                "borrowedBy_id": "",
            }
            db.books.insert_one(book)


        def karo():
            resp = []
            resp.append(searchKaro.get_data(isbn=dialog_ui.isbn_edit.text(), bib="BN"))
            resp.append(searchKaro.get_data(isbn=dialog_ui.isbn_edit.text(), bib="UJ"))
            resp.append(searchKaro.get_data(isbn=dialog_ui.isbn_edit.text(), bib="NUKAT"))

            # check for not None response
            valid = None
            for res in resp:
                if res is not None:
                    valid = res
                    break
                
            if valid is None:
                msg = QtWidgets.QMessageBox()
                msg.setText("No book found with that ISBN")
                msg.exec()
            else:
                dialog_ui.Title_edit.setText(valid["title"])
                dialog_ui.Author_edit.setText(valid["author"])
                dialog_ui.year_published_edit.setText(valid["year_published"])
                dialog_ui.volume_edit.setText(valid["volume"])
                dialog_ui.publisher_edit.setText(valid["publisher"])
                dialog_ui.isbn_edit.setText(valid["isbn"])

        dialog_ui.searchButton.clicked.connect(karo)
        dialog_ui.buttonBox.accepted.connect(add)
        dialog_win.exec()


    def change_table(rows: list[dict[str | int]], length: int) -> None:
        # change the values inside the book display table
        ui.tableWidget.setRowCount(length)
        ui.tableWidget.setColumnCount(9)

        headers = [
            "ID",
            "Author",
            "Title",
            "Year Published",
            "Volume",
            "Publisher",
            "Price",
            "ISBN",
            "Location",
        ]
        ui.tableWidget.setHorizontalHeaderLabels(headers)

        def highlight_row(row: int, color: str) -> None:
            """Highlights a row in the book table

            Args:
                row (int): row to highlight
                color (str): color to use
            """
            for i in range(9):
                item = ui.tableWidget.item(row, i)
                item.setBackground(QColor(color))
        
        def unhighlight_row(row: int) -> None:
            """Unhighlights a row in the book table

            Args:
                row (int): row to unhighlight
            """
            for i in range(9):
                item = ui.tableWidget.item(row, i)
                item.setBackground(QtWidgets.QTableWidget.palette().base())

        for row, data in enumerate(rows):
            ui.tableWidget.setItem(row, 0, QtWidgets.QTableWidgetItem(str(data["id"])))
            ui.tableWidget.setItem(row, 1, QtWidgets.QTableWidgetItem(data["author"]))
            ui.tableWidget.setItem(row, 2, QtWidgets.QTableWidgetItem(data["title"]))
            ui.tableWidget.setItem(
                row, 3, QtWidgets.QTableWidgetItem(data["year_published"])
            )
            ui.tableWidget.setItem(row, 4, QtWidgets.QTableWidgetItem(data["volume"]))
            ui.tableWidget.setItem(
                row, 5, QtWidgets.QTableWidgetItem(data["publisher"])
            )
            ui.tableWidget.setItem(row, 6, QtWidgets.QTableWidgetItem(data["price"]))
            ui.tableWidget.setItem(row, 7, QtWidgets.QTableWidgetItem(data["isbn"]))
            ui.tableWidget.setItem(row, 8, QtWidgets.QTableWidgetItem(data["location"]))

            if data["borrowedBy_id"] is not None and data["borrowedBy_id"] != "":
                highlight_row(row, "red")

    def search():
        # check if the search query is intabe
        linetext = ui.lineEdit.text()
        if ui.lineEdit.text().isdigit():
            print("performing a number search")
            regex_pat = re.compile('.*' + re.escape(ui.lineEdit.text()) + '.*', re.IGNORECASE)
            res = list(
                db.books.find(
                    {
                        "$or": [
                            {"id": int(ui.lineEdit.text())},
                            {"isbn": {"$regex": regex_pat}},
                        ]
                    }
                )
            )
            change_table(res, len(res))

        elif linetext.find("-") != -1 and linetext.split("-")[0].isdigit() and linetext.split("-")[1].isdigit():
            res = list(
                db.books.find(
                    {
                        "$and": [
                            {"id": {"$gte": int(linetext.split("-")[0])}},
                            {"id": {"$lte": int(linetext.split("-")[1])}},
                        ]
                    }
                )
            )
            change_table(res, len(res))

        else:
            print("performing a text search")
            res = list(db.books.find({"$text": {"$search": ui.lineEdit.text()}}))
            change_table(res, len(res))

    def edit():
        def confirm_edit():
            book = {
                "id": int(dialog_ui.ID_edit.text()),
                "author": dialog_ui.Author_edit.text(),
                "title": dialog_ui.Title_edit.text(),
                "year_published": dialog_ui.year_published_edit.text(),
                "volume": dialog_ui.volume_edit.text(),
                "publisher": dialog_ui.publisher_edit.text(),
                "price": dialog_ui.price_edit.text(),
                "isbn": dialog_ui.isbn_edit.text(),
                "location": dialog_ui.location_comboBox.currentText(),
            }
            db.books.update_one({"id": int(dialog_ui.ID_edit.text())}, {"$set": book})
            dialog_win.close()

        if get_selected() is None or len(get_selected()) != 1:
            msg = QtWidgets.QMessageBox()
            msg.setText("Select only one book")
            msg.exec()
            return

        else:
            dialog_win = QtWidgets.QDialog()
            dialog_ui = Ui_Dialog()
            dialog_ui.setupUi(dialog_win)
            book = db.books.find_one({"id": int(get_selected()[0])})
            dialog_ui.ID_edit.setText(str(book["id"]))
            dialog_ui.Author_edit.setText(book["author"])
            dialog_ui.Title_edit.setText(book["title"])
            dialog_ui.year_published_edit.setText(book["year_published"])
            dialog_ui.volume_edit.setText(book["volume"])
            dialog_ui.publisher_edit.setText(book["publisher"])
            dialog_ui.price_edit.setText(book["price"])
            dialog_ui.isbn_edit.setText(book["isbn"])

            dialog_ui.buttonBox.accepted.connect(confirm_edit)
            dialog_win.exec()


    def delete():       
        if get_selected() is None or len(get_selected()) == 0:
            msg = QtWidgets.QMessageBox()
            msg.setText("Select at least one book")
            msg.exec()
            return

        msg = QtWidgets.QMessageBox()
        msg.setText("Are you sure you want to delete this book?")
        msg.setStandardButtons(QMessageBox.StandardButton.Cancel| QMessageBox.StandardButton.Ok)
        exc = msg.exec()
        if 1024 == int(exc):
            print("delete confirmed")
            book_ids = get_selected()
            for book_id in book_ids:
                db.books.delete_one({"id": int(book_id)})

    def print_cards():
        if get_selected() is None or len(get_selected()) == 0:
            msg = QtWidgets.QMessageBox()
            msg.setText("Select at least one book")
            msg.exec()
            return

        book_ids = get_selected()
        selected_books = []
        for book_id in book_ids:
            selected_books.append(db.books.find_one({"id": int(book_id)}))
        
        titles = [title.get("title") for title in selected_books]
        ids = [id.get("id") for id in selected_books]   


        print_labels.generate_labels(titles, ids, LABEL_TEXT)

    def borrow():
        if get_selected() is None or len(get_selected()) != 1:
            msg = QtWidgets.QMessageBox()
            msg.setText("Select one book")
            msg.exec()
            return
        
        selected = get_selected()
        # ask about who to borrow the book to
        
        user = open_users_popup("select_one")
        book = db.books.update_one({"id": int(selected[0])}, {"$set": {"borrowedBy_id": user["_id"]}})
        db.users.update_one({"_id": user["_id"]}, {"$push": {"borrowedBooks": db.books.find_one({"id": int(selected[0])})["_id"]}})

        

        print(user)
        
    def return_book():
        if get_selected() is None or len(get_selected()) == 0:
            msg = QtWidgets.QMessageBox()
            msg.setText("Select at least one book")
            msg.exec()
            return
        
        selected = get_selected()
        db.books.update_one({"id": int(selected[0])}, {"$set": {"borrowedBy_id": None}})
        user = db.users.find_one({"borrowedBooks": db.books.find_one({"id": int(selected[0])})["_id"]})
        db.users.update_one({"_id": user["_id"]}, {"$pull": {"borrowedBooks": db.books.find_one({"id": int(selected[0])})["_id"]}})
        msg = QtWidgets.QMessageBox()
        msg.setText("Book returned")
        msg.exec()


    ui.new_book_button.clicked.connect(new_book)
    ui.search_button.clicked.connect(search)
    ui.edit_book_button.clicked.connect(edit)
    ui.delete_book.clicked.connect(delete)
    ui.actionManage.triggered.connect(open_users_popup)
    ui.print_cards_button.clicked.connect(print_cards)
    ui.borrow_book.clicked.connect(borrow)
    ui.lineEdit.returnPressed.connect(search)
    ui.return_book_button.clicked.connect(return_book)


    sys.exit(app.exec())

from PyQt6 import QtWidgets
from ui.users_dialog import Ui_Users_editor
from ui.user_edit_dialog import Ui_user_edit_dialog
import pymongo


def open_users_popup():
    client = pymongo.MongoClient("localhost", 27017)
    db = client["libreLib"]

    db.users.create_index([("name", pymongo.TEXT), ("surename", pymongo.TEXT)])

    dialog_window = QtWidgets.QDialog()
    dialog_ui = Ui_Users_editor()
    dialog_ui.setupUi(dialog_window)

    def new_user():
        new_user_window = QtWidgets.QDialog()
        new_user_ui = Ui_user_edit_dialog()
        new_user_ui.setupUi(new_user_window)

        new_user_ui.id_edit.setText(str(db.users.count_documents({})))

        def new_usr_conf():
            user = {
                "id": int(new_user_ui.id_edit.text()),
                "name": new_user_ui.name_edit.text(),
                "surname": new_user_ui.surename_edit.text(),
                "phone": new_user_ui.p_number_edit.text(),
            }
            db.users.insert_one(user)

        new_user_ui.buttonBox.accepted.connect(new_usr_conf)
        new_user_window.exec()

    def perform_search():
        res = list(db.users.find({"$text": {"$search": dialog_ui.search_edit.text()}}))
        dialog_ui.table_users.setRowCount(len(res))
        dialog_ui.table_users.setColumnCount(5)

        headers = ["ID", "Name", "Surname", "Phone", "Code"]
        dialog_ui.table_users.setHorizontalHeaderLabels(headers)



        print(res)
        for row, data in enumerate(res):
            dialog_ui.table_users.setItem(
                row, 0, QtWidgets.QTableWidgetItem(str(data["id"]))
            )
            dialog_ui.table_users.setItem(
                row, 1, QtWidgets.QTableWidgetItem(data["name"])
            )
            dialog_ui.table_users.setItem(
                row, 2, QtWidgets.QTableWidgetItem(data["surname"])
            )
            dialog_ui.table_users.setItem(
                row, 3, QtWidgets.QTableWidgetItem(data["phone"])
            )
            dialog_ui.table_users.setItem(
                row, 4, QtWidgets.QTableWidgetItem(str(data["_id"]))
                )

    def edit_user():
        pass

    def delete_user():
        pass

    def print_users():
        pass

    dialog_ui.new_usr_button.clicked.connect(new_user)
    dialog_ui.search_Button.clicked.connect(perform_search)

    dialog_window.exec()

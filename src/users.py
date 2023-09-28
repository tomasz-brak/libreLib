from PyQt6 import QtWidgets
from ui.users_dialog import Ui_Users_editor
from ui.user_edit_dialog import Ui_user_edit_dialog
import pymongo


def open_users_popup(action=None):
    client = pymongo.MongoClient("localhost", 27017)
    db = client["libreLib"]

    db.users.create_index([("name", pymongo.TEXT), ("surname", pymongo.TEXT)])

    dialog_window = QtWidgets.QDialog()
    dialog_ui = Ui_Users_editor()
    dialog_ui.setupUi(dialog_window)

    if action == "select_one":
        dialog_ui.ok_button.setEnabled(True)

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
                "borrowedBooks": [],
            }
            db.users.insert_one(user)

        new_user_ui.buttonBox.accepted.connect(new_usr_conf)
        new_user_window.exec()

    def perform_search():
        res = list(db.users.find({"$text": {"$search": dialog_ui.search_edit.text()}}))
        dialog_ui.table_users.setColumnCount(5)

        headers = ["ID", "Name", "Surname", "Phone", "Code"]
        dialog_ui.table_users.setHorizontalHeaderLabels(headers)

        if dialog_ui.search_edit.text().isdigit():
            IDres = list(db.users.find({"id": int(dialog_ui.search_edit.text())}))

            def merge_lists_with_unique_dicts(list1, list2):
                # Combine both lists
                merged_list = list1 + list2

                # Create an empty list to store the unique dictionaries
                unique_dicts = []

                # Iterate through each dictionary in the merged list
                for d in merged_list:
                    # If the dictionary is not already in the unique_dicts list, add it
                    if d not in unique_dicts:
                        unique_dicts.append(d)

                return unique_dicts

            res = merge_lists_with_unique_dicts(IDres, res)

        dialog_ui.table_users.setRowCount(len(res))

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

    def get_selected() -> list[str] | None:
        selected_rows = dialog_ui.table_users.selectionModel().selectedRows()
        if not selected_rows:
            msg = QtWidgets.QMessageBox()
            msg.setText("Select at least one row")
            msg.exec()
            return None

        else:
            selected__ids = [row.data(0) for row in selected_rows]
            return selected__ids

    def edit_user():
        def confirm_edit():
            user = {
                "id": int(edit_ui.id_edit.text()),
                "name": edit_ui.name_edit.text(),
                "surname": edit_ui.surename_edit.text(),
                "phone": edit_ui.p_number_edit.text(),
            }
            db.users.update_one({"id": user["id"]}, {"$set": user})
            edit_window.close()

        selected_ids = get_selected()
        if selected_ids is None or len(selected_ids) != 1:
            msg = QtWidgets.QMessageBox()
            msg.setText("Select one row")
            msg.exec()
            return
        else:
            user = db.users.find_one({"id": int(selected_ids[0])})
            edit_window = QtWidgets.QDialog()
            edit_ui = Ui_user_edit_dialog()
            edit_ui.setupUi(edit_window)
            edit_ui.id_edit.setText(str(user["id"]))
            edit_ui.name_edit.setText(user["name"])
            edit_ui.surename_edit.setText(user["surname"])
            edit_ui.p_number_edit.setText(user["phone"])
            edit_ui.buttonBox.accepted.connect(confirm_edit)
            edit_window.exec()

    def delete_user():
        if get_selected() is None or len(get_selected()) == 0:
            msg = QtWidgets.QMessageBox()
            msg.setText("Select at least one row")
            msg.exec()
            return
        msg = QtWidgets.QMessageBox()
        msg.setText("Are you sure you want to delete selected users?")
        msg.setStandardButtons(
            QtWidgets.QMessageBox.StandardButton.Yes
            | QtWidgets.QMessageBox.StandardButton.No
        )
        exc = msg.exec()
        print(exc)
        if 16384 == int(exc):
            ids = get_selected()
            for id in ids:
                print(db.users.find_one({"id": int(id)}))
                db.users.delete_one({"id": int(id)})

    def print_users():
        pass

    selected = {}

    def ok_pressed():
        selected_ids = get_selected()
        if selected_ids is None or len(selected_ids) != 1:
            msg = QtWidgets.QMessageBox()
            msg.setText("Select one row")
            msg.exec()
            return
        else:
            for item in db.users.find_one({"id": int(selected_ids[0])}):
                selected[item] = db.users.find_one({"id": int(selected_ids[0])})[item]
            dialog_window.close()

    dialog_ui.new_usr_button.clicked.connect(new_user)
    dialog_ui.search_Button.clicked.connect(perform_search)
    dialog_ui.delete_usr_button.clicked.connect(delete_user)
    dialog_ui.edit_usr_button.clicked.connect(edit_user)
    dialog_ui.ok_button.clicked.connect(ok_pressed)
    dialog_ui.print_usr_button.clicked.connect(print_users)

    dialog_window.exec()

    return selected

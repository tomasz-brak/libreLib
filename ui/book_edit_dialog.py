# Form implementation generated from reading ui file './ui//book_edit_dialog.ui'
#
# Created by: PyQt6 UI code generator 6.5.2
#
# WARNING: Any manual changes made to this file will be lost when pyuic6 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt6 import QtCore, QtGui, QtWidgets


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(400, 512)
        self.verticalLayout = QtWidgets.QVBoxLayout(Dialog)
        self.verticalLayout.setObjectName("verticalLayout")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.label_3 = QtWidgets.QLabel(parent=Dialog)
        self.label_3.setObjectName("label_3")
        self.horizontalLayout_3.addWidget(self.label_3)
        self.ID_edit = QtWidgets.QLineEdit(parent=Dialog)
        self.ID_edit.setReadOnly(True)
        self.ID_edit.setObjectName("ID_edit")
        self.horizontalLayout_3.addWidget(self.ID_edit)
        self.verticalLayout_2.addLayout(self.horizontalLayout_3)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label_2 = QtWidgets.QLabel(parent=Dialog)
        self.label_2.setObjectName("label_2")
        self.horizontalLayout.addWidget(self.label_2)
        self.Author_edit = QtWidgets.QLineEdit(parent=Dialog)
        self.Author_edit.setObjectName("Author_edit")
        self.horizontalLayout.addWidget(self.Author_edit)
        self.verticalLayout_2.addLayout(self.horizontalLayout)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.label = QtWidgets.QLabel(parent=Dialog)
        self.label.setObjectName("label")
        self.horizontalLayout_2.addWidget(self.label)
        self.Title_edit = QtWidgets.QLineEdit(parent=Dialog)
        self.Title_edit.setObjectName("Title_edit")
        self.horizontalLayout_2.addWidget(self.Title_edit)
        self.verticalLayout_2.addLayout(self.horizontalLayout_2)
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.label_4 = QtWidgets.QLabel(parent=Dialog)
        self.label_4.setObjectName("label_4")
        self.horizontalLayout_4.addWidget(self.label_4)
        self.year_published_edit = QtWidgets.QLineEdit(parent=Dialog)
        self.year_published_edit.setObjectName("year_published_edit")
        self.horizontalLayout_4.addWidget(self.year_published_edit)
        self.verticalLayout_2.addLayout(self.horizontalLayout_4)
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.label_5 = QtWidgets.QLabel(parent=Dialog)
        self.label_5.setObjectName("label_5")
        self.horizontalLayout_5.addWidget(self.label_5)
        self.volume_edit = QtWidgets.QLineEdit(parent=Dialog)
        self.volume_edit.setObjectName("volume_edit")
        self.horizontalLayout_5.addWidget(self.volume_edit)
        self.verticalLayout_2.addLayout(self.horizontalLayout_5)
        self.horizontalLayout_6 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_6.setObjectName("horizontalLayout_6")
        self.label_6 = QtWidgets.QLabel(parent=Dialog)
        self.label_6.setObjectName("label_6")
        self.horizontalLayout_6.addWidget(self.label_6)
        self.publisher_edit = QtWidgets.QLineEdit(parent=Dialog)
        self.publisher_edit.setObjectName("publisher_edit")
        self.horizontalLayout_6.addWidget(self.publisher_edit)
        self.verticalLayout_2.addLayout(self.horizontalLayout_6)
        self.horizontalLayout_7 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_7.setObjectName("horizontalLayout_7")
        self.label_7 = QtWidgets.QLabel(parent=Dialog)
        self.label_7.setObjectName("label_7")
        self.horizontalLayout_7.addWidget(self.label_7)
        self.price_edit = QtWidgets.QLineEdit(parent=Dialog)
        self.price_edit.setObjectName("price_edit")
        self.horizontalLayout_7.addWidget(self.price_edit)
        self.verticalLayout_2.addLayout(self.horizontalLayout_7)
        self.horizontalLayout_8 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_8.setObjectName("horizontalLayout_8")
        self.label_8 = QtWidgets.QLabel(parent=Dialog)
        self.label_8.setObjectName("label_8")
        self.horizontalLayout_8.addWidget(self.label_8)
        self.isbn_edit = QtWidgets.QLineEdit(parent=Dialog)
        self.isbn_edit.setObjectName("isbn_edit")
        self.horizontalLayout_8.addWidget(self.isbn_edit)
        self.searchButton = QtWidgets.QPushButton(parent=Dialog)
        self.searchButton.setObjectName("searchButton")
        self.horizontalLayout_8.addWidget(self.searchButton)
        self.verticalLayout_2.addLayout(self.horizontalLayout_8)
        self.horizontalLayout_9 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_9.setObjectName("horizontalLayout_9")
        self.label_9 = QtWidgets.QLabel(parent=Dialog)
        self.label_9.setObjectName("label_9")
        self.horizontalLayout_9.addWidget(self.label_9)
        self.location_comboBox = QtWidgets.QComboBox(parent=Dialog)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.location_comboBox.sizePolicy().hasHeightForWidth())
        self.location_comboBox.setSizePolicy(sizePolicy)
        self.location_comboBox.setObjectName("location_comboBox")
        self.horizontalLayout_9.addWidget(self.location_comboBox)
        self.verticalLayout_2.addLayout(self.horizontalLayout_9)
        self.verticalLayout.addLayout(self.verticalLayout_2)
        self.buttonBox = QtWidgets.QDialogButtonBox(parent=Dialog)
        self.buttonBox.setOrientation(QtCore.Qt.Orientation.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.StandardButton.Cancel|QtWidgets.QDialogButtonBox.StandardButton.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.verticalLayout.addWidget(self.buttonBox)

        self.retranslateUi(Dialog)
        self.buttonBox.accepted.connect(Dialog.accept) # type: ignore
        self.buttonBox.rejected.connect(Dialog.reject) # type: ignore
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.label_3.setText(_translate("Dialog", "ID:"))
        self.label_2.setText(_translate("Dialog", "Author:"))
        self.label.setText(_translate("Dialog", "Title:"))
        self.label_4.setText(_translate("Dialog", "Year Published:"))
        self.label_5.setText(_translate("Dialog", "Volume:"))
        self.label_6.setText(_translate("Dialog", "Publisher:"))
        self.label_7.setText(_translate("Dialog", "Price:"))
        self.label_8.setText(_translate("Dialog", "ISBN:"))
        self.searchButton.setText(_translate("Dialog", "Search"))
        self.label_9.setText(_translate("Dialog", "Location: "))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Dialog = QtWidgets.QDialog()
    ui = Ui_Dialog()
    ui.setupUi(Dialog)
    Dialog.show()
    sys.exit(app.exec())

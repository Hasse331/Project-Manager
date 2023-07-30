
import os
import PyQt5

from PyQt5.QtWidgets import QWidget
from PyQt5.QtWidgets import QApplication as Qapp, QTextEdit, QFileDialog, QMessageBox, QStyle, QDateEdit, QHeaderView, QAbstractItemView, QTableWidget, QTableWidgetItem, QVBoxLayout, QCheckBox, QDialog, QMainWindow as Qmain, QLineEdit as Qline, QLabel as Qlab, QPushButton as Qbtn
from PyQt5.QtCore import pyqtSignal, QTimer, QDate

import data_locations


#data locations
locations = data_locations.set_locations()
datafiles_folder = locations["datafiles_folder"]
folder_location_txt = locations["folder_location_txt"]
project_folder = locations["project_folder"]



class RenameAndSetTop(QDialog):
    rename_input_submitted = pyqtSignal(str, str, str)

    def __init__(self, name, date):
        super().__init__()
        self.setWindowTitle("Rename Project && Set DL")

        self.old_name = name
        self.old_date = date

        layout = QVBoxLayout()
        layout.setSpacing(10)  # Adjust the spacing between widgets
        layout.setContentsMargins(10, 10, 10, 10)
        
        self.setLayout(layout)

        # Project name label and input field
        label = Qlab("Rename Project:", self)
        layout.addWidget(label)

        #field
        self.project_input_field = Qline(self)
        layout.addWidget(self.project_input_field)

        # checkbox
        self.deadline_checkbox = QCheckBox("No Deadline")
        self.deadline_checkbox.setChecked(True)
        layout.addWidget(self.deadline_checkbox)
        self.deadline_checkbox.stateChanged.connect(self.toggle_date_input_field)
        #checkbox editing
        self.deadline_checkbox.setEnabled(False)
        if date == "-":
            self.deadline_checkbox.setEnabled(True)

        #input label
        label2 = Qlab("Set Project Deadline:<br><font size='2'>dd.mm.yy</font>", self)
        layout.addWidget(label2)

        #date input
        self.date_input_field = QDateEdit(self)
        self.date_input_field.setDisplayFormat("dd.MM.yy")
        self.date_input_field.setCalendarPopup(True)
        self.date_input_field.setMinimumDate(QDate.currentDate())
        self.date_input_field.setEnabled(False)
        layout.addWidget(self.date_input_field)

        # Add Project button
        self.add_button = Qbtn("Save New Name And DL", self)
        layout.addWidget(self.add_button)
        self.add_button.clicked.connect(self.file_naming)

    def toggle_date_input_field(self, state):
        self.date_input_field.setEnabled(state != 2)

    def file_naming(self):
        name_input = self.project_input_field.text()
        if any(not c.isalnum() and c not in ('-', ' ', '_', 'ä', 'ö', 'å', ',') for c in name_input):
            msg_box = QMessageBox()
            msg_box.setText("Please, don't use special marks like: !#¤%&/()=?:")
            msg_box.setWindowTitle("Message")
            msg_box.setStandardButtons(QMessageBox.Ok)
            msg_box.exec_()

        elif name_input == self.old_name:
            self.submit_input(name_input)
        else:
            file = os.path.join(datafiles_folder, name_input + ".txt")
            if os.path.exists(file):
                file_2 = name_input + "_" + "2"
                file2_dir = os.path.join(datafiles_folder, file_2 + ".txt")

                if not os.path.exists(file2_dir):
                    num_int = 2
                    name_input = name_input + "_" + str(num_int)
                    self.submit_input(name_input)

                else:
                    run = 1
                    while run == 1:
                        for X in range(20, 1, -1):
                            file2 = f"{name_input}_{X}.txt"
                            file_location = os.path.join(datafiles_folder, file2)

                            if os.path.exists(file_location):
                                X += 1
                                name_input = name_input + "_" + str(X)
                                self.submit_input(name_input)
                                run = 0
                                if run == 0:
                                    break
            else:
                self.submit_input(name_input)

    def submit_input(self, name_input):
        date_input = self.date_input_field.text()

        if name_input and not self.deadline_checkbox.isChecked():
            self.rename_input_submitted.emit(name_input, date_input, self.old_name)
            self.close()
        elif name_input and self.deadline_checkbox.isChecked():
            date_input = self.old_date
            self.rename_input_submitted.emit(name_input, date_input, self.old_name)
            self.close()
        elif not name_input and not self.deadline_checkbox.isChecked():
            name_input = self.old_name
            self.rename_input_submitted.emit(name_input, date_input, self.old_name)
            self.close()
        else:
            pass


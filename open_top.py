
import os
import PyQt5
import platform


from PyQt5.QtWidgets import QWidget
from PyQt5.QtWidgets import QApplication as Qapp, QTextEdit, QFileDialog, QMessageBox, QStyle, QDateEdit, QHeaderView, QAbstractItemView, QTableWidget, QTableWidgetItem, QVBoxLayout, QCheckBox, QDialog, QMainWindow as Qmain, QLineEdit as Qline, QLabel as Qlab, QPushButton as Qbtn
from PyQt5.QtCore import pyqtSignal, QTimer, QDate

import data_locations
import remaining__timer

#data locations
locations = data_locations.set_locations()
datafiles_folder = locations["datafiles_folder"]
folder_location_txt = locations["folder_location_txt"]
project_folder = locations["project_folder"]


class OpenTop(QDialog):

    def __init__(self, name, remaining, date):
        super().__init__()
        self.setWindowTitle("Project: " + name)
        self.setFixedSize(430, 550)
        layout = QVBoxLayout()
        self.setLayout(layout)

        #title
        self.title_label = Qlab(name + "\n\nProject Notes:")
        layout.addWidget(self.title_label)

        #to do/ notes list
        self.notes = QTextEdit(self)
        layout.addWidget(self.notes)
        self.load_notes(name)

        #create folder button
        self.create_button = Qbtn("Create Folder", self)
        self.create_button.setMaximumWidth(200)
        self.create_button.clicked.connect(lambda: self.create_folder(name))
        layout.addWidget(self.create_button)

        # open folder button
        self.open_button = Qbtn("Open Folder", self)
        self.open_button.setMaximumWidth(200)
        self.open_button.clicked.connect(lambda: self.open_folder(name))
        layout.addWidget(self.open_button)


        #save and exit button
        self.save_ae_button = Qbtn("Save && Exit", self)
        self.save_ae_button.setMaximumWidth(100)
        self.save_ae_button.clicked.connect(lambda: self.save_and_exit(name))
        layout.addWidget(self.save_ae_button)

        #small save button
        self.save_button = Qbtn(self)
        pixmapiS = QStyle.SP_DialogSaveButton
        icon_S = self.style().standardIcon(pixmapiS)
        self.save_button.setIcon(icon_S)
        self.save_button.setFixedSize(20, 20)
        self.save_button.setStyleSheet("Qbtn { border: none; }")
        self.save_button.clicked.connect(lambda: self.save_notes(name))
        #save_button.move(270, 55)
        layout.addWidget(self.save_button)


        #time label 
        self.time_label = Qlab()
        self.updated_label(remaining, date, layout)

        #update timer
        self.update_timer = QTimer(self)
        self.update_timer.timeout.connect(lambda: self.updated_label(remaining, date, layout))
        self.update_timer.start(1000)

    def updated_label(self, remaining, date, layout):

        self.time_label.deleteLater()
        place = remaining__timer.RemainingTimer()
        remaining = place.update(date)
        self.time_label = Qlab("\n\nTime Remaining:      " + remaining + "\nDeadline Date:         " + date, self)
        layout.addWidget(self.time_label)

    def save_notes(self, name):
        filename = os.path.join (datafiles_folder, name + ".txt")
        text = self.notes.toPlainText()  # Get the text from the QTextEdit
        with open(filename, "w") as file:
            file.write(text) # Save the text to a file

    def save_and_exit(self, name):
        filename = os.path.join (datafiles_folder, name + ".txt")
        text = self.notes.toPlainText()  # Get the text from the QTextEdit
        with open(filename, "w") as file:
            file.write(text)  # Save the text to a file
        self.close()

    def load_notes(self, name):
        filename = os.path.join (datafiles_folder, name + ".txt")

        if os.path.exists(filename):
            with open(filename, "r") as file:
                text = file.read()  # Read the text from the file
            self.notes.setPlainText(text)  # Set the text in the QTextEdit
        else:
            pass

    def create_folder(self, name):
        datafiles_folder = name

        if os.path.exists(folder_location_txt):
            new_dir =  os.path.join(project_folder, datafiles_folder) 
            if not os.path.exists(new_dir):
                os.makedirs(new_dir)
                msg_box = QMessageBox()
                msg_box.setText("New Folder Made In Project Folder: " + project_folder)
                msg_box.setWindowTitle("Message")
                msg_box.setStandardButtons(QMessageBox.Ok)
                msg_box.exec_()
            else:
                msg_box = QMessageBox()
                msg_box.setText("Project Folder Already Exists")
                msg_box.setWindowTitle("Message")
                msg_box.setStandardButtons(QMessageBox.Ok)
                msg_box.exec_()

        else:
            if not os.path.exists(datafiles_folder):
                os.makedirs(datafiles_folder)
                msg_box = QMessageBox()
                msg_box.setText("New Folder Made In Default Location")
                msg_box.setWindowTitle("Message")
                msg_box.setStandardButtons(QMessageBox.Ok)
                msg_box.exec_()
            else:
                msg_box = QMessageBox()
                msg_box.setText("Project folder Already Exists")
                msg_box.setWindowTitle("Message")
                msg_box.setStandardButtons(QMessageBox.Ok)
                msg_box.exec_()

    def open_folder(self, name):
        system = platform.system()
        
        if os.path.exists(folder_location_txt):
            new_dir =  os.path.join(project_folder, name)
            if os.path.exists(new_dir):
                if system == "Windows":
                    os.startfile(f'{new_dir}')
                elif system == "Darwin":  # macOS
                    os.system(f'open "{new_dir}"')
                elif system == "Linux":
                    os.system(f'xdg-open "{new_dir}"')
                else:
                    print("Unsupported operating system.")

            else:
                msg_box = QMessageBox()
                msg_box.setText("Please, create the project folder first")
                msg_box.setWindowTitle("Message")
                msg_box.setStandardButtons(QMessageBox.Ok)
                msg_box.exec_()

        else:
            if os.path.exists(name):
                if system == "Windows":
                    os.startfile(f'{name}')
                elif system == "Darwin":  # macOS
                    os.system(f'open "{name}"')
                elif system == "Linux":
                    os.system(f'xdg-open "{name}"')
                else:
                    print("Unsupported operating system.")

            else:
                msg_box = QMessageBox()
                msg_box.setText("Please, create the project folder first")
                msg_box.setWindowTitle("Message")
                msg_box.setStandardButtons(QMessageBox.Ok)
                msg_box.exec_()
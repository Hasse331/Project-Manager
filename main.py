import sys
import subprocess
import csv
import os
import shutil
import platform

#module imports:

import First_run_top
import data_locations
import new_top
import open_top
import remaining__timer
import rename_top

from datetime import datetime


def install_depedencies():
    requirements = [
        'PyQt5',
    ]
    #version used when developing: PyQt5==5.15.9

    for requirement in requirements:
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', '--upgrade', 'pip'])
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', requirement])

try:
    import PyQt5

    from PyQt5.QtWidgets import QWidget
    from PyQt5.QtWidgets import QApplication as Qapp, QTextEdit, QFileDialog, QMessageBox, QStyle, QDateEdit, QHeaderView, QAbstractItemView, QTableWidget, QTableWidgetItem, QVBoxLayout, QCheckBox, QDialog, QMainWindow as Qmain, QLineEdit as Qline, QLabel as Qlab, QPushButton as Qbtn
    from PyQt5.QtCore import pyqtSignal, QTimer, QDate
    #from octicons import Octicon
except ImportError:
    print("Installing depedencies...")
    install_depedencies()
    sys.exit()

#data locations
locations = data_locations.set_locations()
datafiles_folder = locations["datafiles_folder"]
folder_location_txt = locations["folder_location_txt"]
project_folder = locations["project_folder"]




#main
class MainWindow(Qmain):
    def __init__(self):
        super().__init__()

        window = Qmain()

        self.setWindowTitle('Project Manager V2')
        self.setFixedSize(430, 550)

        self.title_label = Qlab("Project Manager", self)
        self.title_label.setGeometry(50, 10, 200, 30)

        #project overview label
        self.projects_label = Qlab("Project overview", self)
        self.projects_label.setGeometry(50, 50, 200, 30)

        #Project ovewview list
        self.project_list = QTableWidget(0, 3, self)
        self.project_list.setGeometry(50, 80, 340, 325)
        self.project_list.setColumnHidden(2, True)
        self.project_list.setColumnWidth(0, 250)
        self.project_list.setColumnWidth(1, 20)
        self.project_list.setHorizontalHeaderLabels(["Projects:", "Status"])
        self.project_list.horizontalHeader().setSectionResizeMode(QHeaderView.Fixed)
        self.project_list.horizontalHeader().setStretchLastSection(True)
        self.project_list.setEditTriggers(QAbstractItemView.NoEditTriggers)

        #shortcuts:
        self.project_list.doubleClicked.connect(self.open_project_top)

        #hide row checkbox
        self.hide_row_numbers_checkbox = QCheckBox("Hide Priority")
        self.hide_row_numbers_checkbox.setGeometry(50, 405, 120, 30)  
        self.hide_row_numbers_checkbox.setParent(self)
        self.hide_row_numbers_checkbox.stateChanged.connect(self.toggle_row_numbers)

        #Completed
        self.comp_button = Qbtn("Project Ready", self)
        self.comp_button.setGeometry(50, 445, 150, 30)
        self.comp_button.clicked.connect(self.project_completed)

        #Rename and dl
        self.comp_button = Qbtn("Rename and Deadline", self)
        self.comp_button.setGeometry(205, 445, 150, 30)
        self.comp_button.clicked.connect(self.open_rename_set_top)

        #Folder Location
        self.comp_button = Qbtn("Select Folder", self)
        self.comp_button.setGeometry(50, 480, 150, 30)
        self.comp_button.clicked.connect(self.set_folder_dir)

        #Save and ex
        self.comp_button = Qbtn("Save And Exit", self)
        self.comp_button.setGeometry(205, 480, 150, 30)
        self.comp_button.clicked.connect(self.save_and_exit)

        """
        #Backup btn
        self.backup_btn = Qbtn("Backup", self)
        self.backup_btn.setGeometry(50, 515, 100, 30)
        self.backup_btn.clicked.connect(self.backup_button)
        """
        
        #SMALL BUTTONS:
        #Backup settings
        """
        button_backup = Qbtn(self)
        pixmapiN = QStyle.SP_DriveDVDIcon
        icon_N = self.style().standardIcon(pixmapiN)
        button_backup.setIcon(icon_N)
        button_backup.setFixedSize(20, 20)
        button_backup.setStyleSheet("Qbtn { border: none; }")
        button_backup.clicked.connect(self.backup_settings)
        button_backup.move(150, 515)
        """

        #new button
        button_new = Qbtn(self)
        pixmapiN = QStyle.SP_FileDialogNewFolder
        icon_N = self.style().standardIcon(pixmapiN)
        button_new.setIcon(icon_N)
        button_new.setFixedSize(20, 20)
        button_new.setStyleSheet("Qbtn { border: none; }")
        button_new.clicked.connect(self.open_new_project_top)
        button_new.move(180, 55)

        #open button
        button_open = Qbtn(self)
        pixmapiOP = QStyle.SP_FileDialogStart
        icon_OP = self.style().standardIcon(pixmapiOP)
        button_open.setIcon(icon_OP)
        button_open.setFixedSize(20, 20)
        button_open.setStyleSheet("Qbtn { border: none; }")
        button_open.clicked.connect(self.open_project_top)
        button_open.move(210, 55)

        #save Changes button
        save_button = Qbtn(self)
        pixmapiS = QStyle.SP_DialogSaveButton
        icon_S = self.style().standardIcon(pixmapiS)
        save_button.setIcon(icon_S)
        save_button.setFixedSize(20, 20)
        save_button.setStyleSheet("Qbtn { border: none; }")
        save_button.clicked.connect(self.save_changes)
        save_button.move(240, 55)

        #del but no data btn
        button_trash = Qbtn(self)
        pixmapiT = QStyle.SP_DialogCancelButton
        icon_T = self.style().standardIcon(pixmapiT)
        button_trash.setIcon(icon_T)
        button_trash.setFixedSize(20, 20)
        button_trash.setStyleSheet("Qbtn { border: none; }")
        button_trash.clicked.connect(self.delete_button_no_data)
        button_trash.move(270, 55)

        #del btn
        button_trash = Qbtn(self)
        pixmapiT = QStyle.SP_MessageBoxCritical
        icon_T = self.style().standardIcon(pixmapiT)
        button_trash.setIcon(icon_T)
        button_trash.setFixedSize(20, 20)
        button_trash.setStyleSheet("Qbtn { border: none; }")
        button_trash.clicked.connect(self.delete_button)
        button_trash.move(300, 55)

        #btn up
        button_up = Qbtn(self)
        pixmapiAU = QStyle.SP_ArrowUp
        icon_AU = self.style().standardIcon(pixmapiAU)
        button_up.setIcon(icon_AU)
        button_up.setFixedSize(20, 20)
        button_up.setStyleSheet("Qbtn { border: none; }")
        button_up.clicked.connect(self.move_column_up)
        button_up.move(330, 55)

        #btn down
        button_down = Qbtn(self)
        pixmapiAD = QStyle.SP_ArrowDown
        icon_AD = self.style().standardIcon(pixmapiAD)
        button_down.setIcon(icon_AD)
        button_down.setFixedSize(20, 20)
        button_down.setStyleSheet("Qbtn { border: none; }")
        button_down.clicked.connect(self.move_column_down)
        button_down.move(360, 55)

        self.load_saved_inputs()
#columnds and row numbers
    def move_column_up(self):
        current_row = self.project_list.currentRow()
        if current_row > 0:
            self.project_list.insertRow(current_row - 1)
            for column in range(self.project_list.columnCount()):
                item = self.project_list.takeItem(current_row + 1, column)
                self.project_list.setItem(current_row - 1, column, item)

            self.project_list.removeRow(current_row + 1)
            self.project_list.setCurrentCell(current_row - 1, 0)

    def move_column_down(self):
        current_row = self.project_list.currentRow()
        if current_row >= 0 and current_row < self.project_list.rowCount() - 1:
            self.project_list.insertRow(current_row + 2)
            for column in range(self.project_list.columnCount()):
                item = self.project_list.takeItem(current_row, column)
                self.project_list.setItem(current_row + 2, column, item)

            self.project_list.removeRow(current_row)
            self.project_list.setCurrentCell(current_row + 1, 0)

    def toggle_row_numbers(self):
        is_hidden = self.hide_row_numbers_checkbox.isChecked()
        self.project_list.verticalHeader().setVisible(not is_hidden)
#open tops
    def open_new_project_top(self):
        self.new_project_window = new_top.NewTop()
        self.new_project_window.project_input_submitted.connect(self.handle_new)
        self.new_project_window.exec()

    def open_project_top(self):

        if self.project_list.currentRow() >= 0:

            current_row = self.project_list.currentRow()
            column_count = self.project_list.columnCount()

            row = []
            for column in range(column_count):
                item = self.project_list.item(current_row, column)
                if item is not None:
                    row.append(item.text())

            name = row[0]
            remaining = row[1]
            date = row[2]

            self.open_window = open_top.OpenTop(name, remaining, date)
            self.open_window.exec()

    def open_rename_set_top(self):
        #Get project name and dl
        if self.project_list.currentRow() >= 0:

            current_row = self.project_list.currentRow()
            column_count = self.project_list.columnCount()

            row = []
            for column in range(column_count):
                item = self.project_list.item(current_row, column)
                if item is not None:
                    row.append(item.text())

            name = row[0]
            date = row[2]
        self.rename_and_dl = rename_top.RenameAndSetTop(name, date)
        self.rename_and_dl.rename_input_submitted.connect(self.handle_rename)
        self.rename_and_dl.exec()
#folder dir
    def set_folder_dir(self):
        global project_folder   
        if not os.path.exists(folder_location_txt):
            project_folder = os.path.dirname(os.path.realpath(__file__))
        reply = QMessageBox.question(self, 'Select Project Folder', 'If you have already exsisting project folders you have to move the folders manually in the new location you select.\n\n Your current project folder location is here:\n\n' + project_folder + '\n\nAre you sure you want to continue?', 
                        QMessageBox.Yes | QMessageBox.No, QMessageBox.No)

        if reply == QMessageBox.Yes:
            folder_path = QFileDialog.getExistingDirectory(self, "Select Folder")
            if folder_path:
                
                if not os.path.exists(folder_path):
                    os.makedirs(folder_path)
                filename = os.path.join(datafiles_folder, "Projects_dir.txt")
                with open(filename, "w") as file:
                    file.write(folder_path)
                self.save_and_restart()
#handlers
    def handle_new(self, name_input, date_input):
        row_count = self.project_list.rowCount()
        next_row = 0

        place = remaining__timer.RemainingTimer()
        remaining = place.update(date_input)

        filename = os.path.join (datafiles_folder, name_input + ".txt")
        if not os.path.exists(filename):
            with open(filename, "w") as file:
                file.write("")

        if self.project_list.item(0,0) is None:
            self.project_list.insertRow(row_count)
            self.project_list.setItem(0, 0, QTableWidgetItem(name_input))
            self.project_list.setItem(0, 1, QTableWidgetItem(remaining))
            self.project_list.setItem(0, 2, QTableWidgetItem(date_input))


        else:
            while next_row < row_count and self.project_list.item(next_row, 0) is not None:
                next_row += 1

            self.project_list.insertRow(row_count)
            self.project_list.setItem(next_row, 0, QTableWidgetItem(name_input))
            self.project_list.setItem(next_row, 1, QTableWidgetItem(remaining))
            self.project_list.setItem(next_row, 2, QTableWidgetItem(date_input))
        self.save_changes()

    def handle_rename(self, name_input, date_input, old_name):
        #delete old project fom list
        selected_row = self.project_list.currentRow()
        
        #Handling renaming project datafiles
        try:
            old_folder = os.path.join(project_folder, old_name)
            new_folder = os.path.join(project_folder, name_input)
        except NameError:
            old_folder = old_name
            new_folder = name_input

        old_notes = os.path.join(datafiles_folder, old_name + ".txt")
        new_notes = os.path.join(datafiles_folder, name_input + ".txt")

        try:
            if os.path.exists(old_folder):
                os.rename(old_folder, new_folder)
                self.project_list.removeRow(selected_row)
            if os.path.exists(old_notes):
                os.rename(old_notes, new_notes)
                self.project_list.removeRow(selected_row)
            self.handle_new(name_input, date_input)

        except PermissionError:
            msg_box = QMessageBox()
            msg_box.setText("Please, close all the open files before renaming")
            msg_box.setWindowTitle("Message")
            msg_box.setStandardButtons(QMessageBox.Ok)
            msg_box.exec_()
#save, load, delete etc
    def save_and_exit(self):
        self.save_changes()
        self.close()

    def save_changes(self):
        row_count = self.project_list.rowCount()
        column_count = self.project_list.columnCount()
        filename = os.path.join (datafiles_folder, "save.txt")
        with open(filename, mode='w', newline='') as file:
            writer = csv.writer(file)

            # Iterate over each cell in the grid
            for row in range(row_count):
                row_data = []

                for column in range(column_count):
                    # Retrieve the text from the cell
                    cell_text = self.project_list.item(row, column).text()

                    # Append the text to the row data
                    row_data.append(cell_text)

                # Write the row data to the CSV file
                writer.writerow(row_data)

    def delete_button(self):

        if self.project_list.currentRow() >= 0:

            selected_row = self.project_list.currentRow()
            column_count = self.project_list.columnCount()

            row = []
            for column in range(column_count):
                item = self.project_list.item(selected_row, column)
                if item is not None:
                    row.append(item.text())

            name = row[0]

                
            reply = QMessageBox.question(self, 'Confirmation', 'Delete project and all project data.?', 
                                        QMessageBox.Yes | QMessageBox.No, QMessageBox.No)

            if reply == QMessageBox.Yes:
                #remove project form list
                

                try:

                    #If project folder exsists
                    if os.path.exists(folder_location_txt):
                        del_loc = os.path.join(project_folder, name)
                        if os.path.exists(del_loc):
                            if name != "PMS_datafiles":
                                shutil.rmtree(del_loc)

                    else:

                        if os.path.exists(name):
                            if name != "PMS_datafiles":
                                shutil.rmtree(name)

                    #delete notes
                    notes_path = os.path.join(datafiles_folder, name + ".txt")
                    if os.path.exists(notes_path):
                        os.remove(notes_path)
                    self.project_list.removeRow(selected_row)
                    self.save_changes()

                except PermissionError:
                    msg_box = QMessageBox()
                    msg_box.setText("Please, close all the open files before the deletion")
                    msg_box.setWindowTitle("Message")
                    msg_box.setStandardButtons(QMessageBox.Ok)
                    msg_box.exec_()

    def delete_button_no_data(self):
        if self.project_list.currentRow() >= 0:

            selected_row = self.project_list.currentRow()
            column_count = self.project_list.columnCount()

            row = []
            for column in range(column_count):
                item = self.project_list.item(selected_row, column)
                if item is not None:
                    row.append(item.text())

            name = row[0]

                
            reply = QMessageBox.question(self, 'Confirmation', 'Delete project and project notes only. Project folder will remain..', 
                                        QMessageBox.Yes | QMessageBox.No, QMessageBox.No)

            if reply == QMessageBox.Yes:
                #remove project form list
                

                try:

                    #delete notes
                    notes_path = os.path.join(datafiles_folder, name + ".txt")
                    if os.path.exists(notes_path):
                        os.remove(notes_path)
                    self.project_list.removeRow(selected_row)
                    self.save_changes()

                except PermissionError:
                    msg_box = QMessageBox()
                    msg_box.setText("Please, close all the open files before the deletion")
                    msg_box.setWindowTitle("Message")
                    msg_box.setStandardButtons(QMessageBox.Ok)
                    msg_box.exec_()

    def load_saved_inputs(self):
        try:
            filename = os.path.join (datafiles_folder, "save.txt")
            with open(filename, "r") as file:
                reader = csv.reader(file)
                data = list(reader)
                
                
                # Clear the existing data in the grid
                #self.project_list.clearContents()
                #self.project_list.setRowCount(0)
                
                # Iterate over the rows in the data list
                for row in data:
                    name_input = row[0]
                    date_input = row[2]
                    place = remaining__timer.RemainingTimer()
                    remaining = place.update(date_input)

                    row_count = self.project_list.rowCount()
                    self.project_list.insertRow(row_count)
                    self.project_list.setItem(row_count, 0, QTableWidgetItem(name_input))
                    self.project_list.setItem(row_count, 1, QTableWidgetItem(remaining))
                    self.project_list.setItem(row_count, 2, QTableWidgetItem(date_input))

        except FileNotFoundError:
            pass

    def project_completed(self):

        if self.project_list.currentRow() == -1:
            pass
        else:
        
            reply = QMessageBox.question(self, 'Confirmation', 'Project status can not be changed after this action.\n\nAre you sure you want to mark this project as completed?', 
                                            QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
            
            if reply == QMessageBox.Yes:
                remaining = "Ready"
                date = "Ready"
                current_row = self.project_list.currentRow()
                self.project_list.setItem(current_row, 1, QTableWidgetItem(remaining))
                self.project_list.setItem(current_row, 2, QTableWidgetItem(date))

    def save_and_restart(self):
        self.save_changes()
        python = sys.executable
        os.execl(python, python, '"' + ' '.join(sys.argv) + '"')



if __name__ == "__main__":
    app = Qapp(sys.argv)

    config_file = "config.txt"
    first_run_handler = First_run_top.FirstRunHandler(config_file)

    if first_run_handler.is_first_run():
        first_run = First_run_top.FirstRunTop()
        first_run.exec()

        first_run_handler.mark_as_not_first_run()

    else:
        pass



main_window = MainWindow()
main_window.show()
sys.exit(app.exec())
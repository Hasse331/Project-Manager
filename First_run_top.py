import PyQt5
import os

from PyQt5.QtWidgets import QFileDialog, QVBoxLayout, QDialog, QLabel as Qlab, QPushButton as Qbtn


import data_locations
import First_run_top


#data locations
locations = data_locations.set_locations()
datafiles_folder = locations["datafiles_folder"]
folder_location_txt = locations["folder_location_txt"]
project_folder = locations["project_folder"]

class FirstRunHandler:
    def __init__(self, config_file):
        self.config_file = "config.txt"

    def is_first_run(self):
        filename = os.path.join(datafiles_folder, "config.txt")
        return not os.path.exists(filename)

    def mark_as_not_first_run(self):
        
        if not os.path.exists(datafiles_folder):
            os.makedirs(datafiles_folder)
        
        filename = os.path.join(datafiles_folder, "config.txt")
        with open(filename, "w") as file:
            file.write("")

class FirstRunTop(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Welcome!')
        self.setFixedSize(500, 250)
        
        layout = QVBoxLayout()
        self.setLayout(layout)

        self.title_label = Qlab("Welcome To Minimalistic Project Manager For The First Time!\n\n How to get started: \n 1. Select your project folder location first. \n 2. Create new project. You can rename and set deadline later if you haven't already. \n 3. Create project folder and write notes. \n 4. Manage multiple projects in priority, access you project folder and notes quickly. \n 5. Delete projects and all project data at once if you choose to do so. \n\n Have Fun!", self)
        layout.addWidget(self.title_label)
        self.title_label.setMaximumWidth(500)
        self.cont_button = Qbtn("Use Default Project Folder", self)


        self.set_loc_button = Qbtn("Select Projct Folder", self)
        self.set_loc_button.clicked.connect(self.start_set_path)
        self.cont_button.clicked.connect(self.close)
        layout.addWidget(self.set_loc_button)
        layout.addWidget(self.cont_button)
    
    def start_set_path(self):
        config_file = "config.txt"
        FirstRunHandler.mark_as_not_first_run(self)

        folder_path = QFileDialog.getExistingDirectory(self, "Select Folder")

        if folder_path:
            
            if not os.path.exists(folder_path):
                os.makedirs(folder_path)
            filename = os.path.join(datafiles_folder, "Projects_dir.txt")
            with open(filename, "w") as file:
                file.write(folder_path)
            self.close()


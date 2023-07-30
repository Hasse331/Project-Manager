import os

def set_locations():
    datafiles_folder = "PMS_datafiles"
    folder_location_txt = os.path.join(datafiles_folder, "Projects_dir.txt") 
    project_folder = ""
    if os.path.exists(folder_location_txt):
        with open(folder_location_txt, "r") as file:
            dir = file.read()  # Read the text from the file
            project_folder = dir
    locations = {"datafiles_folder": datafiles_folder, "folder_location_txt": folder_location_txt, "project_folder": project_folder}
    return locations
    
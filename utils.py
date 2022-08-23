import os 

def create_folder(folder_name):
    if not os.path.exists(folder_name):
        os.mkdir(folder_name)
import os
import sys
import cv2
import json
import tkinter as tk
import tkinter.filedialog

import os.path
from os import path

from tkinter import *
from tkvideo import tkvideo
from PIL import Image, ImageTk

from win32api import GetSystemMetrics

# def getFileName(image):
#     print str(image)

# Function to access relative path to a resource within the PyInstaller tmp folder
def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)
    
def get_path(filename):
    if hasattr(sys, "_MEIPASS"):
        return f'{os.path.join(sys._MEIPASS, filename)}'
    else:
        return f'{filename}'

class DataProcessingTool:
    def __init__(self, master):
        self.master = master
        master.title("MoveAhead Data Processing Tool")

        self.drip_map = {}
        # Place buttons for additional functionality
        self.select_folder_button = tk.Button(master, text="Select Folder", command=self.select_folder)
        self.select_folder_button.place(x=5, y=20)

        self.save_drip_map_button = tk.Button(master, text="Save Results", command=self.save_json)
        self.save_drip_map_button.place(x=5, y=80)

    def select_folder(self):
        folder_path = tk.filedialog.askdirectory()
        self.folder_path = folder_path

        # Store contents of the folder in a list to display in GUI
        folder_contents = []

        max_len = 0
        for item in os.listdir(folder_path):
            if len(item) > max_len:
                max_len = len(item)

            # Add file name to folder
            folder_contents.append(item)

        # # create listbox object
        # listbox = tk.Listbox(width=max_len+2, bg = "white", activestyle = 'dotbox', fg = "black")

        # # Populate listbox with contents from the selected folder
        # for index, item in enumerate(folder_contents):
        #     listbox.insert(index, item)

        # listbox.place(x=25, y=80)
        
        self.start_processing_button = tk.Button(self.master, text="Start Processing", command=self.process_folder)
        self.start_processing_button.place(x=200, y=50)

    def save_json(self):

        def import_json(json_path):
            with open(json_path, "r") as f:
                json_data = json.load(f)

            return json_data

        def add_results(drip_map, exists):
            if exists:
                logged_results = import_json("results.json")
            else:
                logged_results = {} 

            merged_logs = {**drip_map, **logged_results}

            with open("results.json", mode='w+') as json_file:
                json.dump(merged_logs, json_file)

            return

        if path.exists("results.json"):
            add_results(self.drip_map, True)
        else:
            add_results(self.drip_map, False)



    def process_folder(self):

        def import_json(json_path):
            with open(json_path, "r") as f:
                json_data = json.load(f)

            return json_data

        def get_results_file():
            if path.exists("results.json"):
                log = import_json("results.json")
            else:
                log = {}

            return log

        self.log = get_results_file()
        prev_assessed_clothes = list(self.log.keys())

        dset_path = os.listdir("clothes_dataset/")
        remaining_clothes = [x for x in os.listdir(self.folder_path) if x not in self.log.keys()]

        for image_name in remaining_clothes:
            img_path = self.folder_path + "/" + image_name
            if image_name in dset_path:
                self.temp_video_gui(img_path, image_name)

        # Close GUI once uploads have been completed.
        self.master.destroy()


    def temp_video_gui(selff, output_path, image_name):

        # Initialize second GUI to handle video annotation and processing (tk.Toplevel since another GUI instance is already running)
        temp_gui = tk.Toplevel()

        pad = 3
        temp_gui.geometry("{0}x{1}+0+0".format(temp_gui.winfo_screenwidth()-pad, temp_gui.winfo_screenheight()-pad))

        # selff.save_drip_map_button = tk.Button(master, text="Save Results", command=self.save_json)
        # selff.save_drip_map_button.place(x=400, y=50)

        temp_gui.resizable(0, 0)
        temp_gui.title(image_name) 

        try:
            # Load Dataset Image into GUI
            dataset_image = Image.open(output_path)
                
            # Get image dimensions
            img = cv2.imread(output_path)
            img_height, img_width, _ = img.shape
            screen_width = GetSystemMetrics(0)
            screen_height = GetSystemMetrics(1)

            # Get ratio of image height to screen height 
            ratio = screen_height / img_height 

            dataset_image = dataset_image.resize(( int(img_width * ratio), int(img_height * ratio)), Image.ANTIALIAS)
            tk_dataset_img = ImageTk.PhotoImage(dataset_image)


            # Create canvas to display image
            canvas = Canvas(temp_gui, width = GetSystemMetrics(0), height = GetSystemMetrics(1))  
            canvas.pack()
            canvas.create_image(20, 20, anchor=NW, image= tk_dataset_img)  

            l2 = tk.Label(temp_gui, text="ID: {}".format(image_name), font=("Arial", 20))
            l2.place(x=800, y=120)


            def leftKey(event):
                selff.drip_map[image_name] = "not_drip"
                temp_gui.destroy()

            def rightKey(event):
                selff.drip_map[image_name] = "drip"
                print(selff.drip_map)
                temp_gui.destroy()

            frame = Frame(selff.master, width=500, height=500)
            selff.master.bind('<Left>', leftKey)
            selff.master.bind('<Right>', rightKey)
            frame.pack()

                # Wait until the window is closed to open the next
            temp_gui.wait_window()

        except:
            temp_gui.destroy()
 

def create_folder(folder_name):
    # used to create folders
    if not os.path.exists(folder_name):
        os.mkdir(folder_name)

    return


def main():

    # Create class folders
    create_folder("labelled_dataset/")
    create_folder("labelled_dataset/not_drip/")
    create_folder("labelled_dataset/drip/")
    # Load Tkinter root window
    window = tk.Tk()
    window.geometry("600x300")
    window.resizable(width=False, height=False)

    gui = DataProcessingTool(window)

    # Iinitialise event listener to wait for interactions with GUI elements
    window.mainloop()

if __name__ == "__main__":
    main()
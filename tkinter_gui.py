import tkinter as tk
from tkinter import *
import tkinter.filedialog
import os
import sys
from PIL import Image, ImageTk
from tkvideo import tkvideo

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

        # Load MoveAhead Logo into GUI
        image = Image.open("moveahead_logo.png")
        image = Image.open(get_path("moveahead_logo.png"))
        image = image.resize((150, 40), Image.ANTIALIAS)

        logo = ImageTk.PhotoImage(image)

        self.label = tk.Label(master, image=logo)
        self.label.photo = logo
        self.label.pack()

        # Class variables
        self.start_date = None
        self.end_date = None

        # with open("config.json", "r") as f:
        #     # Load S3 Bucket credentials from config.json
        #     self.config = json.load(f)

        # Place buttons for additional functionality
        self.select_folder_button = tk.Button(master, text="Select Folder", command=self.select_folder)
        self.select_folder_button.place(x=25, y=50)

        # self.generate_report_button = tk.Button(master, text="Generate Report", command=self.generate_report)
        # self.generate_report_button.place(x=125, y=50)

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

        # create listbox object
        listbox = tk.Listbox(
                        width=max_len+2,
                        bg = "white",
                        activestyle = 'dotbox', 
                        fg = "black")

        # Populate listbox with contents from the selected folder
        for index, item in enumerate(folder_contents):
            listbox.insert(index, item)

        listbox.place(x=25, y=80)
        
        self.start_processing_button = tk.Button(self.master, text="Start Processing", command=self.process_folder)
        self.start_processing_button.place(x=125, y=80)

    def process_folder(self):

        for image_name in os.listdir(self.folder_path):
            # meta_dict = ffmpeg.probe("{}/{}".format(video_folder_path, video), cmd="ffmpeg/ffprobe.exe")
            # print("IMAGE ", image)
            output_path = self.folder_path + "/" + image_name
            print("OUTPATH_PATH:", output_path)
            self.temp_video_gui(output_path, image_name)

        # Close GUI once uploads have been completed.
        self.master.destroy()


    def temp_video_gui(self, output_path, image_name):

        # Initialize second GUI to handle video annotation and processing (tk.Toplevel since another GUI instance is already running)
        temp_gui = tk.Toplevel()

        pad = 3
        temp_gui.geometry("{0}x{1}+0+0".format(
            temp_gui.winfo_screenwidth()-pad, temp_gui.winfo_screenheight()-pad))

        temp_gui.resizable(0, 0)
        temp_gui.title(image_name)

        # Load MoveAhead Logo into GUI
        image = Image.open(get_path("moveahead_logo.png"))
        image = image.resize((200, 60), Image.ANTIALIAS)
        # (150, 40)

        logo = ImageTk.PhotoImage(image)

        temp_gui_label = tk.Label(temp_gui, image=logo)
        temp_gui_label.photo = logo
        temp_gui_label.pack()

        # Load MoveAhead Logo into GUI
        dataset_image = Image.open(output_path)

        canvas = Canvas(width=200, height=200)
        canvas.pack(expand=NO, fill=NONE)

        img = ImageTk.PhotoImage(dataset_image)
        canvas.create_image(50, 50, image=img, anchor=NW)

        # panel = tk.Label(temp_gui, image=dataset_image)
        # panel.image = img
        # panel.pack()
        
        # video_player = tkvideo(video_path, video_label, loop = 1, size = (1280,720))
        # video_player.play()

        # Initialize JSON object for storing additional criteria 
        additional_criteria = {}

        # Hacky solution to set additional criteria variables(?)
        def setBool(key, var):
            additional_criteria[key] = var.get()

        user = sample_name.split("_")[0]
        sample = sample_name.split("_")[1].replace("s", "")

        l1 = tk.Label(temp_gui, text="User: {}".format(user))
        l1.place(x=1300, y=100)

        l2 = tk.Label(temp_gui, text="Sample: {}".format(sample))
        l2.place(x=1300, y=120)

        # # Initialise additional criteria values
        # additional_criteria["made_contact_with_ball"] = False
        # additional_criteria["correct_grip"] = False
        # additional_criteria["hit_in_front_to_side"] = False

        # Create multiple boxes depending on number of criteria to be manually assesed
        # v1 = tk.BooleanVar(temp_gui)
        # c1 = tk.Checkbutton(temp_gui, text="Made contact with ball", variable=v1, command=lambda:setBool("made_contact_with_ball", v1))
        # c1.place(x=1300, y=150)

        # v2 = tk.BooleanVar(temp_gui)
        # c2 = tk.Checkbutton(temp_gui, text="Correct grip", variable=v2, command=lambda:setBool("correct_grip", v2))
        # c2.place(x=1300, y=175)

        # v3 = tk.BooleanVar(temp_gui)
        # c3 = tk.Checkbutton(temp_gui, text="Ball hit in front & to the side", variable=v3, command=lambda:setBool("hit_in_front_to_side", v3))
        # c3.place(x=1300, y=200)
        
        # Using lambda to handle argument passing, stops function being exectued immediately when window loads
        # process_sample_button = tk.Button(temp_gui, text="Process Sample", command= lambda: self.process_sample(temp_gui, video_path, video_name, additional_criteria, config, date))
        # process_sample_button.place(x=1300, y=300)

        # process_sample_button = tk.Button(temp_gui, text="Upload Sample", command= lambda: self.upload_sample_no_BP(temp_gui, video_path, video_name, additional_criteria, config, date))
        # process_sample_button.place(x=1300, y=300)

        # invalid_sample_button = tk.Button(temp_gui, text="Invalid Sample", command= lambda: self.invalid_sample(temp_gui))
        # invalid_sample_button.place(x=1300, y=350)

        # Wait until the window is closed to open the next
        temp_gui.wait_window()
    

def main():
    # Load Tkinter root window
    window = tk.Tk()
    window.geometry("600x300")
    window.resizable(width=False, height=False)

    gui = DataProcessingTool(window)

    # Iinitialise event listener to wait for interactions with GUI elements
    window.mainloop()

if __name__ == "__main__":
    main()
import customtkinter as ctk
import tkinter as tk
from image_descriptor import find_size, list_all
import os
import time
from PIL import Image

import threading
import queue


# Supported modes : Light, Dark, System
ctk.set_appearance_mode("Dark") 

# Supported themes : green, dark-blue, blue
ctk.set_default_color_theme("green") 

appWidth, appHeight = 1700, 800

app = ctk.CTk()

app.geometry(f"{appWidth}x{appHeight}")
restart_thread = False

def browseFiles():
    filename = ctk.filedialog.askdirectory(initialdir="")
    label_file_explorer.configure(text="Current Directory: "+filename)
    directory_path.configure(text=filename)

def get_folder_size():
    directory = directory_path.cget("text")
    if(os.path.isdir(directory)):
        submit_button.grid_forget()
        button.grid_forget()
        size = find_size(directory)
        progressbar.set(0)

        files_left.configure(text=f"Files Completed: {progressbar.get()} / {size}")
        files_left.grid_configure(column = 1, row = 0, padx=90, pady=100, sticky="NEW")

        list_all(directory, progressbar, size, text=files_left, stream_text=answer_stream, image_placement=image_label, prompt=prompt_enter.get())

        submit_button.grid_configure(column = 1, row = 0, padx=90, pady=100, sticky="NEW")
        button.grid_configure(column = 1, row = 0, padx=90, pady=50, sticky="NEW")

        files_left.grid_forget()
    else:
        print("NOOOOOOO")
        print(directory)

# Thread so the progress bar can update in real time
def start_thread():
    thread = threading.Thread(target=get_folder_size, daemon=True) #create new instance if thread is dead
    thread.start() #start thread

app.resizable(True, True)
app.columnconfigure(1, weight=1)
app.columnconfigure(2, weight=1)
# app.rowconfigure(0, weight=1)
# app.rowconfigure(1, weight=1)
# app.rowconfigure(2, weight=1)
# app.rowconfigure(3, weight=1)
# app.rowconfigure(4, weight=1)

# image frame
frame = ctk.CTkFrame(app)

# frame.place(relx=0.45, relwidth=0.5, relheight=0.5)
# frame.grid(column=2, padx=20, sticky="EW")
# image generate
img = ctk.CTkImage(light_image=Image.open("images/place_holder.png"), size=(600 , 400))

# text frame
frame_text = ctk.CTkFrame(app)
# frame_text.place(relx=0.45, rely= 0.5, relwidth=0.5, relheight=0.5)
frame_text.grid(column=2, row=0, padx=10, pady=150, sticky="NEW")

# answer stream 
answer_stream = ctk.CTkLabel(master=frame_text, text='Descriptions will be here.', font=("Arial", 16))
# label.grid(column=2, row=1)
answer_stream.grid(column=2, row=1, padx=10, pady=250, sticky='NEW')

# label to place image
image_label = ctk.CTkLabel(master=app, image=img, text='')
# image_label.place(relwidth=1.0, relheight=1.0)
image_label.grid(column=2, row=0, padx=10, sticky="NEW")


# visual label of current directory
label_file_explorer = ctk.CTkLabel(app, text = "Choose a Folder with Images")
label_file_explorer.grid(column = 1, row = 0, padx=90, sticky="NEW")

# used as a string variable
directory_path = ctk.CTkLabel(app)

# Button to browse files
button = ctk.CTkButton(app, text="Browse Folders", command=browseFiles)
button.grid(column = 1, row = 0, padx=90, pady=50, sticky="NEW")

# Button to activate the image describer
submit_button = ctk.CTkButton(app, text="Submit", command=start_thread)
submit_button.grid(column = 1, row = 0, padx=90, pady=100, sticky="NEW")

# Progress bar for images being described
progressbar = ctk.CTkProgressBar(app)
progressbar.grid(column=1, row=0, padx=90, pady=150, sticky="NEW")
progressbar.set(0)

# Prompt Entry
prompt_enter = ctk.CTkEntry(app)
prompt_enter.grid(column=1, row=0, pady=200, padx=10, sticky="NEW")
ctk.CTkLabel(app, text="Prompt Here").grid(row=0, column=0, padx=10, pady=200, sticky="NEW")
prompt_enter.insert(0, "Describe this photo")

# Variable to show how many files left
files_left = ctk.CTkLabel(app, text = f"Files Completed: {progressbar.get()} ")

app.mainloop()

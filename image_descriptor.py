import textwrap
from time import sleep
from tqdm import tqdm
from image_chatter import ask_image, load_image
from functools import lru_cache
import time
import customtkinter as ctk

# TO DO:
# 1. 
# 2.   
# 3. 

import os
import filetype
import pyexiv2
#import exiftool
#from PIL import Image
#from exiftool import ExifToolHelper
from PIL import Image, ImageFile
ImageFile.LOAD_TRUNCATED_IMAGES = True

locked_files = []
valid_images_ext = ['jpg','png','tga', 'tif', 'tiff']

images_completed = 0

def output_stream(text):
    for i in range(len(text)):
        time.sleep(0.005)
        yield text[: i + 1]

def add_description(filename, label, image_label, prompt): 

    try:
        pyexiv2.Image(filename)
    except:
        print(f"Could not edit metadata on {filename}")
        locked_files.append(os.path.basename(filename))
        return
    
    image = load_image(filename)
    description = ask_image(image, prompt)

    img = ctk.CTkImage(light_image=image, size=(600 , 400))
    image_label.configure(image=img)

    for i in output_stream(description):
        label.configure(text = textwrap.fill(i, width = 95))

    image = pyexiv2.Image(filename)

    image.modify_exif({'Exif.Image.ImageDescription': textwrap.fill(description, width = 140)})

    image.close()

@lru_cache(maxsize=None, typed=False)
def find_size(directory):
    size = 0
    for object in os.listdir(directory):
        f = os.path.join(directory, object)

        # checking if it is a directory
        if os.path.isdir(f):
            size += find_size(f)

        elif os.path.isfile(f):
            if filetype.is_image(f) and filetype.guess(f).extension in valid_images_ext and os.access(f, os.W_OK):
                size += 1
    return size

#@lru_cache(maxsize=None, typed=False)
def list_all(directory, bar, size, text, stream_text, image_placement, prompt):
    global images_completed
    for object in os.listdir(directory):
        f = os.path.join(directory, object)
        
        # checking if it is a directory
        if os.path.isdir(f):
            list_all(f, bar, size, text, stream_text, image_placement, prompt)

        elif os.path.isfile(f):
            if filetype.is_image(f) and filetype.guess(f).extension in valid_images_ext:
                if os.access(f, os.W_OK):
                    #print(f)
                    add_description(f, stream_text, image_placement, prompt)
                    images_completed += 1
                    bar.set(images_completed / size)
                    # bar.update_idletasks()
                    text.configure(text = f"Files Completed: {images_completed} / {size}")
                else:
                    locked_files.append(os.path.basename(f))
                    
    if(images_completed == size):
        images_completed = 0


import tkinter as tk
from tkinter import *
from functools import partial
from PIL import ImageTk,Image

from gtts import gTTS 
import os 
import vlc  
import cv2
import numpy as np
from PIL import Image
import tempfile
import pytesseract
import os
from tqdm import tqdm


#-------------------------------------------------------------------------------------------------------------------------------------

def play_file(file_add):

	file=open(file_add,"r")
	mytext=file.read()
	#mytext = 'Welcome to geeksforgeeks!'
	  
	# Language in which you want to convert 
	language = 'en'


	myobj = gTTS(text=mytext, lang=language, slow=False) 
	  
	# Saving the converted audio in a mp3 file named 
	# welcome  
	myobj.save("converted.mp3") 
	  
	# Playing the converted file 

	p=vlc.MediaPlayer("converted.mp3")
	p.play()
	file.close()






#-------------------------------------------------------------------------------------------------------------------------------------


img_size = 1800
threshold = 215


def process_image(file):
    temp = image_dpi(file)
    im_new = remove_noise_and_smooth(temp)
    return im_new


def image_dpi(file):
    im = Image.open(file)
    length_x, width_y = im.size
    factor = max(1, int(img_size / length_x))
    size = factor * length_x, factor * width_y
    # size = (1800, 1800)
    im_resized = im.resize(size, Image.ANTIALIAS)
    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.png')
    temp = temp_file.name
    im_resized.save(temp, dpi=(300, 300))
    return temp


def smoothening(img):
    ret1, th1 = cv2.threshold(img, threshold, 255, cv2.THRESH_BINARY)
    ret2, th2 = cv2.threshold(th1, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    blur = cv2.GaussianBlur(th2, (1, 1), 0)
    ret3, th3 = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    return th3


def remove_noise_and_smooth(file_name):
    img = cv2.imread(file_name, 0)
    filtered = cv2.adaptiveThreshold(img.astype(np.uint8), 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 41, 3)
    kernel = np.ones((1, 1), np.uint8)
    opening = cv2.morphologyEx(filtered, cv2.MORPH_OPEN, kernel)
    closing = cv2.morphologyEx(opening, cv2.MORPH_CLOSE, kernel)
    img = smoothening(img)
    or_image = cv2.bitwise_or(img, closing)
    return or_image







#ENTER THE SINGLE IMAGE ADDRESS HERE
#ENTER THE DIR IMAGE ADDRESS HERE , UNCOMMNENT TO USE IT
#input_image_dir=""


####---------------DOING THE IMAGE PREPROCESSING----------------------------------
def single_image_text(img_add):
	image_address=img_add
	new_img=process_image(image_address)
	new_name=image_address[0:-4]+"_processed.png"
	cv2.imwrite(new_name, new_img)
	sentence = pytesseract.image_to_string(Image.open(new_name))
	address=image_address[0:-4]+"_text.txt"
	f=open(address,"w")
	f.write(str(sentence))
	f.close()
	play_file(address)






#---------------------------------------------------------------------------------------------------------------------------------------------------------------


root =tk.Tk()
root.geometry('320x80+0+0')
root.title('Image to Audio')




def call_result(label_result, n1):
    img_add = (n1.get())
    single_image_text(img_add)
    label_result.config(text="On Process")
    

#img = PhotoImage(file = r"G:\cell.png") 
#img1 = img.subsample(2, 2) 
#Label(root, image = img1).grid(row = 5, column = 5, 
#      columnspan = 1, rowspan = 1) 
 




number1=tk.StringVar()


labelTitle = tk.Label(root, text="Enter Image address").grid(row=1, column=2)






labelResult = tk.Label(root)
labelResult.grid(row=7, column=2)


entryNum1 = tk.Entry(root,textvariable=number1).grid(row=1, column=3)





call_result = partial(call_result, labelResult, number1)
buttonCal = tk.Button(root, text="Speak", command=call_result).grid(row=3, column=2)



root.mainloop()

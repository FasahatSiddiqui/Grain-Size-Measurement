import cv2
import os
import numpy as np
from tkinter import *
from tkinter.ttk import *
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from tkinter import messagebox
from tkinter import font
from PIL import Image, ImageTk



global file_path
file_path = []
def Openfile():
    global file_path
    #file_path =  filedialog.askopenfilename(initialdir = "/home/fasahat",title = "Select file",filetypes = [("picture","*.jpg .png .tif .bmp .gif"),("all files","*.*")])
    file_path =  filedialog.askopenfilename(initialdir = "P:\Python_codes",title = "Select file to open",filetypes = [("picture","*.jpg .png .tif .bmp .gif"),("all files","*.*")])
    img = cv2.imread(file_path)
    SS=img.shape
    my_text = tk.Text(initial_frame, height=1, width=16)
    my_text.grid(row=0, column=1, sticky='w', padx=3, pady=3)
    my_text.insert(tk.END, str(SS))
    cv2.imshow('Original Image', img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    imgr_height = int(img.shape[1]/1.5)
    size_ratio = (imgr_height / float(img.shape[1]))
    imgr_width = int((float(img.shape[0]) * float(size_ratio)))
    imgr = cv2.resize(img, (imgr_height, imgr_width), interpolation=cv2.INTER_AREA)
    cv2.imshow('Image prieview at 75%' 'height' + '=' + str(imgr_height), imgr)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

global sc
sc = []
def image_scale(): 
    global sc
    file_path
    if len(file_path) > 0:  
        img = cv2.imread(file_path)
        img_height = H
        size_ratio = (img_height / float(img.shape[1]))
        img_width = int((float(img.shape[0]) * float(size_ratio)))
        img = cv2.resize(img, (img_height, img_width), interpolation=cv2.INTER_AREA)
        import Pixel_Size
        sc = Pixel_Size.pixel_value(img)
        print('total pixel' + ' = '+ str(sc))
        sc = R/sc 
        print('scale of image' + ' = '+ str(sc)) 

global region
region = []
def image_crop():
    global region
    file_path
    if len(file_path) > 0:  
        img = cv2.imread(file_path,1)
        img_height = H
        size_ratio = (img_height / float(img.shape[1]))
        img_width = int((float(img.shape[0]) * float(size_ratio)))
        img = cv2.resize(img, (img_height, img_width), interpolation=cv2.INTER_AREA)
        import Crop_Image
        region = Crop_Image.crop_ROI(img)
        cv2.imshow('ROI', region)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
    

global d_mask
d_mask = []
def draw_boundary():
    global d_mask
    region
    img = np.zeros((region.shape))
    import Grain_Outline
    d_mask, img = Grain_Outline.draw_outline(region)
    cv2.imshow('mask', d_mask)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    save_filepath = os.path.join(os.path.dirname(file_path),os.path.splitext(os.path.basename(file_path))[0] +'_'+ str(H) +'_mask.tif')
    cv2.imwrite(save_filepath, d_mask)
    print(d_mask.shape)


def measure_grain():
    sc
    if len(d_mask.shape)>2:
        r_mask=cv2.cvtColor(d_mask, cv2.COLOR_RGB2GRAY)
    else:
        r_mask=d_mask.copy()

    #kernel = np.ones((1,1),np.uint8) 
    #eroded_mask = cv2.erode(r_mask,kernel,iterations = 1)
    #dilated_mask = cv2.dilate(eroded_mask,kernel,iterations = 1)

    r_mask[r_mask==0]=1    # area imside boundary
    r_mask[r_mask==255]=0  # boundary

    from skimage.measure import label, regionprops
    propList = ['Area','equivalent_diameter']
    label_mask = label(r_mask)
    regions = regionprops(label_mask)
    
    from skimage.color import label2rgb
    image_label_overlay = label2rgb(label_mask, image=r_mask, bg_label=0)
    cv2.imshow('mask', image_label_overlay)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    save_filepath = os.path.join(os.path.dirname(file_path),os.path.splitext(os.path.basename(file_path))[0] +'_measurement.csv')
    output_file = open(save_filepath, 'w')

    output_file.write('Grain No.' + ","+ ",".join(propList) + '\n') #join strings in array by  
    grain_number = 1
    for region_props in regions:
        output_file.write(str(grain_number))
        for prop in propList:
            if(prop == 'Area'):
                to_print = region_props[prop]*sc**2
            else: 
                to_print = region_props[prop]*sc
            output_file.write(',' + str(to_print))
        output_file.write('\n')
        grain_number += 1  

    output_file.close()


def h_value():
    global H
    H=int(cluster_box1.get())
    #print(H)

def r_value():
    global R
    R=int(cluster_box2.get())
    #print(R)
  
def u_value():
    global U
    U=unit_box.get()
    #print(U)
    
def data_upload():
    r_value()
    h_value()
    u_value()
    if U == 'Select unit':
        messagebox.showerror("Error","Please select the unit of scale")
    if len(file_path) <1:
        messagebox.showerror("Error","Please select input file correctly")
    if  H>0 and R>0 and len(file_path)>1:        
        messagebox.showinfo("Selection Value","Intial setting is sucessfully completed")
    
#GUI code start from here--------------------------------------------------------

root = tk.Tk()
root.title("GSM Tools")

Cap_font = font.Font(name='TkCaptionFont',exists=True,family='Arial Narrow',size=9,slant='roman',weight='normal')
Cap_font.config

menubar = tk.Menu(root)
# file manage bar
filemenu = tk.Menu(menubar, tearoff=0)
filemenu.add_command(label="Open", command=Openfile)
filemenu.add_command(label="Exit", command=root.quit)
menubar.add_cascade(label="File", menu=filemenu)
root.config(menu=menubar)

#-----------------------------------------------------------------------------------
initial_frame = tk.LabelFrame(root, text="Initilization")
initial_frame.grid(row=1, column=0, padx=10, pady=10)

spin_label1 = tk.Label(initial_frame, text="Image Size:")
spin_label1.grid(row=0, column=0, sticky='W', padx=3 , pady=3)

my_text = tk.Text(initial_frame, height=1, width=16)
my_text.grid(row=0, column=1, sticky='w', padx=3, pady=3)
my_text.insert(tk.END, "(X,Y,Z)")

spin_label1 = tk.Label(initial_frame, text="Set Image Height:")
spin_label1.grid(row=0, column=2, sticky='W', padx=3, pady=3)

var1 = tk.StringVar(value='700') # default setting
cluster_box1 = tk.Spinbox(initial_frame, cursor="arrow", from_=100, to=2000, width=10,textvariable=var1, justify=tk.RIGHT, command=h_value)
cluster_box1.grid(row=0, column=3, sticky='W', padx=3, pady=3)     

spin_label1 = tk.Label(initial_frame, text="Image Resolution:")
spin_label1.grid(row=0, column=4, sticky='W', padx=3, pady=3)

var2 = tk.StringVar(value='5') # default setting
cluster_box2 = tk.Spinbox(initial_frame, cursor="arrow", from_=1, to=15, width=10,textvariable=var2, justify=tk.RIGHT, command=r_value)
cluster_box2.grid(row=0, column=5, sticky='W', padx=3, pady=3) 

#Label('Combobox with text entry')
list1 = ('Select unit','um', 'nm')
var3 = tk.StringVar()
var3.set(list1[0])
unit_box = ttk.Combobox(initial_frame, width = 14, height=3, textvariable=var3, values=list1)
unit_box.grid(row=0, column=6,sticky='W', padx=3, pady=3)
                
#--------------------------------------------------------------------------------
Command_frame = tk.LabelFrame(root, text="Command Window")              
Command_frame.grid(row=0, column=0, padx=10, pady=10)

Upload_button = tk.Button(Command_frame, text="Upload data", command=data_upload)
Upload_button.grid(row=0, column=0,padx=6, pady=3) 

seg_button1 = tk.Button(Command_frame, text="Scale Image", command=image_scale)
seg_button1.grid(row=0, column=1, padx=6, pady=3)

Upload_button = tk.Button(Command_frame, text="Crop Image", command= image_crop)
Upload_button.grid(row=0, column=3,padx=6, pady=3) 

Upload_button = tk.Button(Command_frame, text="Draw Boundary", command= draw_boundary)
Upload_button.grid(row=0, column=4,padx=6, pady=3)

Upload_button = tk.Button(Command_frame, text="Measure Grain Size", command= measure_grain)
Upload_button.grid(row=0, column=5,padx=6, pady=3)

Exit_button = tk.Button(Command_frame, text='Program Exit', command=root.quit)
Exit_button.grid(row=0,column=6, padx=6, pady=3)

#root.iconphoto(False, PhotoImage(file ='/home/fasahat/Eco-Leafs.png')) 
#root.iconbitmap("P:\Python_codes\Eco-Leafs.ico")
root.mainloop()
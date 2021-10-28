import numpy as np
from statistics import mean
import cv2

def draw_outline(img):
    global ix, iy, fx, fy, drawing, d_mask
    img1=img.copy()
    d_mask=np.zeros((img1.shape[0],img1.shape[1]))
    drawing = False
    ix, iy = -1, -1

    # mouse callback function
    def mouse_crop(event, x, y, flags, params):
        global ix, iy, drawing #, overlay, output, alpha
        overlay = img1.copy()
        output = img1.copy()
        alpha = 0.5

        if event == cv2.EVENT_LBUTTONDOWN:
            drawing = True
            ix, iy = x, y        

        elif event == cv2.EVENT_MOUSEMOVE:
            if drawing == True:
                cv2.line(overlay, (ix, iy), (x,y), [0, 0, 255], 1)
                cv2.line(d_mask, (ix, iy), (x,y), [255], 2)
                cv2.addWeighted(overlay, alpha, output, 1 - alpha, 0, img1)
                ix, iy = x, y

        elif event == cv2.EVENT_LBUTTONUP:
            drawing = False

    cv2.namedWindow('image')
    cv2.setMouseCallback('image', mouse_crop)
    while(1):
        cv2.imshow('image', img1)
        if cv2.waitKey(20) & 0xFF==13:
            break
    cv2.destroyAllWindows()
    
    d_mask= d_mask.astype(np.uint8)
    return d_mask, img1


if __name__ =="__main__":
    import tkinter as tk
    from tkinter import filedialog
    root = tk.Tk()
    file_path = filedialog.askopenfilename(initialdir = "/home/fasahat/pCloudDrive/MyPictures/",title = "Select file",filetypes = [("picture","*.jpg .png .tif .bmp .gif")])
    root.destroy()

    img = cv2.imread(file_path,1)
    img_height = 1000
    size_ratio = (img_height / float(img.shape[1]))
    img_width = int((float(img.shape[0]) * float(size_ratio)))
    img = cv2.resize(img, (img_height, img_width), interpolation=cv2.INTER_AREA)

    import random
    clr = [random.randrange(0, 255, 10),random.randrange(0, 255, 10),random.randrange(0, 255, 10)]

    draw_outline(img)
    cv2.imshow('test 2', d_mask)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    
    save_path='P:\Python_codes\ImageJ_project\mask.tif'
    cv2.imwrite(save_path, d_mask)